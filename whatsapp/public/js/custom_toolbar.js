// public/js/custom_toolbar.js

if (frappe.boot) {
    override_toolbar();
    override_report_view();
} else {
    frappe.after_ajax(() => {
        override_toolbar();
        override_report_view();
    });
}

function override_toolbar() {
    class CustomToolbar extends frappe.ui.form.Toolbar {
        make_navigation() {
            super.make_navigation();
            const frm = this.frm;


            // frappe.msgprint("hhh6")
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

function override_report_view(){
    console.log("override_report_view")
	// Wait for Frappe to be fully loaded
	const ReportView = frappe.views.ReportView;

	if (!ReportView) return;

	const original = ReportView.prototype.report_menu_items;

	ReportView.prototype.report_menu_items = function () {
		// Call original method to get default menu items
		let items = original.call(this);
        const frm = this.frm;


		// Add your custom item
        console.log("pp")
		items.push({
			label: __("Send Via WhatsApp"),
			action: () => {
                new frappe.views.ReportWhatsAppComposer({ report: this });
				
			},
		});

		return items;
	};
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
