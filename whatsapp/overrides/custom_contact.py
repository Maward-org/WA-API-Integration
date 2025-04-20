import frappe
from frappe.contacts.doctype.contact.contact import Contact

class CustomContact(Contact):
    def validate(self):
    
        super().validate()
        # frappe.msgprint("www")
        
        for num in self.phone_nos:
            if num.custom_is_whatsapp:
                self.custom_wa_number=num.phone
            
