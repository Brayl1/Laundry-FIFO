import re
from decimal import Decimal
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from database.models import Membership
from database.models import ACCENTS, STATUSES, Ticket, Workspace


class TicketForm(forms.ModelForm):
    version = forms.IntegerField(required=False, widget=forms.HiddenInput)
    def __init__(self, *args, workspace=None, **kwargs):
        super().__init__(*args, **kwargs)
        members = Membership.objects.filter(workspace=workspace, role__in=["owner", "manager", "agent"]).values("user_id")
        self.fields["assignee"].queryset = get_user_model().objects.filter(id__in=members).order_by("first_name", "username")
        self.fields["assignee"].label_from_instance = lambda user: user.get_full_name() or user.get_username()
        self.fields["assignee"].empty_label = "Unassigned"
        # Laundry details are optional so an order can be written down before the bag is weighed.
        # An empty service falls back to the default in services.save_ticket.
        self.fields["service_type"].required = False
        self.fields["weight_kg"].validators.extend([MinValueValidator(Decimal("0.1")), MaxValueValidator(Decimal("99.99"))])
        if self.instance.pk:
            self.fields["version"].initial = self.instance.version
            self.fields["version"].required = True
    class Meta:
        model = Ticket
        fields = ("title", "customer_name", "customer_phone", "service_type", "weight_kg", "category", "status",
                  "priority", "due_date", "assignee", "requester_email", "description")
        labels = {
            "title": "Order label",
            "customer_name": "Customer name",
            "customer_phone": "Mobile number",
            "service_type": "Service",
            "weight_kg": "Weight (kg)",
            "category": "Load type",
            "priority": "Turnaround",
            "due_date": "Promised pickup date",
            "assignee": "Handled by",
            "requester_email": "Customer email (optional)",
            "description": "Notes for the attendant",
        }
        help_texts = {
            "title": "How you will find this bag, for example \"Santos weekly bag\".",
            "weight_kg": "Weigh the dry laundry. The amount due is worked out for you.",
            "category": "For example Everyday clothes, Bedding, Uniforms or Delicates.",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "No fabric softener. Wash whites separately."}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "customer_name": forms.TextInput(attrs={"placeholder": "Maria Santos", "autocomplete": "off"}),
            "customer_phone": forms.TextInput(attrs={"placeholder": "0917 555 0142", "inputmode": "tel", "autocomplete": "off"}),
            "weight_kg": forms.NumberInput(attrs={"step": "0.1", "min": "0.1", "max": "99.99", "inputmode": "decimal", "placeholder": "5.5"}),
        }

    def clean_title(self):
        value = self.cleaned_data["title"].strip()
        if not value:
            raise forms.ValidationError("Give this item a title.")
        return value

    def clean_category(self):
        value = self.cleaned_data["category"].strip()
        if not value:
            raise forms.ValidationError("Enter a load type.")
        return value

    def clean_customer_phone(self):
        value = self.cleaned_data.get("customer_phone", "").strip()
        if value and not re.fullmatch(r"[0-9+()\-\s]{4,20}", value):
            raise forms.ValidationError("Use digits, spaces, + or - only, for example 0917 555 0142.")
        return value


class PreferencesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep the existing stored key so current databases need no migration.
        self.fields["accent"].choices = [("teal", "Ocean blue (default)"), ("violet", "Lavender"), ("forest", "Mint"), ("clay", "Peach")]

    class Meta:
        model = Workspace
        fields = ("name", "accent")

    def clean_name(self):
        value = self.cleaned_data["name"].strip()
        if not value:
            raise forms.ValidationError("Enter your laundry shop's name.")
        return value


class MoveForm(forms.Form):
    status = forms.ChoiceField(choices=STATUSES)


class WorkflowForm(forms.Form):
    operation = forms.ChoiceField(choices=[
        ("append", "Add to end · append"), ("prepend", "Add to start · prepend"),
        ("insert_at", "Insert at position · insert_at"), ("remove_at", "Remove at position · remove_at"),
        ("remove", "Remove first matching step · remove"), ("get", "Read at position · get"),
        ("index_of", "Find first position · index_of"),
    ])
    value = forms.CharField(max_length=80, required=False)
    index = forms.IntegerField(min_value=0, required=False)

    def clean(self):
        data = super().clean()
        op = data.get("operation")
        if op in {"append", "prepend", "insert_at", "remove", "index_of"} and not data.get("value", "").strip():
            self.add_error("value", "This operation needs a value.")
        if op in {"insert_at", "remove_at", "get"} and data.get("index") is None:
            if "index" not in self.errors:
                self.add_error("index", "This operation needs an index.")
        return data


class CommentForm(forms.Form):
    body = forms.CharField(max_length=3000, widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Add context, a handoff, or a progress update…"}), label="Team note")
