from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "_apps.account"

    def ready(self) -> None:
        import _apps.account.signals  # noqa F401
