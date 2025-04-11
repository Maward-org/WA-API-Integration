# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.file_manager import save_file


class WASetting(Document):
	



	@frappe.whitelist()
	def generate_and_save_salary_slips(self):
		if not self.hrms_sender:
			frappe.throw("Please Assign Sender Account.")
		employees = frappe.get_all("Employee", filters={"status": "Active"})
		frappe.msgprint(f"employees {employees}")

		for emp in employees:
			
			slip = frappe.get_all("Salary Slip", filters={"employee": emp.name}, order_by="posting_date desc", limit=1)
			# frappe.msgprint(f"slip{slip}")
			if not slip:
				continue

			slip_doc = frappe.get_doc("Salary Slip", slip[0].name)

			# Generate PDF
			pdf_data = frappe.get_print("Salary Slip", slip_doc.name, as_pdf=True)

			# Save PDF to File doctype, attach to Salary Slip or Employee
			filename = f"SalarySlip-{emp.name}-{slip_doc.posting_date}.pdf"
			file_doc = frappe.new_doc("File")
			file_doc.update({
				"file_name": filename,
				"is_private": 0,
				"content": pdf_data,
				"dt":"Salary Slip",
				"dn":slip_doc.name,
				"is_private":1
			})
			file_doc.save(ignore_permissions=True)
			
			
			frappe.msgprint(f"file_list {file_doc.name}")
			emp = frappe.get_doc("Employee", emp.name)
		# 	file_list = frappe.get_all("File", , limit=1)
		# 	if file_list:

			file= frappe.get_doc("File", file_doc.name)
		# 		frappe.msgprint(f"file{file}")
			if file_doc:	
				frappe.get_doc(
								{
									"doctype": "WA Log",
								
									"sender": self.hrms_sender,
									"receiver_id": emp.cell_number,
									"type": "Send File",
									"ref_doctype": "Salary Slip",
									"ref_document": slip_doc.name,
									
									
									"status":"Queued",
									"channel_type":"Direct",
									"file_reference":file_doc.file_url
									# "group_id":self.group_id

									
								}
							).insert() 

		# return "Salary slips generated and saved."
