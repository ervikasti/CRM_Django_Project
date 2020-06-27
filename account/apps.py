from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    #for signals to work,we override ready method
    def ready(self):
        import account.signals