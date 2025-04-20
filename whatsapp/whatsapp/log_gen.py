import frappe
# from date import now

def apply(doc, state):
        
        
  
    
 
    
        rules = frappe.get_list(
                "WA Automation Rule",
                filters={"enabled": 1, "document_type": doc.doctype},
                
        )
        
        if not rules:
                return
        for rule in rules:

                rule = frappe.get_doc("WA Automation Rule", rule.name)  # Fetch full rule doc
                # frappe.msgprint(f"rule {rule}")
                

                
                sender = rule.sending_account
                receiver = doc.get(rule.recipient_phone_field)

                if not sender:
                        frappe.msgprint(f"⚠️ Warning: Sending account field '{rule.sending_account}' is missing in {doc.name}")
                        return  # Avoid creating an incomplete log

                if rule.channel_type=="Direct" and not receiver:
                        frappe.msgprint(f"⚠️ Warning: Recipient phone field '{rule.recipient_phone_field}' is missing in {doc.name}")
                        return
                
                if rule.channel_type=="Group" and not rule.group_id:
                        frappe.msgprint(f"⚠️ Warning: Group ID  is missing in {rule.name}")
                        return
                
                rule.send(doc)



@frappe.whitelist()
def process_whatsapp_pop_up(data,doctype,doc):
        import json

        if isinstance(data, str):
            data = json.loads(data)
        
        # #fecth needed info


        # sender = frappe.db.get_single_value('WA Setting', 'hrms_sender')

        module = frappe.get_meta("Salary Slip").module


        doc = frappe.get_single("WA Setting") 
        account=""
        for row in doc.account_module_settings:
                if row.module ==module:
                        account= row.sending_account 

        
        if not account:
                frappe.throw(f"Account is not set for module{module} in WA Setting")

        

        to = data.get("receiver")
        msg = data.get("message")
        is_attach_print=data.get("attach_document_print")
        send_copy=data.get("send_copy")
        doc_details = frappe.get_doc(doctype, doc)
        lang=data.get("print_language")
        attachments = data.get("checked_attachments") or []
        sender_doc=frappe.get_doc("WA Account",account)
        # frappe.msgprint(len(attachments))

        # frappe.msgprint(f"doc: {to}")
                
       
        # frappe.msgprint(f"is_attach_print {is_attach_print}")

        
        # Generate PDF
        if is_attach_print:
                if lang:
                       frappe.local.lang = lang
                frappe.local.site = frappe.local.site or frappe.get_site_path()
                frappe.local.signed_query_string = True

                
                
                print_foramt=data.get("print_format")
                pdf_data = frappe.get_print(
                        doctype=doctype,
                        print_format=print_foramt,
                        # lang=lang,
                        as_pdf=True,
                        doc=doc_details
                        )


                filename = f"SalarySlip-{doc}-{doc_details.creation}.pdf"
                file_doc = frappe.new_doc("File")
                file_doc.update({
                        "file_name": filename,
                        "is_private": 0,
                        "content": pdf_data,
                        "dt":"Salary Slip",
                        "dn":doc,
                        "is_private":1
                })
                file_doc.save(ignore_permissions=True)
                # frappe.msgprint(f"{len(data.get("checked_attachments"))}")
                
#                 frappe.msgprint("jere")
                if file_doc:	
                        attachments.append(file_doc.file_url)
                # print("Attachmentsss:", attachments)

                # frappe.msgprint(", ".join(attachments))

        for attach in attachments:
                frappe.msgprint(f"loop{to}")
                # Generate Log
                generate_log(account,to,"Send Attach","Salary Slip",doc,"Direct",msg,attach)
                
                
                if send_copy:
                        #get sending account phone num
                        
                        #Generate Log
                        generate_log(account,sender_doc.device_id.split(':')[0],"Send Attach","Salary Slip",doc,"Direct",msg,attach)

                        
def generate_log(sender,reciever,type,doctype,ref_doc,channel_type,content,url=None):
             if url and "http" in url:
                     url = url[url.find("/private"):]
                     
            
                

             frappe.get_doc(
                        {
                                "doctype": "WA Log",
                        
                                "sender": sender,
                                "receiver_id": reciever,
                                "type": type,
                                "ref_doctype": doctype,
                                "ref_document": ref_doc,
                               
                                
                                "status":"Queued",
                                "channel_type":channel_type,
                                "file_reference":url,
                                "content":content
                                # "group_id":self.group_id

                                
                        }
                ).insert() 
                

# return "Salary slips generated and saved."
