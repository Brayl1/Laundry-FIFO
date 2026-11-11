from decimal import Decimal, InvalidOperation
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
PATHS = {
 "grid": '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
 "inbox": '<path d="M4 4h16l2 12v4H2v-4L4 4Z"/><path d="M2 14h6l2 3h4l2-3h6"/>',
 "queue": '<path d="M4 6h16M4 12h10M4 18h6m6-3 4 3-4 3"/>',
 "workflow": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M6 9v9h9m-3-3 3 3-3 3M9 6h9v6"/>',
 "chart": '<path d="M4 3v17h17M9 15V9m5 6V5m5 10v-4"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "archive": '<rect x="3" y="3" width="18" height="4" rx="1"/><path d="M5 7v14h14V7m-10 5h6"/>',
 "team": '<circle cx="9" cy="8" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3m1-16a3 3 0 0 1 0 6m2 4a5 5 0 0 1 3 4v2"/>',
 "settings": '<path d="M4 7h16M4 17h16"/><circle cx="9" cy="7" r="3"/><circle cx="15" cy="17" r="3"/>',
 "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "arrow": '<path d="M4 12h16m-6-6 6 6-6 6"/>',
 "check": '<path d="m5 12 4 4L19 6"/>',
 "chevron": '<path d="m8 10 4 4 4-4"/>',
 "download": '<path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4"/>',
 "book": '<path d="M12 5v16M3 3l9 2 9-2v16l-9 2-9-2V3Z"/>',
 "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
 "logout": '<path d="M9 4H3v16h6m5-14 6 6-6 6M8 12h12"/>',
 "bolt": '<path d="m13 2-9 12h7l-1 8 10-12h-7l1-8Z"/>',
 "flag": '<path d="M5 22V3m0 1c5-5 9 5 14 0v11c-5 5-9-5-14 0"/>',
 "note": '<path d="M4 3h16v18H4zM8 8h8m-8 4h8m-8 4h4"/>',
 "washer": '<rect x="4" y="2.5" width="16" height="19" rx="2.5"/><circle cx="12" cy="14" r="4.5"/><path d="M7.5 6h.01M10.5 6h.01"/>',
 "droplet": '<path d="M12 3c3.6 4.2 6 6.7 6 10a6 6 0 0 1-12 0c0-3.3 2.4-5.8 6-10Z"/>',
 "shirt": '<path d="m8 3-5 3 2 4 3-1.5V21h8V8.5l3 1.5 2-4-5-3a4 4 0 0 1-8 0Z"/>',
 "tag": '<path d="M3 12V4h8l10 10-8 8L3 12Z"/><circle cx="7.5" cy="8.5" r="1"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>',
 "scale": '<circle cx="12" cy="12" r="9"/><path d="m12 12 3.2-3.2M7.5 7.3a6.5 6.5 0 0 1 9 0"/>',
 "wallet": '<path d="M3 7a2 2 0 0 1 2-2h13v4"/><path d="M3 7v11a2 2 0 0 0 2 2h14a1 1 0 0 0 1-1V9H5a2 2 0 0 1-2-2Z"/><path d="M16 14.5h.01"/>',
}
@register.simple_tag
def icon(name):
    path = PATHS.get(name, PATHS["grid"])
    return mark_safe('<svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+path+'</svg>')


@register.filter
def peso(value):
    """Format an amount of money as Philippine pesos, e.g. 220 -> "₱220.00". Empty values show a dash."""
    if value in (None, ""):
        return "—"
    try:
        return f"₱{Decimal(str(value)):,.2f}"
    except (InvalidOperation, ValueError):
        return "—"


@register.filter
def kilos(value):
    """Format a weight without trailing zeros, e.g. Decimal('5.50') -> "5.5 kg". Empty values show a dash."""
    if value in (None, ""):
        return "—"
    try:
        return f"{Decimal(str(value)).normalize():f} kg"
    except (InvalidOperation, ValueError):
        return "—"
