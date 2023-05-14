import os
from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[-1]
    valid_extensions = [".png", ".jpg", ".jpeg"]
    if not str(ext).lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extension. Allowed: " + str(valid_extensions)
        )
