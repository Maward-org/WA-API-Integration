# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_phone_number_with_country_code



class WAAccount(Document):
	
	@property
	def status(self):
		status = frappe.get_value("WA QR Details", {"wa_account": self.name}, "status")
		return status or ""
	
	@property
	def phone_number(self):
		num = frappe.get_value("WA QR Details", {"wa_account": self.name}, "phone_number")
		return num or ""


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
	def trigger_login_code_webhook(self,phone):
		doc = frappe.get_doc("WA QR Details", {"wa_account": self.name})
		doc.get_code = 1
		# doc.qr_updated = 0
		frappe.msgprint(phone)
		doc.phone_number=phone
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
			doc.qr_updated=0
			doc.save()

			return {"qr_link": doc.url}
		else:
			return {"qr_link": None}
		

	@frappe.whitelist()
	def get_latest_code(self):
		"""Fetch latest  code if updated, else return loading state."""
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
			doc.qr_updated=0
			doc.save()
			trimmed_code = doc.code.replace("-", "")
			return {"code": trimmed_code}
		else:
			return {"code": None}
		

	@frappe.whitelist()
	def update_status(self):
		
		doc = frappe.get_doc("WA QR Details", {"wa_account": self.name})

		doc.status_updated=0
		doc.save()
		doc.status_updated=1
		doc.save()
			
	
		
		
	

	# @frappe.whitelist()
	# def check_phone_validity(phone_number):
	# 	# try:
	# 	# 	frappe.msgprint(validate_phone_number_with_country_code(phone_number))
	# 	# 	return validate_phone_number_with_country_code(phone_number)  # Returns True if valid
	# 	# except Exception:
	# 	# 	return False  # Returns False if invalid
		
	# 	from phonenumbers import NumberParseException, is_valid_number, parse
	# 	from frappe import _
	# 	valid_number = False
	# 	error_message = _("Phone Number {0} set in field {1} is not valid.")
	# 	error_title = _("Invalid Phone Number")
		
		
	# 	try:
	# 		frappe.msgprint(is_valid_number(parse(phone_number)))
	# 		if valid_number := is_valid_number(parse(phone_number)):
	# 			return True
	# 	except NumberParseException as e:
	# 		pass
	# 	# 	if e.error_type == NumberParseException.INVALID_COUNTRY_CODE:
	# 	# 		error_message = _("Please select a country code for field {1}.")
	# 	# 		error_title = _("Country Code Required")
	# 	# finally:
	# 	# 	if not valid_number:
	# 	# 		frappe.throw(
	# 	# 			error_message.format(frappe.bold(phone_number), frappe.bold("Phone Number")),
	# 	# 			title=error_title,
	# 	# 			exc=frappe.InvalidPhoneNumberError,
	# 	# 		)

