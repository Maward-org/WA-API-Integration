// Copyright (c) 2025, Yemen Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("WA Setting", {
	refresh(frm) {

	},
    send_slips(frm){
        console.log("btn clicked")
        frappe.call({
            method: 'generate_and_save_salary_slips',
            doc: frm.doc,
            callback: function(r) {
                // frappe.msgprint(__('Salary Slips generated and saved.'));
            }
        });
    }
});
// frappe.ui.form.on('WA Setting', {
//     refresh(frm) {
//         frm.add_custom_button(__('Send Slips'), () => {
            
//         });
//     }
// });
