
frappe.views.WhatsAppComposer = class {
	constructor(opts) {
		$.extend(this, opts);
		this.frm = opts.frm;
		this.doc = this.frm?.doc || {};
		this.make();
	}

	make() {
		const me = this;
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Print Format",
				filters: { doc_type: this.frm.doctype },
				fields: ["name"],
				limit_page_length: 100,
			},
			callback(r) {
				const formats = (r.message || []).map((f) => f.name);
				

				me.dialog = new frappe.ui.Dialog({
					title: __("Send WhatsApp"),
					fields: [
						
						{
							label: __("To"),
							fieldtype: "Link",
							reqd: 0,
							fieldname: "receiver",
							options: "Contact",
							reqd: 1,
							get_query: () => {
								return {
									filters: [
										["custom_wa_number", "!=", ""]
										
									]
								};
							}
						},
						
						
					
						{
							label: "Message",
							fieldname: "message",
							fieldtype: "Small Text",
							reqd: 1,
						},
						{ fieldtype: "Section Break" },
						{
							label: "Send me a copy",
							fieldname: "send_copy",
							fieldtype: "Check",
							default: 0,
						},
						{
							label: "Attach Document Print",
							fieldtype: "Check",
							fieldname: "attach_document_print",
							default: 1,
						},
						{
							label: "Print Format",
							fieldtype: "Select",
							fieldname: "print_format",
							options: formats,
							default:formats[0],
							depends_on: "attach_document_print",
						},
						{
							label: "Print Language",
							fieldtype: "Link",
							options: "Language",
							fieldname: "print_language",
							default: frappe.boot.lang,
							depends_on: "attach_document_print",
							
							
						},
						
						{ fieldtype: "Column Break" },
						{
							label: "Select Attachments",
							fieldtype: "HTML",
							fieldname: "select_attachments",
						},
					],
					primary_action_label: __("Send"),
					primary_action(values) {
						if(values.attach_document_print){
							if(values.print_format==""|| values.print_language==""){
								frappe.throw("Print Fromat & Langauage shoul be specified")
							}
						}
						console.log("💬 WhatsApp Payload:", values);
                        let checked_attachmentss = [];
							
					document.querySelectorAll('.attachment-checkbox:checked').forEach(function(checkbox) {
						const fileUrl = checkbox.getAttribute('data-file-url');
						checked_attachmentss.push(fileUrl);
						
					});
                        
                        values.checked_attachments = checked_attachmentss;
                      
                        checked_attachmentss = [];
                       




						frappe.call({
							method: "whatsapp.whatsapp.log_gen.process_whatsapp_pop_up",
							args: {
								data: values,
								doctype: me.frm.doc.doctype,
								doc: me.frm.doc.name,
                                
							},
							callback() {
                                
								
								me.dialog.hide();
								
							},
						});
					},
				});

				me.dialog.show();
				me.dialog.onhide = () => {
					//delete form DOM
					me.dialog.$wrapper.remove(); 
				};
				me.setup_attach();
			},
		});
	}


	setup_attach() {
		const fields = this.dialog.fields_dict;
		const attach = $(fields.select_attachments.wrapper);
		if (!this.attachments) this.attachments = [];

		const args = {
			doctype: this.frm.doctype,
			docname: this.frm.docname,
			folder: "Home/Attachments",
			on_success: (attachment) => {
				this.frm.attachments.attachment_uploaded(attachment);
				this.render_attachment_rows(attachment);
			},
		};

		$(` 
			<label class="control-label">${__("Select Attachments")}</label>
			<div class='attach-list'></div>
			<p class='add-more-attachments'>
				<button class='btn btn-xs btn-default'>
					${frappe.utils.icon("small-add", "xs")}&nbsp;
					${__("Add Attachment")}
				</button>
			</p>
		`).appendTo(attach.empty());

		attach.find(".add-more-attachments button")
			.on("click", () => new frappe.ui.FileUploader(args));

		this.render_attachment_rows();
	}

	render_attachment_rows(attachment) {
		const field = this.dialog.fields_dict.select_attachments;
		const attachment_rows = $(field.wrapper).find(".attach-list");
		let files = attachment ? [attachment] : this.frm.get_files();

		files.forEach((f) => {
			if (!attachment_rows.find(`[data-file-name="${f.name}"]`).length) {
				f.file_url = frappe.urllib.get_full_url(f.file_url);
				attachment_rows.append(this.get_attachment_row(f));
			}
		});
	}

	get_attachment_row(file) {
		return $(`<p class="checkbox flex" data-file-name="${file.name}">
			<label title="${file.file_name}" style="max-width: 100%">
				<input type="checkbox" class="attachment-checkbox" data-file-url="${file.file_url}">
				<span class="ellipsis" style="max-width: calc(100% - 90px)">
					${file.file_name}
				</span>
				<a href="${file.file_url}" target="_blank" class="btn-link" style="padding-left: 5px">
					${frappe.utils.icon("link-url", "sm")}
				</a>
			</label>
		</p>`);
	}
};
