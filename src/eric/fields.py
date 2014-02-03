from uuid import uuid4

from django.db.models.fields import CharField


_ALPHA_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

_ALPHA_UNIQUE_FIELD_LENGTH = 20


def get_alpha_unique_value():
    unique_integer = uuid4().int
    alpha_chars_count = len(_ALPHA_CHARS)
    
    characters = []
    while len(characters) < _ALPHA_UNIQUE_FIELD_LENGTH:
        unique_integer, remainder = divmod(unique_integer, alpha_chars_count)
        character = _ALPHA_CHARS[remainder]
        characters.append(character)
    
    return "".join(characters)


class AlphaUniqueField(CharField):
    
    def __init__(self, *args, **kwargs):
        super(AlphaUniqueField, self).__init__(
            default=get_alpha_unique_value,
            max_length=_ALPHA_UNIQUE_FIELD_LENGTH,
            *args,
            **kwargs
            )
