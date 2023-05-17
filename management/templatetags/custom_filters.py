from django import template

register = template.Library()


@register.filter
def get_all_fields(obj):
    return obj._meta.fields


@register.filter
def get_all_field_values(obj):
    return [getattr(obj, field.name) for field in obj._meta.fields]


@register.filter
def zip_fields_values(fields, values):
    return zip(fields, values)


@register.filter
def render_form_with_instance(form, instance):
    for field in form:
        if field.name != "user":
            field.field.widget.attrs['value'] = getattr(instance, field.name)
    return form
