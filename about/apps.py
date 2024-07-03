from django.apps import AppConfig


class AboutConfig(AppConfig):
    """
    Defining a class that inherits from Django's AppConfig.
    It will be used to configure the 'about' app
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'about'
