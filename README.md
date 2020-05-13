# Slack notifications

## Installation

```bash
pip install slack-notifications
```


## Simple usage

```python
import os

import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


slack.send_notify('channel-name', username='Bot', text='@channel This is test message')
```


## Use attachments

```python
import os

import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


attachment = slack.Attachment(
    title='Attachment title',
    pretext='Attachment pretext',
    text='Attachment text',
    footer='Attachment footer',
    color='green',
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', attachments=[attachment])
```

See program API


## Attachment fields

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


attachment = slack.Attachment(
    title='Attachment title',
    pretext='Attachment pretext',
    text='Attachment text',
    footer='Attachment footer',
    fields=[
        Attachment.Field(
            title='Field title',
            value='Field value',
        ),
    ],
    color='green',
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', attachments=[attachment])
```


## Simple Text Block

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


block = slack.SimpleTextBlock(
    'Text example',
    fields=[
        SimpleTextBlock.Field(
            'Text field',
        ),
        SimpleTextBlock.Field(
            'Text field',
            emoji=True,
        ),
    ],
)

slack.send_notify('channel-name', username='Bot', text='@channel This is test message', blocks=[block])
```

See program API


## Init color

```python
import slack_notifications as slack


slack.init_color('green', '#008000')
```


## Call slack resource

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


response = slack.call_resource(slack.Resource('users.info', 'GET'), params={'user': 'W1234567890'})
```


## Resource iterator

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


for user in slack.resource_iterator(slack.Resource('users.list', 'GET'), 'members'):
    pass
```


## Raise exception if error was given

```python
import slack_notifications as slack


slack.ACCESS_TOKEN = 'xxx'


slack.send_notify('channel-name', username='Bot', text='@channel This is test message', raise_exc=True)
```


# Program API

## send_notify

* channel
* text: str = None
* username: str = None
* icon_url: str = None
* icon_emoji: str = None
* link_names: bool = True
* raise_exc: bool = False
* attachments: List[Attachment] = None
* blocks: List[BaseBlock] = None


## call_resource

* resource: Resource
* raise_exc: bool = False
* **kwargs (requests lib options)


## resource_iterator

* resource: Resource
* from_key: str
* cursor: str = None
* raise_exc: bool = False
* limit: int = DEFAULT_RECORDS_LIMIT


## init_color

* name: str
* code: str


## Attachment

* image_url: str = None,
* thumb_url: str = None,
* author_name: str = None,
* author_link: str = None,
* author_icon: str = None,
* title: str = None,
* title_link: str = None,
* text: str = None,
* pretext: str = None,
* footer: str = None,
* footer_icon: str = None,
* timestamp: str = None,
* fields: List[Attachment.Field] = None,
* color: str = None

### Attachment.Field

* title: str = None
* value: str = None
* short: bool = False


## SimpleTextBlock

* text: str
* mrkdwn: bool = True
* block_id: str = None
* fields: List[SimpleTextBlock.Field] = None

### SimpleTextBlock.Field

* text: str
* emoji: bool = False
* mrkdwn: bool = True


## DividerBlock

* block_id: str = None


## ImageBlock

* image_url: str
* title: str = None
* alt_text: str = None
* mrkdwn: bool = True
* block_id: str = None


## ContextBlock

* elements: List[Union[ContextBlock.TextElement, ContextBlock.ImageElement]]
* block_id: str = None

### ContextBlock.TextElement

* text: str
* mrkdwn: bool = True


### ContextBlock.ImageElement

* image_url: str
* alt_text: str = None
