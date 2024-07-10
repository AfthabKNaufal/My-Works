import logging

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_multisafepay.controllers.main import (
    MultiSafePayController)


_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'multisafe':
            return res
        payload = self._multisafe_prepare_payment_request_payload()
        payment_data = self.provider_id._multisafepay_make_request(
            self.provider_id.multisafepay_api_key, payload=payload)
        self.provider_reference = payment_data.get('id')
        checkout_url = payment_data['data']['payment_url']
        parsed_url = urls.url_parse(checkout_url)
        url_params = urls.url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params}

    def _multisafe_prepare_payment_request_payload(self):
        first_name, last_name = payment_utils.split_partner_name(
            self.partner_name)
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url,
                                     MultiSafePayController._return_url)

        return {
            "type": "redirect",
            "order_id": self.id,
            "gateway": "",
            "currency": self.currency_id.name,
            "amount": self.amount*1000,
            "description": self._description,
            "payment_options": {
                "notification_url": "https://www.example.com/client/"
                                    "notification?type=notification",
                "notification_method": "POST",
                "redirect_url": f'{redirect_url}?ref={self.reference}',
                "cancel_url": "https://www.example.com/client/notification?"
                              "type=cancel",
                "close_window": True
            },
            "customer": {
                "locale": self.partner_lang,
                "ip_address": "123.123.123.123",
                "first_name": first_name,
                "last_name": last_name,
                "company_name": self.company_id.name,
                "address1": self.partner_address,
                "house_number": "39C",
                "zip_code": self.partner_zip,
                "city": self.partner_city,
                "country": self.partner_country_id.name,
                "phone": self.partner_phone,
                "email": self.partner_email,

            }
                }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'multisafe' or len(tx) == 1:
            return tx

        tx = self.search(
            [('reference', '=', notification_data.get('ref')),
             ('provider_code', '=', 'multisafe')]
        )
        if not tx:
            raise ValidationError("MultiSafePay: " + _(
                "No transaction found matching reference %s.",
                notification_data.get('ref')
            ))
        tx._process_notification_data(notification_data)
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafe':
            return

        payment_data = self.provider_id._multisafepay_make_request(
            self.provider_id.multisafepay_api_key, method="GET",
            payload=self._multisafe_prepare_payment_request_payload()
        )
        payment_status = payment_data['data']['status']
        if payment_status == 'pending':
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'completed':
            self._set_done()
        elif payment_status in ['expired', 'canceled', 'failed']:
            self._set_canceled(
                "MultisafePay: " + _("Canceled payment with status: %s",
                               payment_status))
        else:
            _logger.info(
                "received data with invalid payment status (%s) for "
                "transaction with reference %s",
                payment_status, self.reference
            )
            self._set_error(
                "MultiSafePay: " + _("Received data with invalid payment "
                                     "status: %s", payment_status)
            )
