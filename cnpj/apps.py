from django.apps import AppConfig


class CnpjConfig(AppConfig):
    """Configuration for the Cnpj application."""

    default_auto_field: str= 'django.db.models.BigAutoField'
    name: str= 'cnpj'