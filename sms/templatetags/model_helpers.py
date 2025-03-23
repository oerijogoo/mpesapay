from django import template

register = template.Library()

@register.filter
def model_name(model_class):
    """Returns the lowercase model name from a model class"""
    return model_class._meta.model_name