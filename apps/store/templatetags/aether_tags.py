from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='inr')
def inr_format(value):
    """Formats numeric values in Indian Rupee format, e.g. 185000 -> ₹1,85,000"""
    if value is None or value == '':
        return '₹0'
    try:
        val = int(round(float(value)))
    except (ValueError, TypeError):
        return f"₹{value}"
    
    s = str(val)
    if len(s) <= 3:
        return f"₹{s}"
    last_three = s[-3:]
    remaining = s[:-3]
    out = ""
    while len(remaining) > 2:
        out = "," + remaining[-2:] + out
        remaining = remaining[:-2]
    if remaining:
        out = remaining + out
    return f"₹{out},{last_three}"


@register.filter(name='times')
def times(number):
    """Returns range(1, number+1) for star rating loops"""
    try:
        return range(int(number))
    except (ValueError, TypeError):
        return []


@register.filter(name='sub')
def sub(value, arg):
    """Subtracts arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
