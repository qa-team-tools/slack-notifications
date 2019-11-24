# -*- coding: utf8 -*-

import os
from typing import List

import requests


ACCESS_TOKEN_ENV_NAME = 'SLACK_ACCESS_TOKEN'

SLACK_API_URL = 'https://slack.com/api'
ACCESS_TOKEN = os.getenv(ACCESS_TOKEN_ENV_NAME)

DEFAULT_RECORDS_LIMIT = 100
DEFAULT_REQUEST_TIMEOUT = 180

COLOR_MAP = {
    'green': '#008000',
    'gray': '#808080',
    'red': '#FF0000',
    'blue': '#0000FF',
    'black': '#000000',
    'yellow': '#FFFF00',
    'maroon': '#800000',
    'purple': '#800080',
    'olive': '#808000',
    'silver': '#C0C0C0',
    'gold': '#FFD700',
    'pink': '#FFC0CB',
    'coral': '#FF7F50',
    'brown': '#A52A2A',
    'indigo': '#4B0082',
    'aqua': '#00FFFF',
    'cyan': '#00FFFF',
    'lime': '#00FF00',
    'teal': '#008080',
    'navy': '#000080',
    'sienna': '#A0522D',
}


class SlackError(requests.exceptions.RequestException):
    pass


class Resource:

    def __init__(self, handle, method):
        self.handle = handle
        self.method = method


class AttachmentField:

    def __init__(self, *, title=None, value=None, short=False):
        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):
        assert self.title is not None and self.value is not None, 'Title or value is required for attachment field'

        data = {'short': self.short}

        if self.title:
            data['title'] = self.title

        if self.value:
            data['value'] = self.value

        return data


class Attachment:

    def __init__(self, *,
                 image_url=None,
                 thumb_url=None,
                 author_name=None,
                 author_link=None,
                 author_icon=None,
                 title=None,
                 title_link=None,
                 text=None,
                 pretext=None,
                 footer=None,
                 footer_icon=None,
                 timestamp=None,
                 fields: List[AttachmentField] = None,
                 color=None):
        self.image_url = image_url
        self.thumb_url = thumb_url

        self.author_name = author_name
        self.author_link = author_link
        self.author_icon = author_icon

        self.title = title
        self.title_link = title_link

        self.text = text

        self.pretext = pretext

        self.footer = footer
        self.footer_icon = footer_icon

        self.timestamp = timestamp

        self.fields = fields

        self.color = color

    def to_dict(self):
        default_color = COLOR_MAP['gray']
        data = {
            'mrkdwn_in': [],
        }

        if self.color:
            data['color'] = COLOR_MAP.get(self.color, default_color)

        if self.image_url:
            data['image_url'] = self.image_url

        if self.thumb_url:
            data['thumb_url'] = self.thumb_url

        if self.author_name:
            data['author_name'] = self.author_name

        if self.author_link:
            data['author_link'] = self.author_link

        if self.author_icon:
            data['author_icon'] = self.author_icon

        if self.title:
            data['title'] = self.title

        if self.title_link:
            data['title_link'] = self.title_link

        if self.pretext:
            data['pretext'] = self.pretext
            data['mrkdwn_in'].append('pretext')

        if self.text:
            data['text'] = self.text
            data['mrkdwn_in'].append('text')

        if self.footer:
            data['footer'] = self.footer
            data['mrkdwn_in'].append('footer')

        if self.footer_icon:
            data['footer_icon'] = self.footer_icon

        if self.timestamp:
            data['ts'] = self.timestamp

        if self.fields:
            data['fields'] = [f.to_dict() for f in self.fields]

        return data


def init_color(name, code):
    COLOR_MAP[name] = code


def call_resource(resource: Resource, *, raise_exc=False, **kwargs):
    assert ACCESS_TOKEN is not None, f'Please export "{ACCESS_TOKEN_ENV_NAME}" environment variable'

    kwargs.setdefault('timeout', DEFAULT_REQUEST_TIMEOUT)

    url = f'{SLACK_API_URL}/{resource.handle}'

    kwargs['headers'] = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json; charset=utf-8',
    }

    response = requests.request(resource.method, url, **kwargs)

    if raise_exc:
        response.raise_for_status()

        json = response.json()

        if not json['ok']:
            raise SlackError(response=response)

    return response


def resource_iterator(resource: Resource, from_key: str, *, limit=DEFAULT_RECORDS_LIMIT, cursor=None):
    params = {'limit': limit}

    if cursor:
        params['cursor'] = cursor

    response = call_resource(resource, params=params)
    data = response.json()

    for item in data[from_key]:
        yield item

    cursor = data.get('response_metadata', {}).get('next_cursor')

    if cursor:
        yield from resource_iterator(resource, from_key, limit=limit, cursor=cursor)


def send_notify(channel, *,
                text: str = None,
                username: str = None,
                raise_exc: bool = False,
                attachments: List[Attachment] = None):
    data = {
        'channel': channel,
        'link_names': True,
    }

    if username:
        data['as_user'] = False
        data['username'] = username
    else:
        data['as_user'] = True

    if text:
        data['mrkdwn'] = True
        data['text'] = text

    if attachments:
        data['attachments'] = [a.to_dict() for a in attachments]

    return call_resource(Resource('chat.postMessage', 'POST'), raise_exc=raise_exc, json=data)
