from .actions import ADSocketAction
from .transport import ACTION_CREATE, ACTION_DELETE, ACTION_UPDATE
from django.db.models import Model


class A(ADSocketAction):

    class Meta:
        models = 'whatever'
        actions = [ACTION_UPDATE, ACTION_CREATE, ACTION_DELETE]

    def __init__(self, *args, **kwargs):
        print(*args, **kwargs)
        print(self.meta)
