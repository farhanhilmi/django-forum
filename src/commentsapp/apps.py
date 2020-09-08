from django.apps import AppConfig


class CommentsappConfig(AppConfig):
    name = 'commentsapp'

    def ready(self):
        import commentsapp.signals
