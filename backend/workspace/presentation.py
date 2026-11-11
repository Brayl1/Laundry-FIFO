"""View-only helpers: the dashboard's activity chart geometry and the pickup text message."""
from datetime import timedelta
from math import ceil
from django.utils import timezone


def activity_chart(created, resolved, start):
    created_days = [timezone.localtime(value).date() for value in created]
    resolved_days = [timezone.localtime(value).date() for value in resolved]
    days = [{"day": start + timedelta(days=i),
             "created": created_days.count(start + timedelta(days=i)),
             "resolved": resolved_days.count(start + timedelta(days=i))} for i in range(7)]
    peak = max([row[key] for row in days for key in ("created", "resolved")] + [1])
    ceiling = max(4, ceil(peak / 4) * 4)
    left, right, top, bottom = 46, 710, 22, 252
    for i, row in enumerate(days):
        row["x"] = round(left + i * (right - left) / 6, 2)
        for key in ("created", "resolved"):
            row[key + "_y"] = round(bottom - row[key] / ceiling * (bottom - top), 2)
    def line(key):
        return "M " + " L ".join(f'{row["x"]},{row[key + "_y"]}' for row in days)
    created_line, resolved_line = line("created"), line("resolved")
    return {"days": days, "created_line": created_line, "resolved_line": resolved_line,
            "created_area": created_line + f" L {right},{bottom} L {left},{bottom} Z",
            "resolved_area": resolved_line + f" L {right},{bottom} L {left},{bottom} Z",
            "ticks": [{"value": ceiling - i * ceiling // 4,
                       "y": top + i * (bottom-top) / 4} for i in range(5)],
            "start": start, "end": start + timedelta(days=6),
            "created_total": sum(row["created"] for row in days),
            "resolved_total": sum(row["resolved"] for row in days)}


def pickup_message(ticket, shop_name):
    """A ready-to-send text for a customer whose order is Ready for pickup. Plain text; the template escapes it."""
    greeting = f"Hi {ticket.customer_name}!" if ticket.customer_name else "Hello!"
    lines = [f"{greeting} Your laundry {ticket.reference} is ready for pickup at {shop_name}."]
    if ticket.weight_kg is not None:
        kilos = f"{ticket.weight_kg.normalize():f}"
        lines.append(f"{kilos} kg, {ticket.get_service_type_display()}. Amount due: PHP {ticket.amount_due:,.2f}.")
    lines.append("Thank you for choosing us!")
    return " ".join(lines)
