# Adsocket transport

## Install

``` bash
pip install adsocket-transport-django
```

## Usage

Using django.db.singals is very easy...

```python
from django.apps import AppConfig
from adsocket_transport_django.apps import ADSocketConfig


class VideosConfig(ADSocketConfig, AppConfig):
    """
    Basic application config
    """
    name = "myapp"
    verbose_name = "My App"

    adsocket_signals = [
        'myapp.ws_message_creator.VideoMessageCreator'

    ]
```

```python
from adsocket_transport_django.creator import ADSocketCreator
from adsocket_transport_django import CREATE, UPDATE, DELETE, Message

from myapp import models


class VideoMessageCreator(ADSocketCreator):

    class Meta:
        model = models.Todo

    def create(self, model):
        return Message(
            type='publish',
            channel=f'todos:{model.pk}',
            data={'obj': model.pk, 'action': 'create'}
        )

    def update(self, model):
        return Message(
            type='publish',
            channel=f'todos:{model.pk}',
            data={'obj': model.pk, 'action': 'update'}
        )

    def delete(self, model):
        return Message(
            type='publish',
            channel=f'todos:{model.pk}',
            data={'obj': model.pk, 'action': 'delete'}
        )

```
