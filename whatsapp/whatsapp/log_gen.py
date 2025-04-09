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

