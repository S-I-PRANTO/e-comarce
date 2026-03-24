from django.core.exceptions import ValidationError

def validate_file(file):
    
    max_size=10
    max_size_in_bytes=max_size * 1024 * 1024

    if file.size > max_size_in_bytes:
        raise ValidationError(f"File can't be larger then {max_size}MB ")
     