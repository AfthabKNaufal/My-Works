/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment} from "@web/core/utils/render";
export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var uniq=0

PublicWidget.registry.TableColumnValueSnippet = PublicWidget.Widget.extend({
    selector: '.ref-arrival-content',
    willStart: async function(){
        var self = this
        this.data = await jsonrpc('/new_created_machines',{})
        console.log(this.data)

    },

    start: function(){
        const relEl = this.$el.find('#new_machines_carousel')
        var chunkdata = chunk(this.data,4)
        chunkdata[0].is_active = true
        uniq+=1
        relEl.html(renderToFragment('machine_management.new_machine_snippet_carousel',{'chunkdata':chunkdata,
        'uniq':uniq}))
    }
});
