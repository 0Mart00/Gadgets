from django.db import models

class JsonQueryMixin(models.Model):
    """
    Mixin a JSON mezők dinamikus lekérdezéséhez.
    Feltételezi, hogy a JSON mező neve 'specs', vagy felülírható.
    """
    class Meta:
        abstract = True

    @classmethod
    def filter_by_spec(cls, key: str, value: any, field_name: str = 'specs'):
        """
        Dinamikus szűrés JSON kulcs-érték párra.
        Használat: Gadget.filter_by_spec('cpu_cores', 8)
        """
        filter_kwargs = {f"{field_name}__{key}": value}
        return cls.objects.filter(**filter_kwargs)

    @classmethod
    def has_spec_key(cls, key: str, field_name: str = 'specs'):
        """Ellenőrzi, hogy egy kulcs létezik-e a JSON-ben."""
        filter_kwargs = {f"{field_name}__has_key": key}
        return cls.objects.filter(**filter_kwargs)