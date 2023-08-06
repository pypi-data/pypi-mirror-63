import logging
import types

from adsocket_transport.transport import ADSocketTransport
from adsocket_transport.exceptions import ADSocketException
from adsocket_transport.message import Message

from .utils import DeferredService
from .creator import ADSocketCreator, ADSocketCreatorMeta
from .exceptions import ADSocketDuplicityError
from .activity import ActivityName, CREATE, UPDATE, DELETE
from django.db.models import Model
from django.db.models.signals import post_save, pre_delete
from django.db.models.utils import make_model_tuple

_logger = logging.getLogger(__name__)

__all__ = [
    'ADSocketTransportDjango',
    'adsocket',

]


class ActionDefinition:
    # __slots__ = ('model', '_actions', 'callback', 'creator', '_frozen')
    _model = None
    _creator = None
    _actions = None
    callback = None

    def __init__(self, model=None, actions=None, callback=None, creator=None):
        """
        ActionDefinition is simple dataclass to make work with params easier,
        since there is a difference between registring Model & Creator

        :param model: Django model instance
        :type model: django.db.models.Model
        :param actions: list of actions
        :type actions: list
        :param callback: callback function to be called after the signal received
        :type callback: func
        :param creator: Creator object instance
        :type creator: adsocket_transport.creator.ADSocketCreator
        """
        self._model = model
        if actions:
            for a in actions:
                if not isinstance(a, ActivityName):
                    t = type(a)
                    raise ADSocketException(
                        f"Action must be instance of "
                        f"adsocket.transport.ActionName not {t}"
                    )
            self._actions = actions

        if creator and not issubclass(creator, (ADSocketCreator, ADSocketCreatorMeta)):
            t = type(creator)
            raise ADSocketException(
                f"Action must be instance of "
                f"adsocket_transport_django.ADSocketCreator not {t}"
            )
        self.creator = creator

        if callback and not hasattr(callback, '__call__'):
            raise ADSocketException("Callback must be callable object or function")
        self.callback = callback

    @property
    def actions(self):
        if self.creator:
            return self.creator.meta.actions
        return self._actions

    @property
    def model(self):
        if self.creator:
            return self.creator.meta.model
        return self._model


