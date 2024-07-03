from django.apps import AppConfig


class PostsConfig(AppConfig):
    """
    Defining a class that inherits from Django's AppConfig
    It will be used to configure the 'posts' app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
