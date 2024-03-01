from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
# inside apps.py

class TranslateConfig(AppConfig):
    name = 'google_translate'
