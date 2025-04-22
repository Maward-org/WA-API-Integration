frappe.views.ReportWhatsAppComposer = class {
	constructor(opts) {
		this.report = opts.report;
		this.report_name = this.report.report_name || "Report";
		this.data = this.report.data || [];
		this.make();
	}

	make() {
		this.dialog = new frappe.ui.Dialog({
			title: __("Send WhatsApp (Report)"),
			fields: [
				{
					label: __("To"),
					fieldtype: "Link",
					fieldname: "receiver",
					options: "Contact",
					reqd: 1,
					get_query: () => ({
						filters: [["custom_wa_number", "!=", ""]],
					}),
				},
				{
					label: __("Message"),
					fieldtype: "Small Text",
					fieldname: "message",
					reqd: 1,
				},
                {
                    label: "Send me a copy",
                    fieldname: "send_copy",
                    fieldtype: "Check",
                    default: 0,
                },
				{
                    label: "With Letter head",
                    fieldtype: "check",
                    fieldname: "with_letter_head",
                    
                    default:0,
                    
                },
                {
                    label: "Letter head",
                    fieldtype: "link",
                    fieldname: "letter_head",
                    options:"Letter Head",
                    
                    depends_on: "with_letter_head",
                },
                {
                    label: "Orientation",
                    fieldtype: "select",
                    fieldname: "orientation",
                    options:["Landscape","Portrait"]
                },
			],
			primary_action_label: __("Send"),
			primary_action: (values) => {
                values.is_report = true;
				frappe.call({
                    method: "whatsapp.whatsapp.log_gen.process_whatsapp_pop_up",
                    args: {
                        data: values,
                       
                        
                    },
                    callback() {
                        
                        
                        me.dialog.hide();
                        
                    },
                });
			},
		});

		this.dialog.show();
        me.dialog.onhide = () => {
            //delete form DOM
            me.dialog.$wrapper.remove(); 
        };
	}

	// send_whatsapp(values) {
	// 	const payload = {
	// 		receiver: values.receiver,
	// 		message: values.message,
	// 		attach_csv: values.attach_csv,
	// 		report_name: this.report_name,
	// 		filters: this.report.get_filter_values(),
	// 	};

	// 	frappe.call({
	// 		method: "whatsapp.whatsapp.report_whatsapp.send_report_via_whatsapp",
	// 		args: { data: payload },
	// 		callback: () => {
	// 			this.dialog.hide();
	// 			frappe.msgprint(__("WhatsApp sent successfully"));
	// 		},
	// 	});
	// }
};
