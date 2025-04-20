// public/js/custom_toolbar.js

if (frappe.boot) {
    override_toolbar();
} else {
    frappe.after_ajax(() => {
        override_toolbar();
    });
}

function override_toolbar() {
    class CustomToolbar extends frappe.ui.form.Toolbar {
        make_navigation() {
            super.make_navigation();
            const frm = this.frm;


            frappe.msgprint("hhh6")
            this.page.add_action_icon(
                "custom-whatsapp",
                
                () => {
                    new frappe.views.WhatsAppComposer({ frm });
                },
                
                __("Send Via WA")
            );
        }
    }

    frappe.ui.form.Toolbar = CustomToolbar;
}


// function override_query_report() {
//     class CustomQueryReport extends frappe.views.BaseList {
//         get_menu_items() {
//         let send_via_Wa={
// 				label: __("Send Via WA"),
// 				action: () =>{}
// 				// 	frappe.set_route("List", "Auto Email Report", { report: this.report_name }),
// 				// standard: true,
// 			}
//             super.get_menu_items().append(send_via_Wa);
            
//         }
//     }

    
// }
