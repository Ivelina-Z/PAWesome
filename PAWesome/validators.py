from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator(BaseValidator):
    def __init__(self, max_size):
        super().__init__(self, max_size)
        self.max_size = max_size

    def __call__(self, value):
        max_size_bytes = 1024 ** 2 * self.max_size
        if value.size > max_size_bytes:
            raise ValidationError(f'The file should be less than {self.max_size} MB.')

    def __eq__(self, other):
        return self.value == other.value
