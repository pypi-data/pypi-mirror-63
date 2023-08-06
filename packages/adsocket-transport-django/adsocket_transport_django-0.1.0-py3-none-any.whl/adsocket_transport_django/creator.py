import abc


from .exceptions import ADSocketConfigurationError
from .activity import CREATE, DELETE, UPDATE


__all__ = [
    'ADSocketCreator'
]


class ADSocketCreatorMeta(type):

    META_ATTRIBUTES = ['model', 'actions']

    def __new__(mcs, klazz, bases, attrs):

        # Do this only on subclasses of BaseWorkflowMetaclass
        parents = [b for b in bases if isinstance(b, ADSocketCreatorMeta)]
        if not parents:
            # It's something else, so go ahead
            return super().__new__(
                mcs, klazz, bases, attrs
            )

        base_meta = ADSocketCreator.Meta
        meta = attrs.pop('Meta', None)
        meta_instance = base_meta()
        for x in ADSocketCreatorMeta.META_ATTRIBUTES:
            meta_instance.__dict__[x] = base_meta.__dict__[x]
            if meta and hasattr(meta, x):
                meta_instance.__dict__[x] = meta.__dict__[x]

        if meta_instance.model is None:
            raise ADSocketConfigurationError(
                "`model` attribute must be set and msut be "
                "subclass of django.db.Model")
        from django.db.models import Model
        if not issubclass(meta_instance.model, Model):
            raise ADSocketConfigurationError(
                "`model` attribute must be subclass of django.db.Model")

        attrs['meta'] = meta_instance

        return super().__new__(mcs, klazz, bases, attrs)


class ADSocketCreator(metaclass=ADSocketCreatorMeta):

    class Meta:
        model = None
        actions = [CREATE, DELETE, UPDATE]

    def create(self, model):
        raise NotImplementedError("Method create is not implemented")

    def update(self, model):
        raise NotImplementedError("Method update is not implemented")

    def delete(self, model):
        raise NotImplementedError("Method delete is not implemented")

