# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WAAccount(Document):
	@frappe.whitelist()
	def trigger_webhook(self):
		# pass
		# frappe.db.set_value(self.doctype, self.name, 'get_qr', 1, update_modified=False)
		# frappe.db.set_value(self.doctype, self.name, 'qr_updated', 0, update_modified=False)
		# doc = frappe.get_doc("WA QR Details", self.name)
		doc = frappe.get_doc("WA QR Details", {"wa_account": self.name})



		
		doc.get_qr = 1
		doc.qr_updated = 0
		doc.save()  # Ignores version conflicts
		# frappe.db.commit()


	
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
