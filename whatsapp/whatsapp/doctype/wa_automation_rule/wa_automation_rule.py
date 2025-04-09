# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_to_date,nowdate


class WAAutomationRule(Document):
	
	
# 	def get_documents_for_today(self):
# 		"""get list of documents that will be triggered today"""
# 		docs = []

# 		diff_days = self.days_in_advance
# 		if self.event == "Days After":
# 			diff_days = -diff_days

# 		reference_date = add_to_date(nowdate(), days=diff_days)
# 		reference_date_start = reference_date + " 00:00:00.000000"
# 		reference_date_end = reference_date + " 23:59:59.000000"

# 		doc_list = frappe.get_all(
# 			self.document_type,
# 			fields="name",
# 			filters=[
# 				{self.date_changed: (">=", reference_date_start)},
# 				{self.date_changed: ("<=", reference_date_end)},
# 			],
# 		)

# 		for d in doc_list:
# 			doc = frappe.get_doc(self.document_type, d.name)

# 			if self.condition and not frappe.safe_eval(self.condition, None, get_context(doc)):
# 				continue

# 			docs.append(doc)

# 		return docs

	def send(self, doc):
		if self.rule_condition_satisfied(doc):
			

			if self.event=="Submit" or self.event=="Cancel":
				# frappe.msgprint(frappe.utils.now())
				exists = frappe.db.exists(
				"WA Log",
				{
				"ref_document": doc.name,
				"repeat_solve": self.event  ,



				},
				)
				# frappe.msgprint(f"exist{exists}")
				if exists:
						return
			if self.action_type=="Create Group":
				self.create_group(doc)
			elif "User" in self.action_type:
				self.edit_group(doc)
			else:
				self.create_log(doc)
			
	def create_log(self,doc):
		doc = frappe.get_doc(
						{
							"doctype": "WA Log",
						
							"sender": self.sending_account,
							"receiver_id": doc.get(self.recipient_phone_field) if self.channel_type=="Direct" else self.group_id+"@g.us" ,
							"type": self.action_type,
							"ref_doctype": doc.doctype,
							"ref_document": doc.name,
							"wa_automation_rule": self.name,
							**({"repeat_solve": self.event} if self.event in ["Submit", "Cancel"] else {}),
							"status":"Queued",
							"channel_type":self.channel_type,
							"file_reference":doc.get(self.file_field) if self.file_field else ""
							# "group_id":self.group_id

							
						}
					).insert() 
					
	def create_group(self,doc):
		channel = frappe.get_doc(
						{
							"doctype": "WA Channel",
						
							"channel_creator": self.sending_account,
							"channel_name": doc.get(self.group_name_reference),
							"type": "Group",
							"members": [] 
							
							
						}
					)
		
		for member in self.group_members:  
			# frappe.msgprint(f"user id{doc.get(member.member_id)}")
			channel.append("members", { 
				"user_id": doc.get(member.member_id), 
				"is_admin": member.is_admin
			}) 
		channel.insert()
		new_doc = frappe.get_doc("WA Channel",channel.name )
		new_doc.create_log()
		# frappe.db.commit()
					
	
					
	def edit_group(self,doc):
		channel = frappe.get_doc("WA Channel", self.group_name)
		# frappe.msgprint(self.group_name)

		# Append new member to the child table
		

		if self.action_type=="Add User":
			for member in self.group_members: 
				channel.append("members", {
				"user_id": doc.get(member.member_id),
				"is_admin":  member.is_admin
				})
			# frappe.msgprint("tt") 
		elif self.action_type=="Remove User":
			users_to_remove = [doc.get(member.member_id) for member in self.group_members]

			# Filter out existing members that match the IDs to remove
			channel.members = [
				member for member in channel.members
				if member.user_id not in users_to_remove
			]
				
		elif self.action_type=="Promote User":
			users_to_promote = [doc.get(member.member_id) for member in self.group_members]
			for member in channel.members:
				if member.user_id in users_to_promote:
					member.is_admin = True  

		elif self.action_type=="Demote User":
			users_to_promote = [doc.get(member.member_id) for member in self.group_members]
			for member in channel.members:
				if member.user_id in users_to_promote:
					member.is_admin = False  

					
				
			
		# channel.run_method("validate")
		channel.save()
		channel.sync_members_with_whatsapp()
		
	

	def validate_condition(self, doc):
			return self.condition and frappe.safe_eval(self.condition, None, {"doc": doc.as_dict()})