class ADSocketTransportDjango(ADSocketTransport):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._models = {}

    def register(self, model: Model, actions=None, callback=None):
        """
        Register Django model to ADSocket Transport

        :param model: Django model class
        :type model: django.db.models.Model
        :param actions: List of actions
        :type actions: list
        :param callback: function to be called when signal was raised
        :type callback: func
        :return: void
        :rtype: void
        """
        actions = actions or [CREATE, UPDATE, DELETE]

        if not issubclass(model, Model):
            raise ADSocketException("Model must be "
                                    "django.db.models.Model instance")

        if not callback and not hasattr(model, 'adsocket_hook'):
            raise ADSocketException(f"I don't have any callback "
                                    f"for model {model}")

        fqmn = '.'.join(make_model_tuple(model))
        if fqmn in self._models:
            raise ADSocketException(f"You are trying to register "
                                    f"model {model} twice")

        ad = ActionDefinition(
            model=model,
            callback=callback,
            actions=actions
        )
        self._activate(ad)

    def register_decorator(self, func, model, actions=None):
        """

        :param func: Decorated function
        :type func: function
        :param model: Django model instance
        :type model: django.db.models.Model
        :param actions: List of actions you want to
        :type actions:
        :return:
        :rtype:
        """
        self.register(model=model, actions=actions, callback=func)
        return func

    def register_creator(self, creator: ADSocketCreator):
        fqmn = '.'.join(make_model_tuple(creator.meta.model))
        self._check_for_duplicities(fqmn)
        ad = ActionDefinition(creator=creator)
        self._models[fqmn] = ad
        self._activate(ad)

    def deregister(self, model):
        fqmn = '.'.join(make_model_tuple(model))
        if fqmn not in self._models:
            return

        model = self._models[fqmn]
        if model.has_creator():
            actions = model.meta.actions
            model = model.meta.model
        else:
            actions = model.actions
            model = model.model

        if CREATE in actions or UPDATE in actions:
            post_save.disconnect(self.receive_signal_save, model.model)
        if DELETE in actions:
            pre_delete.disconnect(self.receive_signal_delete, model.model)

        del self._models[fqmn]

    def _activate(self, ad: ActionDefinition):

        if UPDATE or CREATE in ad.actions:
            post_save.connect(self.receive_signal_save, ad.model)
        if DELETE in ad.actions:
            pre_delete.connect(self.receive_signal_delete, ad.model)

    def _check_for_duplicities(self, fqmn):
        """
        Since single model can be registered only once we have to make
        sure that new model isn't already registered

        :param fqmn: Fully qualified model name
        :type fqmn: str
        :raises: ADSocketDuplicityError
        :return: void
        :rtype: void
        """
        if fqmn in self._models:
            raise ADSocketDuplicityError(f"Model {fqmn} already registered")

    def _signal_handler(self, sender: Model, activity: ActivityName, **kwargs):
        """
        Model Signal receiver. If all requirements met, callback function or
        'adsocket_hook' method on model is gonna be executed. Return value of
        this function otr method is supposed to be Message instance
        or tuple:
        ('name:id (of channel)', {"message": "data"})


        :param models.Model sender: Django model instance
        :param ActionName action: What action we are performing (create, update,
                            delete)
        :param dict kwargs:
        :return:
        """
        fqmn = '.'.join(make_model_tuple(sender))
        _logger.debug(f"Received {activity} signal ({fqmn})")
        if fqmn not in self._models:
            _logger.error(f"Model not found {fqmn}")
            return
        instance = kwargs.get('instance')
        ad = self._models[fqmn]

        if activity == CREATE and CREATE not in ad.actions:
            _logger.debug(f"Create action not wanted for "
                          f"model {sender.__class__}")
            return

        if activity == UPDATE and UPDATE not in ad.actions:
            _logger.debug(f"Update action not wanted for "
                          f"model {sender.__class__}")
            return

        if activity == DELETE and DELETE not in ad.actions:
            _logger.debug(f"Delete action not wanted for "
                          f"model {sender.__class__}")
            return
        if ad.creator:
            creator = ad.creator()
            func = getattr(creator, str(activity))
            result = func(instance)
        elif ad.callback:
            result = ad.callback['cb'](instance, activity)
        elif hasattr(instance, 'adsocket_hook'):
            result = instance.adsocket_hook(instance, activity)
        else:
            raise ADSocketException(f"Callback not set for "
                                    f"model {instance.__class__}")
        if isinstance(result, Message):
            self.send(result)
        elif isinstance(result, (list, tuple, types.GeneratorType)):
            for msg in result:
                if isinstance(msg, Message):
                    self.send(msg)
                else:
                    self.send_data(result[0], result[1])
        elif isinstance(result, tuple):
            self.send_data(result[0], result[1])
        elif result is None:
            pass
        else:
            _logger.error(f"Unknown result coming from hook {instance.__class__}")

    def receive_signal_save(self, sender, **kwargs):
        """
        Detect action what was performed and call _signal_handler

        :param models.Model sender: Django model instance
        :param dict kwargs: Signal kwargs
        :return:
        """
        try:
            action = CREATE if kwargs.get('created') else UPDATE
            return self._signal_handler(sender, action, **kwargs)
        except Exception as e:
            _logger.exception(str(e))

    def receive_signal_delete(self, sender, **kwargs):
        """
        Just adds ACTION_DELETE and call _signal_handler

        :param models.Model sender: Django model instance
        :param dict kwargs: Signal kwargs
        :return:
        """
        try:
            return self._signal_handler(sender, DELETE, **kwargs)
        except Exception as e:
            _logger.exception(str(e))

adsocket = DeferredService(ADSocketTransportDjango)
# adsocket = ADSocketTransportDjango(
#     driver=adsocket_settings.driver,
#     driver_options=adsocket_settings.driver_options
# )

# adsocket_decorator = adsocket.register_decorator
