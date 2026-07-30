from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(name='html_tags')
def html_tags(value):
    return mark_safe(value)
