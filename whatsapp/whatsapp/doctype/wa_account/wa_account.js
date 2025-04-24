

frappe.ui.form.on('WA Account', {
    refresh: function(frm) {
        toggle_btn(frm)
        // update_status(frm)
        if (frm.doc.domain) { 
            frm.add_custom_button('Refresh Status', function() {
                update_status(frm)

            } )  
            }

       

},
    status:function(frm){
        toggle_btn(frm)

    },



});

function toggle_btn(frm) {
    


    
        frm.page.clear_secondary_action();
        frm.page.clear_inner_toolbar();

        if (!frm.is_new()) { 
            if (frm.doc.status == "Connected") { 
                frm.add_custom_button('Logout', function() {                
                    frappe.call({
                        method: "create_account_log",
                        doc:frm.doc,
                        args:{                 
                            type:"Logout"
                        },
                        freeze: true,
                        freeze_message: "جاري تسجيل الخروج..", 
                    });
                    
                }).addClass('btn-primary');
                frm.add_custom_button('Sync Groups', function(){
                    
                    frappe.call({
                        method: "create_account_log",
                        doc:frm.doc,
                        args:{
                              
                            type:"Sync Groups"
                        },
                        })
                    
            })
            } else if (frm.doc.status == "Disconnected") { 
                frm.add_custom_button('Get QR Code', function() {
                    // console.log("hereee ")
                        frappe.call({
                            method: "create_account_log",
                            doc:frm.doc,
                            args:{
                              
                                type:"Login QR"
                            },
                           
                            callback: function(response) {
                                console.log("hereee")
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
                                        update_status(frm)
                                    }
                                });
                            
                                d.show();
                                function fetchQRCode(retries = 10, delay = 2000) {
                                    console.log("fetchQRCode")
                                    if (retries <= 0) {
                                        frappe.msgprint("QR Code update timeout. Please try again.");
                                        return;
                                    }
                            
                                    frappe.call({
                                        method: "get_latest_code",
                                        doc:frm.doc,
                                       
                                        callback: function(response) {
                                            let qr_link = response.message.code;
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
                        
                      
                    
                      
               
                    


                    
                },__("Login")).addClass('btn-primary');

                frm.add_custom_button('Get Direct Code', function() {

                    let d = new frappe.ui.Dialog({
                        title: 'Login Through Code',
                        fields: [
                            {
                                label:'Phone Number',
                                fieldname: 'phone_number',
                                fieldtype: 'Phone',
                                reqd: 1,
                                default:frm.doc.phone_number
                            },
                            {
                                fieldname: 'code_html',
                                fieldtype: 'HTML',
                                options: `<div style="text-align:center; font-family: Arial, sans-serif; padding: 20px;">
                                    <p style="color: #333;"> Waiting for code...</p>
                                    
                                  
                                    
                                    
                                </div>`
                            }
                        ],
                        primary_action_label: 'Done',
                        primary_action: function() {
                            d.hide();
                            update_status(frm)
                        },
                        secondary_action_label: 'Get Code',
                        secondary_action: function() {
                            let values = d.get_values();
                            // if (validate_phone(values.phone_number)) {
                            //    console.log("valiiid")
                            //     return;
                            // }
                            // frappe.msgprint(__('Code Sent!'));
                            console.log(values.phone_number)
                            frappe.call({
                                method: "create_account_log",
                                doc:frm.doc,
                                args:{
                                    phone:values.phone_number,
                                    type:"Login Code"
                                },
                               
                                callback: function(response) {
                                    function fetchCode(retries = 10, delay = 2000) {
                                        console.log("fetchCode")
                                        if (retries <= 0) {
                                            frappe.msgprint("Code fetch timeout. Please try again.");
                                            return;
                                        }
                                
                                        frappe.call({
                                            method: "get_latest_code",
                                            doc:frm.doc,
                                           
                                            callback: function(response) {
                                                let code = response.message.code;
                                                console.log("response.message.code"+code)
                        
                                                
                                                if (code) {
                                                    d.fields_dict.code_html.$wrapper.html(`<div style="text-align:center; font-family: Arial, sans-serif; padding: 20px;">
                                                        <h3 style="color: #333;">Enter the Code</h3>
                                                        <p style="color: #777;">Go to Linked Devices \u279C Link with Phone Number Instead </p>
                                                        <p style="color: #777;">Then Enter the following code </p>
                                                        <div style="display: flex; justify-content: center; gap: 8px; margin-top: 10px;">
                                                            <input type="text" id="code1" maxlength="1" class="otp-box" readonly>
                                                            <input type="text" id="code2" maxlength="1" class="otp-box" readonly>
                                                            <input type="text" id="code3" maxlength="1" class="otp-box" readonly>
                                                            <input type="text" id="code4" maxlength="1" class="otp-box" readonly>
                                                            <span style="font-size: 20px; font-weight: bold;">-</span>
                                                            <input type="text" id="code5" maxlength="1" class="otp-box" readonly>
                                                            <input type="text" id="code6" maxlength="1" class="otp-box" readonly>
                                                            <input type="text" id="code7" maxlength="1" class="otp-box" readonly>
                                                            <input type="text" id="code8" maxlength="1" class="otp-box" readonly>
                                                        </div>
                                                        <style>
                                                            .otp-box {
                                                                width: 40px;
                                                                height: 40px;
                                                                font-size: 20px;
                                                                text-align: center;
                                                                border: 2px solid #ccc;
                                                                border-radius: 5px;
                                                                outline: none;
                                                            }
                                                            .otp-box:focus {
                                                                border-color: #007bff;
                                                                box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
                                                            }
                                                        </style>
                                                    </div>`);
                                                    var cleanedCode = code.replace(/-/g, "");


                                                    for (let i = 0; i < cleanedCode.length && i < 8; i++) {
                                                        
                                                        document.getElementById(`code${i + 1}`).value = cleanedCode[i];
                                                    }
                                                } else {
                                                    // Keep polling every 2 seconds
                                                    setTimeout(() => fetchCode(retries - 1, delay), delay);
                                                }
                                            }
                                        });
                                    }
                                    fetchCode(); 
                                
                                }});
                        },
                        primary_action: function() {
                            // let values = d.get_values();
                            // if (validate_phone(values.phone_number)) {
                                
                                
                            // }
                            
                            d.hide();
                        }
                    });
                    
                    d.show();
                    
                    // Disable "Get Code" initially
                    // d.get_secondary_action_button().prop('disabled', true);
                    
                    // Validate phone number and enable/disable "Get Code"
                    // d.fields_dict.phone_number.$wrapper.find('input').on('input', function() {
                    //     let phoneValue = $(this).val().trim();
                    //     d.get_secondary_action_button().prop('disabled', !validate_phone(phoneValue));
                    // });
                    
                    // Function to validate phone number using Frappe utils
                    function validate_phone(phone, callback) {
                        frappe.call({
                            method: 'check_phone_validity',
                             doc:frm.doc,
                            args: { phone_number: phone },
                            callback: function(response) {
                                console.log(response.message)
                                return(response.message);
                            }
                        });
                    }
                    d.show();
          
           

                
                  
           
                


                
            },__("Login"));
            }
        }


}
function update_status(frm){
    console.log("btn")

    if (!frm.is_new()) { 
    frappe.call({   
        method: "create_account_log",
        doc:frm.doc,
        args:{
              
            type:"Update Account Status"
        },
        freeze: true,
        freeze_message: "جاري..",
        callback: function(response) {
            frappe.msgprint("Please Wait")
           
            setTimeout(function() {
                location.reload(); 
            }, 3000); 
    
    
    }
    },
    )}}