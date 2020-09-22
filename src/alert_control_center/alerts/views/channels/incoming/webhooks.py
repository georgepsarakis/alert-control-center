import logging

from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from alert_control_center.utils.constants import API_ERROR_CODES
from alert_control_center.alerts.models import IncomingWebhook, \
    IncomingWebhookLog

from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers


class WebhookField(serializers.RelatedField):
    def to_representation(self, webhook: IncomingWebhook):
        return webhook.url


class IncomingWebhookLogSerializer(ModelSerializer):
    webhook = WebhookField(read_only=True)

    class Meta:
        model = IncomingWebhookLog
        fields = ['identifier', 'webhook', 'created_at']

logger = logging.getLogger(__name__)

JSON_GENERIC_ERROR_CODE = 1000


class JsonErrorResponse:
    def __init__(self, reason, code):
        self.reason = reason or 'Invalid data'
        self.code = code or JSON_GENERIC_ERROR_CODE

    def __call__(self, envelope):
        if not isinstance(envelope, (list, tuple)):
            envelope = [envelope]

        response = {}
        for envelope_level in envelope:
            response = response.setdefault(envelope_level, {})

        response['reason'] = self.reason
        response['code'] = self.code
        return response

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GenericAlertHook(View):
    def _get_webhook(self, url_token):
        return IncomingWebhook.objects.from_url(url_token)

    def post(self, *_, **kwargs):
        webhook = self._get_webhook(kwargs.get('token'))

        if webhook is None:
            response_data = \
                JsonErrorResponse(
                    reason='Invalid channel',
                    code=API_ERROR_CODES['INVALID_INCOMING_CHANNEL']
                )(['webhooks', 'incoming'])
            status_code = 404
        else:
            status_code = 200
            log = IncomingWebhookLog.objects.create(
                payload=self.request.body.decode('utf-8'),
                webhook=webhook
            )
            response_data = IncomingWebhookLogSerializer(log).data
            logger.info('Created log {}'.format(log.id))
        return JsonResponse(data=response_data, status=status_code)
