# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WAAccount(Document):
	
	@property
	def status(self):
		status = frappe.get_value("WA QR Details", {"wa_account": self.name}, "status")
		return status or ""


	def validate(self):
		if self.is_new():
			wa_details = frappe.get_doc({
			'doctype': 'WA QR Details',
			'wa_account': self.name,  
			
				})
		
			wa_details.insert()
			frappe.msgprint(f"Created WA QR Details for {self.name}")

		frappe.db.set_value("WA QR Details", {"wa_account": self.name}, "domain", self.domain)

	@frappe.whitelist()
	def trigger_login_webhook(self):
		doc = frappe.get_doc("WA QR Details", {"wa_account": self.name})
		doc.get_qr = 1
		doc.qr_updated = 0
		doc.save() 

	@frappe.whitelist()
	def trigger_logout_webhook(self):
	
		doc = frappe.get_doc("WA QR Details", {"wa_account": self.name})
		doc.logout = 1
		doc.save() 


	
	@frappe.whitelist()
	def get_latest_qr(self):
		"""Fetch latest QR code if updated, else return loading state."""
		doc = frappe.get_doc("WA QR Details", {"wa_account": self.name})
		# qr_updated=frappe.db.get_value(self.doctype, self.name, 'qr_updated')
		# frappe.msgprint(f"qr_updated: {qr_updated}")
		

		if doc.qr_updated:
			
			# frappe.msgprint(f"qr_updated: {doc.qr_updated}")
			# frappe.msgprint(f"qr_link: {doc.last_qr}")
			# self.get_qr = 0
			# self.qr_updated = 1
			# self.save(ignore_version=True)
			# last_qr=frappe.db.get_value(self.doctype, self.name, 'last_qr')

			return {"qr_link": doc.url}
		else:
			return {"qr_link": None}
