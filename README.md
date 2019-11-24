# Slack notifications

## Installation

```bash
pip install slack-notifications
```

## Simple usage

```python
import os

from slack_notifications import send_notify


os.environ['SLACK_ACCESS_TOKEN'] = 'xxx'


send_notify('channel-name', username='Bot', text='@channel This is test message')
```


## Use attachments

```python
import os

from slack_notifications import send_notify, Attachment


os.environ['SLACK_ACCESS_TOKEN'] = 'xxx'


attachment = Attachment(
    title='Attachment title',
    pretext='Attachment pretext',
    text='Attachment text',
    footer='Attachment footer',
    color='green',
)

send_notify('channel-name', username='Bot', text='@channel This is test message', attachments=[attachment])
```


## Attachment fields

```python
import os

from slack_notifications import send_notify, Attachment, AttachmentField


os.environ['SLACK_ACCESS_TOKEN'] = 'xxx'


field = AttachmentField(
    title='Field title',
    value='Field value',
)

attachment = Attachment(
    title='Attachment title',
    pretext='Attachment pretext',
    text='Attachment text',
    footer='Attachment footer',
    fields=[field],
    color='green',
)

send_notify('channel-name', username='Bot', text='@channel This is test message', attachments=[attachment])
```

## Init attachment color

```python
from slack_notifications import init_color


init_color('green', '#008000')
```

## Call slack resource

```python
import os

from slack_notifications import call_resource, Resource


os.environ['SLACK_ACCESS_TOKEN'] = 'xxx'


response = call_resource(Resource('users.info', 'GET'), params={'user': 'W1234567890'})
```


## Resource iterator

```python
import os

from slack_notifications import resource_iterator, Resource


os.environ['SLACK_ACCESS_TOKEN'] = 'xxx'


for user in resource_iterator(Resource('users.list', 'GET'), 'members'):
    pass
```

## Raise exception if error was given

```python
import os

from slack_notifications import send_notify


os.environ['SLACK_ACCESS_TOKEN'] = 'xxx'


send_notify('channel-name', username='Bot', text='@channel This is test message', raise_exc=True)
```


# Objects

## AttachmentField

* title=None
* value=None
* short=False

## Attachment

* image_url=None,
* thumb_url=None,
* author_name=None,
* author_link=None,
* author_icon=None,
* title=None,
* title_link=None,
* text=None,
* pretext=None,
* footer=None,
* footer_icon=None,
* timestamp=None,
* fields: List[AttachmentField] = None,
* color=None
