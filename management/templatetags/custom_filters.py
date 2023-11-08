import decimal

from django import template
from django.core.paginator import Paginator

from management.models import Management

register = template.Library()


@register.simple_tag
def paginate_url(value, field_name, urlencode=None):
    url = "?{}={}".format(field_name, value)
    if urlencode:
        querystring = urlencode.split("&")
        filter_querystring = filter(lambda p: p.split("=")[0] != field_name, querystring)
        encoded_querystring = "&".join(filter_querystring)
        url = "{}&{}".format(url, encoded_querystring)
        print(url)
    return url


@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=2, on_ends=2):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number,
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)


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


@register.simple_tag
def check_error_field_name(instance_id, field_name, instances_errors):
    """

    this is using a template tags to get the error if it exist in the instance
    :param instance_id:
    :param field_name:
    :param instances_errors:
    :return:
    """
    for item in instances_errors:
        # if the id of the error
        if item.get("id") == instance_id:
            # if the field name exists
            if item.get(field_name):
                return "error_exist_class"
    return ""


@register.filter
def get_field_type(field_name):
    try:
        field_object = Management._meta.get_field(field_name)
        return field_object.get_internal_type()
    except Exception as e:
        return ''
