from django.forms import CheckboxInput
from django.forms.utils import flatatt
from django.utils.html import format_html


class CustomDeleteFormsetWidget(CheckboxInput):
    template_name = 'delete-formset-widget.html'
