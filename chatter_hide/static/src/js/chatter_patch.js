import { Chatter } from "@mail/chatter/web_portal/chatter";
import { patch } from "@web/core/utils/patch";

patch(Chatter.prototype, {
    setup() {
        super.setup();
    },
    onClickToggle(){
        const chatterEl = document.querySelectorAll(".o-mail-Chatter")
        const formrender = document.querySelectorAll(".o_form_renderer")
        const formrender_bg = document.querySelectorAll(".o_form_sheet_bg")
        console.log('askfh',formrender_bg)
        if (chatterEl) {
              chatterEl.forEach((el) => {
                    if (el.classList.contains("d-none")) {
                        el.classList.remove("d-none");
                        formrender[0].classList.add('d-flex')
                        formrender_bg[0].classList.remove('d-contents')
                    } else {
                        el.classList.add("d-none");
                        formrender[0].classList.remove('d-flex')
                        formrender_bg[0].classList.add('d-contents')
                    }
                });
        }
    }
});