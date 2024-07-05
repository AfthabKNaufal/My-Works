/** @odoo-module */
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { jsonrpc } from "@web/core/network/rpc_service";
import { useService } from "@web/core/utils/hooks";


patch(PaymentScreen.prototype, {
    setup() {
        this.rpc = useService("orm");
        super.setup();
    },
    async validateOrder(isForceValidate) {
        this.pos.pos_session.discount_limit -= this.pos.pos_session.balance
        await this.orm.call("pos.session", "update_limit", [[this.pos_session_id]], {
            value: this.pos.pos_session.discount_limit,
            session_id : this.pos.pos_session.id
        });
        await super.validateOrder(...arguments);
    },
});
