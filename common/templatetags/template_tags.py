from django import template

register = template.Library()


@register.simple_tag
def update_variable(value):
    data = value
    return data


@register.filter(is_safe=False)
def subtract(value, arg):
    """Adds the arg to the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''
