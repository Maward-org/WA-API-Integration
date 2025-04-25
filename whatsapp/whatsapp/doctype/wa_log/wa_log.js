// Copyright (c) 2025, Yemen Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("WA Log", {
	refresh(frm) {
        if (frm.doc.failure_message) {  
            frm.trigger("failure_message");  // Trigger failure_message event

            
        }
        
	},
    failure_message(frm){
        frm.add_custom_button("Resend", function () {
            // Mark the document as dirty (modified)
            frm.dirty();
            
            frm.set_value("status", "Queued");

            // Save the document
            frm.save();
               
            // frappe.msgprint("Resending message...");
        });
    }
});
