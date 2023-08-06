from django.conf import settings

__all__ = [
    'adsocket_settings'
]

DEFAULTS = {
    'driver': 'redis',
    'driver_options': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'channel': 'adsocket'
    }
}


class Settings:

    def __init__(self, defaults):
        self.defaults = defaults

    @property
    def django_settings(self):
        if not hasattr(self, '_django_settings'):
            self._django_settings = getattr(settings, 'ADSOCKET', {})
        return self._django_settings

    def __getattr__(self, item):

        if item not in self.defaults:
            raise AttributeError(f"Settings {item} does not exist")

        try:
            val = self.django_settings[item]
        except KeyError:
            val = self.defaults[item]

        return val


adsocket_settings = Settings(DEFAULTS)
