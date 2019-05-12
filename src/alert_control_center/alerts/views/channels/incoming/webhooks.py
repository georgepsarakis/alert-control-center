from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from alert_control_center.utils.constants import API_ERROR_CODES
from alert_control_center.alerts.models import IncomingWebhook


class GenericAlertHook(View):
    def _get_webhook(self, url_token):


    def post(self, *args, **kwargs):
        token = kwargs.get('token')
        if token is None:
            response_data = {
                'webhooks': {
                    'incoming': {
                        'error': 'Invalid channel ID',
                        'error_id':
                            API_ERROR_CODES['INVALID_INCOMING_CHANNEL']
                    }
                }
            }
            status_code = 404
        else:
            response_data = {
                'accepted': token,
                'time': timezone.now()
            }
            status_code = 200
        return JsonResponse(data=response_data, status=status_code)
