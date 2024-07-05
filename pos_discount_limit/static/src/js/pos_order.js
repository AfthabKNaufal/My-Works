/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(Order.prototype, {
    async pay() {
        var total_discount = 0
        var taxes_prod = 0
        console.log(this)
        this.orderlines.map(obj =>{
            if (this.pos.config.iface_tax_included === "total"){
                obj.product.taxes_id.map(key=>{
                    taxes_prod += (eval(obj.price * (this.pos.taxes[key-1].amount/100)))
                })
                total_discount += ((taxes_prod + obj.price)*obj.discount/100)
            }
            else{
                total_discount += eval(obj.price*(obj.discount/100))
            }
        })
        if (total_discount > this.pos.pos_session.discount_limit) {
             this.env.services.popup.add(ErrorPopup, {
                    title: _t("Discount Limit has been Reached!"),
                    body: _t("Your remaining balance is %s, you can extend your limit from your settings",this.pos.pos_session.discount_limit),
                });
             return false
        }
        this.pos.pos_session.balance = total_discount
        super.pay()
    }
});