// frappe.ui.form.on('WA Account', {
//     refresh: function(frm) {
//         frm.add_custom_button('Get QR Code', function() {
//             //to trigger the webhoook
//             frm.set_value("get_qr",0)
//             frm.set_value("get_qr",1)
//             frm.refresh_field("last_qr");
//             frm.refresh_field("get_qr");
            
           

//             frm.save()

//             let d = new frappe.ui.Dialog({
//                 title: 'Scan WhatsApp QR Code',
//                 fields: [
//                     {
//                         fieldname: 'qr_code_html',
//                         fieldtype: 'HTML',
//                         options: `<div style="text-align:center;">
                           
//                             <p>Waiting for QR code...</p>
//                         </div>`
//                     }
//                 ],
//                 primary_action_label: 'Done',
//                 primary_action: function() {
//                     d.hide();
//                 }
//             });
        
//             d.show();
        
//             function fetchQRCode(retries = 5, delay = 2000) {
//                 console.log("fetchQRCode")
//                 if (retries <= 0) {
//                     frappe.msgprint("QR Code update timeout. Please try again.");
//                     return;
//                 }
        
//                 frappe.call({
//                     method: "get_latest_qr",
//                     doc:frm.doc,
                   
//                     callback: function(response) {
//                         let qr_link = response.message.qr_link;
//                         console.log("response.message.qr_link"+qr_link)

//                         frm.refresh_field("last_qr");
//                         frm.refresh_field("get_qr");
//                         frm.refresh_field("qr_updated");
//                         if (qr_link) {
//                             // Update the QR code in the dialog
//                             d.fields_dict.qr_code_html.$wrapper.html(`
//                                 <div style="text-align:center;">
//                                     <img id="qr_image" src="${qr_link}" alt="WhatsApp QR Code"
//                                     style="max-width: 300px; border: 1px solid #ddd; padding: 10px;"/>
//                                     <p>Scan this QR code to link your WhatsApp account.</p>
//                                 </div>
//                             `);
//                         } else {
//                             // Keep polling every 2 seconds
//                             setTimeout(() => fetchQRCode(retries - 1, delay), delay);
//                         }
//                     }
//                 });
//             }
        
//             fetchQRCode(); // Start polling for QR update
//         }).addClass('btn-primary');
        
//     }



// frappe.ui.form.on('WA Account', {
//     refresh: function(frm) {
//         frm.add_custom_button('Get QR Code', function() {
          
           

//             frappe.call({
//                 method: "trigger_webhook",
//                 doc:frm.doc,
               
//                 callback: function(response) {

//                     // let qr_link = response.message.qr_link;
//                     console.log("webhook triggered")
//                     //show dailog
//                     let d = new frappe.ui.Dialog({
//                         title: 'Scan WhatsApp QR Code',
//                         fields: [
//                             {
//                                 fieldname: 'qr_code_html',
//                                 fieldtype: 'HTML',
//                                 options: `<div style="text-align:center;">
                                   
//                                     <p>Waiting for QR code...</p>
//                                 </div>`
//                             }
//                         ],
//                         primary_action_label: 'Done',
//                         primary_action: function() {
//                             d.hide();
//                         }
//                     });
                
//                     d.show();
//                     function fetchQRCode(retries = 5, delay = 2000) {
//                         console.log("fetchQRCode")
//                         if (retries <= 0) {
//                             frappe.msgprint("QR Code update timeout. Please try again.");
//                             return;
//                         }
                
//                         frappe.call({
//                             method: "get_latest_qr",
//                             doc:frm.doc,
                           
//                             callback: function(response) {
//                                 let qr_link = response.message.qr_link;
//                                 console.log("response.message.qr_link"+qr_link)
        
//                                 frm.refresh_field("last_qr");
//                                 frm.refresh_field("get_qr");
//                                 frm.refresh_field("qr_updated");
//                                 if (qr_link) {
//                                     // Update the QR code in the dialog
//                                     d.fields_dict.qr_code_html.$wrapper.html(`
//                                         <div style="text-align:center;">
//                                             <img id="qr_image" src="${qr_link}" alt="WhatsApp QR Code"
//                                             style="max-width: 300px; border: 1px solid #ddd; padding: 10px;"/>
//                                             <p>Scan this QR code to link your WhatsApp account.</p>
//                                         </div>
//                                     `);
//                                 } else {
//                                     // Keep polling every 2 seconds
//                                     setTimeout(() => fetchQRCode(retries - 1, delay), delay);
//                                 }
//                             }
//                         });
//                     }
                
//                     fetchQRCode(); // Start polling for QR update

                    
//                 }
//             });
            
          
        
//             function fetchQRCode(retries = 5, delay = 2000) {
//                 console.log("fetchQRCode")
//                 if (retries <= 0) {
//                     frappe.msgprint("QR Code update timeout. Please try again.");
//                     return;
//                 }
        
