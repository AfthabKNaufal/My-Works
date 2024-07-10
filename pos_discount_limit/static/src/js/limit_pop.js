/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { _t } from "@web/core/l10n/translation";
import { useState } from "@odoo/owl";

export class limitpopup extends TextAreaPopup{
    static template = "point_of-sale.limitpop";
    static defaultProps = {
        confirmText: _t("Confirm"),
        cancelText: _t("Discard"),
        title: "",
        body: "",
    };
    setup(){
    this.state = useState({otp:"1111"})
    console.log(this.state)
    }
    async getPayload() {
        return this.state.otp;
    }

}