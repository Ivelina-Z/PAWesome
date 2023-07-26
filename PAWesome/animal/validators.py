from django.core.exceptions import ValidationError


def validate_one_main_image(formset):
    total_main_images = 0
    for instance in formset:
        if instance.cleaned_data['is_main_image']:
            total_main_images += 1
        if total_main_images > 1:
            raise ValidationError('The main image can be only ONE.')
