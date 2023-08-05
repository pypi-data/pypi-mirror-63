from typing import Any

from django import template
from django.forms import BoundField
from django.template import Template

from flex_forms.components import FlexFieldType, BaseStaticFlexField, StaticFlexFieldType
from flex_forms.forms import FlexFormParameters

register = template.Library()

dummy = Template("""{% extends wrapper_template %}""")


@register.inclusion_tag(dummy)
def flex_field(bound_field: BoundField, label: str = None, required: bool = None, **kwargs):
    """
    Takes context and render field in specified template.
    Expected params:

    - required_text
    - icon
    - show_errors
    - wrapper_template
    - field_group_class
    """

    if bound_field:
        widget = bound_field.field.widget
        field_type = type(widget).__name__
        label = label if label is not None else bound_field.label
        required = required if required is not None else bound_field.field.required
        readonly = bound_field.field.widget.attrs.get(FlexFormParameters.READONLY, False)
        disabled = bound_field.field.disabled
        icon = kwargs.get(FlexFormParameters.ICON) or widget.attrs.pop(FlexFormParameters.ICON, None)
        additional_icon = kwargs.get(FlexFormParameters.ADDITIONAL_ICON) or \
                          widget.attrs.pop(FlexFormParameters.ADDITIONAL_ICON, None)
        required_text = widget.attrs.pop(FlexFormParameters.REQUIRED_TEXT, '')
        show_errors = widget.attrs.pop(FlexFormParameters.SHOW_ERRORS, True)
        wrapper_template = \
            kwargs.get(FlexFormParameters.WRAPPER_TEMPLATE) or widget.attrs.get(FlexFormParameters.WRAPPER_TEMPLATE)
        field_group_class = \
            kwargs.get(FlexFormParameters.FIELD_GROUP_CLASS) or \
            widget.attrs.pop(FlexFormParameters.FIELD_GROUP_CLASS, '')

        context = dict(
            field=bound_field,
            field_group_class=field_group_class,
            wrapper_template=wrapper_template,
            label=label,
            required=required,
            required_text=required_text,
            field_type=field_type,
            icon=icon,
            additional_icon=additional_icon,
            show_errors=show_errors,
            readonly=FlexFormParameters.READONLY if readonly else '',
            disabled=FlexFormParameters.DISABLED if disabled else ''
        )
        context.update(kwargs)

        return context


@register.inclusion_tag(dummy)
def static_flex_field(static_field: StaticFlexFieldType, label: str = None, **kwargs):
    """
    Render static html as a ordinary field.
    Expected params:

    - icon
    - wrapper_template
    - field_group_class
    """

    if static_field:
        label = label if label is not None else static_field.label
        icon = kwargs.get(FlexFormParameters.ICON) or static_field.icon
        wrapper_template = kwargs.get(FlexFormParameters.WRAPPER_TEMPLATE) or static_field.wrapper_template
        field_group_class = kwargs.get(FlexFormParameters.FIELD_GROUP_CLASS) or static_field.field_group_class
        help_text = static_field.help_text
        data = static_field.data

        context = dict(
            field_group_class=field_group_class,
            wrapper_template=wrapper_template,
            label=label,
            icon=icon,
            help_text=help_text,
            data=data
        )
        context.update(kwargs)

        return context


@register.inclusion_tag(dummy)
def complex_flex_field(field: FlexFieldType, **kwargs):
    """
    Complex field context handler.
    """

    context = {}
    if isinstance(field, BoundField):
        context = flex_field(field, **kwargs)
    elif isinstance(field, BaseStaticFlexField):
        context = static_flex_field(field, **kwargs)

    return context


@register.simple_tag
def flex_form_grid(form_object: Any, start_row: int = 0, end_row: int = None) -> str:
    """
    Render form fields from map specified in the form.
    """

    from flex_forms.utils import FlexFormObjectFieldCollector

    collector = FlexFormObjectFieldCollector(form_object)
    collector.start_row = start_row
    collector.end_row = end_row
    return collector.get_template()


@register.simple_tag(takes_context=True)
def as_flex(context, form_object: Any) -> str:
    """
    Render form objects with csrf_token in the context.
    """

    if form_object:
        form_object.extra_context.update(dict(csrf_token=context.get('csrf_token')))
        return form_object.as_flex()
    return ''


@register.filter
def check_form_method(params: dict) -> bool:
    """
    Checker to controls for adding a csrf_token to the form.
    """

    return params.get('method') not in ['GET', 'get']
