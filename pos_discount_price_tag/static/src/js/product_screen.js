/** @odoo-module */
import { Pos } from "@point_of_sale/app/generic_components/product_card/product_card";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype,{
    setup(){
     super.setup();
     console.log(this)
    },
    DiscountTagAvailable(product_id){
        if (this.pos.db.product_by_id[this.props.productId].discount_tag_id){
            return (this.pos.db.product_by_id[this.props.productId].discount_tag_id[1])
        }
    }

});