# 	def validate(self):
		

# 		# validate_template(self.message)

# 		if self.event in ("Days Before", "Days After") and not self.date_changed:
# 			frappe.throw(_("Please specify which date field must be checked"))

# 		if self.event == "Value Change" and not self.value_changed:
# 			frappe.throw(_("Please specify which value field must be checked"))

		
# 		self.validate_condition()


# @frappe.whitelist()
# def get_documents_for_today(notification):
# 	notification = frappe.get_doc("Notification", notification)
# 	notification.check_permission("read")
# 	return [d.name for d in notification.get_documents_for_today()]

	def rule_condition_satisfied(self, doc):
		if self.condition:
			if not self.validate_condition(doc):
				return False

		if self.event == "New":
			# indicates that this was a new doc

			return doc.get_doc_before_save() is None
		if self.event == "Submit":
			return doc.docstatus.is_submitted()
		if self.event == "Cancel":
			return doc.docstatus.is_cancelled()
		if self.event == "Value Change":
			field_to_check = self.value_changed
			if not field_to_check:
				return False
			doc_before_save = doc.get_doc_before_save()
			# check if the field has been changوو
			# if condition is set check if it is satisfied
			return (
				doc_before_save
				and doc_before_save.get(field_to_check) != doc.get(field_to_check)
				and (not self.condition or self.validate_condition(doc))
			)

		if self.event in ["Custom", "Save"]:
			doc_before_save = doc.get_doc_before_save()
			if not doc_before_save:
				return True  # If no previous version, treat it as valid

			# Ignore changes in docstatus
			if doc_before_save.docstatus != doc.docstatus:
				return False

			return True

		return False


# def trigger_notifications(doc, method=None):
# 	if frappe.flags.in_import or frappe.flags.in_patch:
# 		# don't send notifications while syncing or patching
# 		return

# 	if method == "daily":
# 		doc_list = frappe.get_all(
# 			"Notification", filters={"event": ("in", ("Days Before", "Days After")), "enabled": 1}
# 		)
# 		for d in doc_list:
# 			alert = frappe.get_doc("Notification", d.name)

# 			for doc in alert.get_documents_for_today():
# 				evaluate_alert(doc, alert, alert.event)
# 				frappe.db.commit()


# def evaluate_alert(doc: Document, alert, event):
# 	from jinja2 import TemplateError

# 	try:
# 		if isinstance(alert, str):
# 			alert = frappe.get_doc("Notification", alert)

# 		context = get_context(doc)

# 		if alert.condition:
# 			if not frappe.safe_eval(alert.condition, None, context):
# 				return

# 		if event == "Value Change" and not doc.is_new():
# 			if not frappe.db.has_column(doc.doctype, alert.value_changed):
# 				alert.db_set("enabled", 0)
# 				alert.log_error(f"Notification {alert.name} has been disabled due to missing field")
# 				return

# 			doc_before_save = doc.get_doc_before_save()
# 			field_value_before_save = doc_before_save.get(alert.value_changed) if doc_before_save else None

# 			fieldtype = doc.meta.get_field(alert.value_changed).fieldtype
# 			if cast(fieldtype, doc.get(alert.value_changed)) == cast(fieldtype, field_value_before_save):
# 				# value not changed
# 				return

# 		if event != "Value Change" and not doc.is_new():
# 			# reload the doc for the latest values & comments,
# 			# except for validate type event.
# 			doc.reload()
# 		alert.send(doc)
# 	except TemplateError:
# 		message = _("Error while evaluating Notification {0}. Please fix your template.").format(
# 			frappe.utils.get_link_to_form("Notification", alert.name)
# 		)
# 		frappe.throw(message, title=_("Error in Notification"))
# 	except Exception as e:
# 		title = str(e)
# 		frappe.log_error(title=title)

# 		msg = f"<details><summary>{title}</summary>{message}</details>"
# 		frappe.throw(msg, title=_("Error in Notification"))



		
		
