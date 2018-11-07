#! coding: utf-8

"""Handles interactions with Slack.
"""


import logging
import slackclient


class _SlackWriter(object):
    """Writes messages in a Slack channel.
    """

    def __init__(self, channel, username, token):
        self.channel = channel
        self.username = username

        self.client = slackclient.SlackClient(token)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _parameterize(self, text, extra_params):
        params = {
            'channel': self.channel,
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
            self.logger.error(err)

        if call is None:
            self.logger.error('API call could not be completed')
            return False

        response = call.get('ok')
        if response:
            self.logger.info('Text successfully written')
        else:
            api_err = call.get('error')
            self.logger.error(api_err)

        return response


class SlackNotifier(object):
    """Notifies success and error in slack channels.
    """

    def __init__(self, success_channel, error_channel, username, token):
        self.writer_success = _SlackWriter(success_channel, username, token)
        self.writer_error = _SlackWriter(error_channel, username, token)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _notify(self, message, extra_params=None, is_error=False):
        writer = self.writer_success
        if is_error:
            writer = self.writer_error

        return writer.write(message, extra_params)

    def notify_success(self, message, extra_params=None):
        return self._notify(message, extra_params)

    def notify_error(self, message, extra_params=None):
        return self._notify(message, extra_params, True)
