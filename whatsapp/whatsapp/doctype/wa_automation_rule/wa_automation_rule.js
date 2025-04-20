// Copyright (c) 2025, Yemen Frappe and contributors
// For license information, please see license.txt

// frappe.ui.form.on("WA Automation Rule", {
// 	refresh(frm) {

// 	},
// });



frappe.wa_auto_rule = {
	setup_fieldname_select: function (frm) {
       
		// get the doctype to update fields
        console.log("here"+frm.doc.document_type)
		if (!frm.doc.document_type) {
			return;
		}
       

		frappe.model.with_doctype(frm.doc.document_type, function () {
			let get_select_options = function (df, parent_field) {
				// Append parent_field name along with fieldname for child table fields
				let select_value = parent_field ? df.fieldname + "," + parent_field : df.fieldname;

                    return {
                        value: select_value,
                        label: df.fieldname + " (" + (df.label) + ")",
                    };
			};

			let get_img_field_options = function (df, parent_field) {
				let file_options = $.map(fields, function (d) {
					return d.fieldtype == "Attach Image" 
						? get_select_options(d)
						: null;
				});
				// console.log("file_options"+file_options)
				return file_options
			};
			let get_file_field_options = function (df, parent_field) {
				let file_options = $.map(fields, function (d) {
					return d.fieldtype == "Attach" 
						? get_select_options(d)
						: null;
				});
				// console.log("file_options"+file_options)
				return file_options
			};
            // console.log("get_select_options:"+get_select_options)

			let get_date_change_options = function () {
				let date_options = $.map(fields, function (d) {
					return d.fieldtype == "Date" || d.fieldtype == "Datetime"
						? get_select_options(d)
						: null;
				});

                // console.log("date_options:"+date_options)

				// append creation and modified date to Date Change field
				return date_options.concat([
					{ value: "creation", label: `creation (${__("Created On")})` },
					{ value: "modified", label: `modified (${__("Last Modified Date")})` },
				]);
			};
            let get_phone_reciepient_options = function () {
				let phone_options = $.map(fields, function (d) {
					return ((d.fieldtype == "Data" && d.options=="Phone") || d.fieldtype == "Phone")
						? get_select_options(d)
						: null;
				});
                console.log("date_options:"+phone_options)

				// append creation and modified date to Date Change field
				return phone_options
			};

			let get_data_options = function () {
				let data_options = $.map(fields, function (d) {
					return d.fieldtype == "Data" 
						? get_select_options(d)
						: null;
				});
                // console.log("date_options:"+date_options)

				// append creation and modified date to Date Change field
				return data_options
			};

			let get_link_options = function () {
				let data_options = $.map(fields, function (d) {
					return d.fieldtype == "Link" 
						? get_select_options(d)
						: null;
				});
                // console.log("date_options:"+date_options)

				// append creation and modified date to Date Change field
				return data_options
			};


			let fields = frappe.get_doc("DocType", frm.doc.document_type).fields;
			let options = $.map(fields, function (d) {
				return in_list(frappe.model.no_value_type, d.fieldtype)
					? null
					: get_select_options(d);
			});

			// set value changed options
			frm.set_df_property("value_changed", "options", [""].concat(options));
			// frm.set_df_property("set_property_after_alert", "options", [""].concat(options));
			if(frm.doc.action_type=="Send Image"){
				frm.set_df_property("file_field", "options", get_img_field_options());
			}
			else{
				frm.set_df_property("file_field", "options", get_file_field_options());
			}

			

			

			// set date changed options
			frm.set_df_property("date_changed", "options", get_date_change_options());

			// set date phone reciepient options
            frm.set_df_property("recipient_phone_field", "options", get_phone_reciepient_options());

			// frm.set_df_property("", "options", get_data_options());
			frm.fields_dict["group_members"].grid.update_docfield_property(
				"member_id", "options",  get_phone_reciepient_options()
			);
			frm.set_df_property("group_name_reference", "options", get_data_options());

		// 	let receiver_fields = [];
		// 	if (frm.doc.channel === "Email") {
		// 		receiver_fields = $.map(fields, function (d) {
		// 			// Add User and Email fields from child into select dropdown
		// 			if (frappe.model.table_fields.includes(d.fieldtype)) {
		// 				let child_fields = frappe.get_doc("DocType", d.options).fields;
		// 				return $.map(child_fields, function (df) {
		// 					return df.options == "Email" ||
		// 						(df.options == "User" && df.fieldtype == "Link")
		// 						? get_select_options(df, d.fieldname)
		// 						: null;
		// 				});
		// 				// Add User and Email fields from parent into select dropdown
		// 			} else {
		// 				return d.options == "Email" ||
		// 					(d.options == "User" && d.fieldtype == "Link")
		// 					? get_select_options(d)
		// 					: null;
		// 			}
		// 		});
		// 	} else if (in_list(["WhatsApp", "SMS"], frm.doc.channel)) {
		// 		receiver_fields = $.map(fields, function (d) {
		// 			return d.options == "Phone" ? get_select_options(d) : null;
		// 		});
		// 	}

		// 	// set email recipient options
		// 	frm.fields_dict.recipients.grid.update_docfield_property(
		// 		"receiver_by_document_field",
		// 		"options",
		// 		[""].concat(["owner"]).concat(receiver_fields)
		// 	);
		// });
	},)},

	}