//                 frappe.call({
//                     method: "get_latest_qr",
//                     doc:frm.doc,
                   
//                     callback: function(response) {
//                         let qr_link = response.message.qr_link;
//                         console.log("response.message.qr_link"+qr_link)

//                         frm.refresh_field("last_qr");
//                         frm.refresh_field("get_qr");
//                         frm.refresh_field("qr_updated");
//                         if (qr_link) {
//                             // Update the QR code in the dialog
//                             d.fields_dict.qr_code_html.$wrapper.html(`
//                                 <div style="text-align:center;">
//                                     <img id="qr_image" src="${qr_link}" alt="WhatsApp QR Code"
//                                     style="max-width: 300px; border: 1px solid #ddd; padding: 10px;"/>
//                                     <p>Scan this QR code to link your WhatsApp account.</p>
//                                 </div>
//                             `);
//                         } else {
//                             // Keep polling every 2 seconds
//                             setTimeout(() => fetchQRCode(retries - 1, delay), delay);
//                         }
//                     }
//                 });
//             }
        
//            // Start polling for QR update
//         }).addClass('btn-primary');
        
//     }
// });


frappe.ui.form.on('WA Account', {
    refresh: function(frm) {
        frm.add_custom_button('Get QR Code', function() {
          
           

            frappe.call({
                method: "trigger_webhook",
                doc:frm.doc,
               
                callback: function(response) {
                    // frm.refresh_field("last_qr");
                    // frm.refresh_field("get_qr");
                    // frm.refresh_field("qr_updated");

                    // let qr_link = response.message.qr_link;
                    console.log("webhook triggered")
                    //show dailog
                    let d = new frappe.ui.Dialog({
                        title: 'Scan WhatsApp QR Code',
                        fields: [
                            {
                                fieldname: 'qr_code_html',
                                fieldtype: 'HTML',
                                options: `<div style="text-align:center;">
                                   
                                    <p>Waiting for QR code...</p>
                                </div>`
                            }
                        ],
                        primary_action_label: 'Done',
                        primary_action: function() {
                            d.hide();
                        }
                    });
                
                    d.show();
                    function fetchQRCode(retries = 5, delay = 2000) {
                        console.log("fetchQRCode")
                        if (retries <= 0) {
                            frappe.msgprint("QR Code update timeout. Please try again.");
                            return;
                        }
                
                        frappe.call({
                            method: "get_latest_qr",
                            doc:frm.doc,
                           
                            callback: function(response) {
                                let qr_link = response.message.qr_link;
                                console.log("response.message.qr_link"+qr_link)
        
                                frm.refresh_field("last_qr");
                                frm.refresh_field("get_qr");
                                frm.refresh_field("qr_updated");
                                if (qr_link) {
                                    // Update the QR code in the dialog
                                    d.fields_dict.qr_code_html.$wrapper.html(`
                                        <div style="text-align:center;">
                                            <img id="qr_image" src="${qr_link}" alt="WhatsApp QR Code"
                                            style="max-width: 300px; border: 1px solid #ddd; padding: 10px;"/>
                                            <p>Scan this QR code to link your WhatsApp account.</p>
                                            <p>Refresh the code every 30 seconds</p>
                                        </div>
                                    `);
                                } else {
                                    // Keep polling every 2 seconds
                                    setTimeout(() => fetchQRCode(retries - 1, delay), delay);
                                }
                            }
                        });
                    }
                
                    fetchQRCode(); // Start polling for QR update

                    
                }
            });
            
          
        
            function fetchQRCode(retries = 5, delay = 2000) {
                console.log("fetchQRCode")
                if (retries <= 0) {
                    frappe.msgprint("QR Code update timeout. Please try again.");
                    return;
                }
        
                frappe.call({
                    method: "get_latest_qr",
                    doc:frm.doc,
                   
                    callback: function(response) {
                        let qr_link = response.message.qr_link;
                        console.log("response.message.qr_link"+qr_link)

                        frm.refresh_field("last_qr");
                        frm.refresh_field("get_qr");
                        frm.refresh_field("qr_updated");
                        if (qr_link) {
                            // Update the QR code in the dialog
                            d.fields_dict.qr_code_html.$wrapper.html(`
                                <div style="text-align:center;">
                                    <img id="qr_image" src="${qr_link}" alt="WhatsApp QR Code"
                                    style="max-width: 300px; border: 1px solid #ddd; padding: 10px;"/>
                                    <p>Scan this QR code to link your WhatsApp account.</p>
                                </div>
                            `);
                        } else {
                            // Keep polling every 2 seconds
                            setTimeout(() => fetchQRCode(retries - 1, delay), delay);
                        }
                    }
                });
            }
        
           // Start polling for QR update
        }).addClass('btn-primary');
        
    }
});

