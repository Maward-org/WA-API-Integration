frappe.views.ReportWhatsAppComposer = class {
	constructor(opts) {
		this.report = opts.report;
		this.report_name = this.report.report_name || "Report";
		this.data = this.report.data || [];
		this.make();
	}

	make() {
		console.log("000")
		this.dialog = new frappe.ui.Dialog({
			title: __("Send WhatsApp (Repor)"),
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
					fieldtype: "Check",
					fieldname: "with_letter_head",
									
				},
				{
					label: "Letter head",
					fieldtype: "Link",
					fieldname: "letter_head",
					options:"Letter Head",
					
					depends_on: "with_letter_head",
				},
				{
					label: "Orientation",
					fieldtype: "Select",
					fieldname: "orientation",
					options:["Landscape","Portrait"],
					default:"Landscape",
					reqd: 1,
				},
				
			],
			primary_action_label: __("Send"),
			primary_action: (values) => {
				// frappe.msgprint("sent7")
				console.log(this.report.data)
				values.is_report = true;
				values.report_name=this.report_name,
				values.data = this.report.data;  
				values.columns=this.report.columns;
				values.doctype=this.report.doctype;
				// frappe.render_grid({
				// 	template: print_settings.columns ? "print_grid" : custom_format,
				// 	title: __(this.report_name),
				// 	subtitle: filters_html,
				// 	print_settings: print_settings,
				// 	landscape: landscape,
				// 	// filters: this.get_filter_values(),
				// 	data: this.report.data,
				// 	columns: this.report.columns,
				// 	original_data: this.data,
				// 	report: this,
				// 	can_use_smaller_font: this.report.is_standard === "Yes" && custom_format ? 0 : 1,
				// });
				const content = frappe.render_template("print_grid", {
					title: "My Report Title",
					subtitle:"",
					columns: this.report.columns,
					data: this.report.data,
					original_data: this.report.data,
					landscape: true,
					can_use_smaller_font: true,
					report: this.report,
				});
				const full_html = frappe.render_template("print_template", {
					title: this.report.doctype,
					content: content,
					base_url: frappe.urllib.get_base_url(),
					print_css: frappe.boot.print_css,
					lang: frappe.boot.lang,
					layout_direction: frappe.utils.is_rtl() ? "rtl" : "ltr",
					landscape: true,
					columns: this.report.columns,
					can_use_smaller_font: true,
					print_settings: {
						letter_head: {
							header: "<p>Letterhead</p>",
							footer: "<p>Footer</p>"
						},
						repeat_header_footer: 1
					}
				});
				
				console.log("html"+full_html)
				values.html=full_html;
				
				frappe.call({
					method: "whatsapp.whatsapp.log_gen.process_report_whatsapp_pop_up",
					args: {
						data:values
					},
					callback: function(r) {
						me.dialog.hide();
						
					}
				});
				
				// console.log("value"+value)
				// let dialog = frappe.ui.get_print_settings(
				// 	false,
				// 	(print_settings) => this.print_report(print_settings),
				// 	this.report.letter_head,
				// 	this.report.columns
				// );
				// this.add_portrait_warning(dialog);

			},
		});

		this.dialog.show();
	}
	print_report(print_settings) {
		const custom_format =  null;//
		const filters_html = null;//
		const landscape = print_settings.orientation == "Landscape";

		// this.make_access_log("Print", "PDF");
		frappe.render_grid({
			template: print_settings.columns ? "print_grid" : custom_format,
			title: __(this.report_name),
			subtitle: filters_html,
			print_settings: print_settings,
			landscape: landscape,
			// filters: this.get_filter_values(),
			data: this.report.data,
			columns: this.report.columns,
			original_data: this.data,
			report: this,
			can_use_smaller_font: this.report.is_standard === "Yes" && custom_format ? 0 : 1,
		});
	}
	add_portrait_warning(dialog) {
		if (this.report.columns.length > 10) {
			dialog.set_df_property("orientation", "change", () => {
				let value = dialog.get_value("orientation");
				let description =
					value === "Portrait"
						? __("Report with more than 10 columns looks better in Landscape mode.")
						: "";
				dialog.set_df_property("orientation", "description", description);
			});
		}
	}

	
};
