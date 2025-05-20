# products/templatetags/extras.py

from django import template
import math

register = template.Library()

@register.filter
def floor(value):
    try:
        return math.floor(float(value))
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    return float(value) - float(arg)