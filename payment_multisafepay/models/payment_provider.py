
import requests
import logging
import pprint

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


from odoo.addons.payment_multisafepay import const

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(selection_add=[('multisafe', 'Multi Safe')],
                            ondelete={'multisafe': 'set default'})

    multisafepay_api_key = fields.Char('MultiSafepay test api key',
                                       size=40)

    @api.model
    def _get_compatible_providers(self, *args, is_validation=False, **kwargs):
        providers = super()._get_compatible_providers(
            *args, is_validation=is_validation, **kwargs)
        if is_validation:
            providers = providers.filtered(lambda p: p.code != 'multisafe')
        return providers

    @api.onchange('multisafepay_api_key')
    def _onchange_multisafepay_api_key(self):
        if self.multisafepay_api_key and len(
                self.multisafepay_api_key) != 40:
            raise UserError('An API key must be 40 characters long')

    @api.constrains('state', 'code')
    def _check_provider_state(self):
        if self.filtered(lambda p: p.code == 'multisafe' and p.state not in (
        'test', 'disabled')):
            raise UserError(_("Multi Safe Pay providers should "
                              "never be enabled."))

    def _get_default_payment_method_codes(self):
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'multisafe':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES

    def _multisafepay_make_request(self, endpoint, payload, method='POST'):
        order = payload['order_id']
        self.ensure_one()
        url = (f'https://testapi.multisafepay.com/v1/json/orders?api_key='
               f'{endpoint}')
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
                }
        try:
            if method == 'GET':
                url = (f'https://testapi.multisafepay.com/v1/json/orders/'
                       f'{order}?api_key={endpoint}')
                headers = {"Accept": "application/json"}
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, json=payload, headers=headers,
                                         timeout=10)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Invalid API request at %s with data:\n%s", url,
                    pprint.pformat(payload),
                )
                raise ValidationError("MultiSafePay: " + _(
                    "The communication with the API failed. Multisafepay "
                    "gave us the following "
                    "information: '%s'", response.json().get('message', '')
                ))
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "MultiSafePay: " + _(
                    "Could not establish the connection to the API.")
            )
        return response.json()