frappe.ui.form.on("WA Automation Rule", {
	
	onload: function (frm) {
		console.log("onload")

		
		frm.set_query("document_type", function () {
			return {
				filters: {
					istable: 0,
				},
			};
		});
		
	},
	refresh: function (frm) {
		frappe.wa_auto_rule.setup_fieldname_select(frm);
		frm.trigger('action_type');
		frm.trigger('channel_type');
		
		
		
	
		// frm.trigger("event");
	},
	document_type: function (frm) {
		frappe.wa_auto_rule.setup_fieldname_select(frm);
	},
	action_type: function (frm) {
	
		frappe.wa_auto_rule.setup_fieldname_select(frm);
		let action = frm.doc.action_type || "";
	
			let isSendAction = action.includes("Send");
			let isCreateGroup = action === "Create Group";
			
			let isUser = action.includes("User");
			let isNamed =( isUser ||frm.doc.channel_type === "Group");
			let isGroup =action.includes("Group");
			let test=isUser || isGroup
			console.log(isSendAction,isCreateGroup,isUser,isGroup,test)
	
			frm.set_df_property("message_content", "hidden", !isSendAction);
			frm.set_df_property("group_name_reference", "hidden", !isCreateGroup);
			frm.set_df_property("group_members", "hidden",!test);
			frm.set_df_property("group", "hidden", !isUser);
			frm.set_df_property("group_name", "hidden", !isNamed);
		
	},
	channel_type(frm){
		frm.trigger('action_type');
		let new_options = [];
		let updated_options=[];
		if (frm.fields_dict.action_type.df.options)
		{let current_options = frm.fields_dict.action_type.df.options.split("\n");



		if (frm.doc.channel_type === "Group") {
			// console.log("here")
			new_options = ["Create Group", "Add User", "Remove User", "Promote User", "Demote User"];
		}
		else{
			current_options=["","Send Message","Send Image","Send File"]
		}
		updated_options = [...new Set([...current_options, ...new_options])];
		}
		else{
			updated_options=["","Send Message","Send Image","Send File"]
		}

	
		frm.set_df_property("action_type", "options", updated_options.join("\n")); 
	}
	// view_properties: function (frm) {
	// 	frappe.route_options = { doc_type: frm.doc.document_type };
	// 	frappe.set_route("Form", "Customize Form");
	// },
	// event: function (frm) {
	// 	if (in_list(["Days Before", "Days After"], frm.doc.event)) {
	// 		frm.add_custom_button(__("Get Alerts for Today"), function () {
	// 			frappe.call({
	// 				method: "frappe.email.doctype.notification.notification.get_documents_for_today",
	// 				args: {
	// 					notification: frm.doc.name,
	// 				},
	// 				callback: function (r) {
	// 					if (r.message && r.message.length > 0) {
	// 						frappe.msgprint(r.message.toString());
	// 					} else {
	// 						frappe.msgprint(__("No alerts for today"));
	// 					}
	// 				},
	// 			});
	// 		});
	// 	}
	// },
	// channel: function (frm) {
	// 	frm.toggle_reqd("recipients", frm.doc.channel == "Email");
	// 	frappe.notification.setup_fieldname_select(frm);
	// 	frappe.notification.setup_example_message(frm);
	// 	if (frm.doc.channel === "SMS" && frm.doc.__islocal) {
	// 		frm.set_df_property(
	// 			"channel",
	// 			"description",
	// 			`To use SMS Channel, initialize <a href="/app/sms-settings">SMS Settings</a>.`
	// 		);
	// 	} else {
	// 		frm.set_df_property("channel", "description", ` `);
	// 	}
	// },
});

