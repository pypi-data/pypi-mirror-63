import importlib

from .creator import ADSocketCreator, ADSocketCreatorMeta


def import_module(pth):
    """

    :param pth:
    :return:
    """
    the_module, klazz = pth.rsplit('.', 1)
    the_module = importlib.import_module(the_module)
    class_ptr = getattr(the_module, klazz)

    return class_ptr


class ADSocketConfig:

    adsocket_signals = []

    def ready(self):
        super(ADSocketConfig, self).ready()
        from . import adsocket
        if not self.adsocket_signals:
            return

        for s in self.adsocket_signals:
            if isinstance(s, str):
                klazz = import_module(s)
                if issubclass(klazz, (ADSocketCreator, ADSocketCreatorMeta)):
                    adsocket.register_creator(klazz)
                else:
                    raise NotImplemented()



