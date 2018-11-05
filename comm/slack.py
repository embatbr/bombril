#! coding: utf-8

"""Sends messages to Slack.
"""


import logging
import slackclient


class SlackNotifier(object):

    def __init__(self, success_channel_id, error_channel_id, username, token):
        self.success_channel_id = success_channel_id
        self.error_channel_id = error_channel_id
        self.username = username

        self.client = slackclient.SlackClient(token)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def notify(self, message, extra_params=None):
        params = {
            'channel': self.success_channel_id,
            'username': self.username,
            'text': message
        }

        if extra_params and isinstance(extra_params, dict):
            params.update(extra_params)

        call = None
        try:
            call = self.client.api_call('chat.postMessage', **params)
        except Exception as err:
            self.logger.error(err)

        if call is None:
            self.logger.error('API call could not be completed')
            return False

        response = call.get('ok')
        if response:
            self.logger.info('Notification successfully sent')
        else:
            api_err = call.get('error')
            self.logger.error(api_err)

        return response

    def notify_error(self, message):
        extra_params = {
            'channel': self.error_channel_id
        }

        return self.notify(message, extra_params)
