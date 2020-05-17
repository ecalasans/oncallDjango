from django import template
register = template.Library()

@register.filter
def get_value(value, key):
    return value.get(key)

@register.filter
def get_key(dicionario, valor):
    for key, value in dicionario.items():
        if value == valor:
            return key
        else:
            continue