import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MultiSafePayController(http.Controller):
    _return_url = '/payment/multisafe/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'],
        csrf=False,
        save_session=False
    )
    def multisafe_return_from_checkout(self, **data):

        _logger.info("handling redirection from multisafe with data:\n%s",
                     pprint.pformat(data))
        request.env['payment.transaction'].sudo()._handle_notification_data(
            'multisafe', data)
        return request.redirect('/payment/status')
