/** @odoo-module */
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    export_for_printing(){
        const result = super.export_for_printing(...arguments);
        var order_line = this.orderlines
        for (var i=0;i<order_line.length;i++){
            result.orderlines[i].discount_tag_id = order_line[i].product.discount_tag_id
        }
        return result
    }
});