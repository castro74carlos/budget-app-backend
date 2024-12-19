from django import template

register = template.Library()

@register.filter
def display_amount(transaction):
    sign = "+" if transaction.type == "INC" else "-"
    return f"{sign}${transaction.amount}"
