#! coding: utf-8

"""Handles interactions with Slack.
"""


import slackclient


class SlackChannel(object):
    """Writes messages in a Slack channel.
    """

    def __init__(self, name, _id, username, token):
        self.name = name
        self.id = _id
        self.username = username

        self.client = slackclient.SlackClient(token)

    def _parameterize(self, text, extra_params):
        params = {
            'channel': self.id,
            'username': self.username,
            'text': text
        }

        if extra_params and isinstance(extra_params, dict):
            params.update(extra_params)

        return params

    def write(self, text, extra_params=None):
        call = None
        try:
            params = self._parameterize(text, extra_params)
            call = self.client.api_call('chat.postMessage', **params)
        except Exception as err:
            pass

        if call is None:
            return False

        response = call.get('ok')
        if response:
        else:
            api_err = call.get('error')

        return response


class SlackNotifier(object):
    """Notifies channels.
    """

    def __init__(self, channels_info, username, token):
        self.channels = dict()
        for channel_info in channels_info:
            name = channel_info['name']
            self.channels[name] = SlackChannel(name, channel_info['id'], username, token)

    def notify(self, channel_name, message, extra_params=None):
        return self.channels[channel_name].write(message, extra_params)

    def notify_channels(self, channels_names, messages):
        ret = dict()

        for (channel_name, message) in zip(channels_names, messages):
            ret[channel_name] = self.notify(channel_name, message)

        return ret

    def notify_all(self, message, extra_params=None):
        ret = dict()

        for channel_name in self.channels.keys():
            ret[channel_name] = self.channels[channel_name].write(message, extra_params)

        return ret
