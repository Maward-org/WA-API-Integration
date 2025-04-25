// Copyright (c) 2025, Yemen Frappe and contributors
// For license information, please see license.txt

function generateRandomCode() {
    return "CH-" + Math.random().toString(36).substr(2, 8).toUpperCase(); 
}

frappe.ui.form.on("WA Channel", {
    refresh: function(frm) {
        if (!frm.doc.channel_id) { 
            frm.set_value("channel_id", generateRandomCode());
        }
        
        frappe.call({
            method: "get_user_type_options",
            doc:frm.doc,
            
            callback: function(child_response) {
                if (child_response.message) {
                    frm.fields_dict.members.grid.update_docfield_property(
                        "user_type", "options", child_response.message.join("\n")
                    );
                    frm.refresh_field("members");     
                }
            }
        });     
    },
	after_save(frm) {
    //     let creation_time = frm.doc.creation.split(".")[0];
    //     console.log("aftersave"+frappe.datetime.now_datetime()+"---"+creation_time)
    
            // console.log("new")

            
            frappe.call({
                method: "create_log",
                doc:frm.doc,
               
                callback: function(response) {

        }



    })

    
	}})

frappe.ui.form.on("WA Channel User", "user_type", function(frm, cdt, cdn) {
    // console.log("here")
    var item = locals[cdt][cdn];
    item.user = "";
    frm.refresh_field("members");
});
frappe.ui.form.on("WA Channel User", "user", function(frm, cdt, cdn) {
    var item = locals[cdt][cdn];  
    if (item.user_type) {  
        frappe.call({
            method: "get_user_type_phone",
            doc:frm.doc,
            
            args: { user_type: item.user_type,user:item.user },  
            callback: function(response) {
                if (response.message) {
                    frappe.model.set_value(cdt, cdn, "user_id", response.message); // Set the value
                } else {
                    frappe.model.set_value(cdt, cdn, "user_id", ""); // Clear if no match
                }
                frm.refresh_field("members");


            }})}

    // if (item.user_type == "Customer" && item.user) {
    //     frappe.db.get_value("Customer", item.user, "mobile_no")
    //         .then(r => {
    //             if (r.message && r.message.mobile_no) {
    //                 item.user_id = r.message.mobile_no;  // Assign inside the async callback
    //                 frm.refresh_field("members");  // Refresh child table to show the update
    //             }
    //         });
    // } else {
    //     item.user_id = "";  
    //     frm.refresh_field("members");
    // }
});
