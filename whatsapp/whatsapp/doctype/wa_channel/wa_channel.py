# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json



class WAChannel(Document):
	@frappe.whitelist()
	def get_user_type_options(Self):
		wa_settings = frappe.get_single("WA Setting")

		user_types = [row.document_type for row in wa_settings.user_types]
		frappe.msgprint(user_types)
		return user_types


	
	@frappe.whitelist()
	def get_user_type_phone(self,user_type,user):
		
		# Fetch the single document "WA Settings"
		wa_settings = frappe.get_single("WA Setting")

		
		for row in wa_settings.user_types:  # Assuming 'user_settings' is the child table fieldname
			if row.document_type == user_type:
				value = frappe.get_value(user_type, user,row.phone_field)
				frappe.msgprint(f"value {value},user_type{user_type},row.phone_field{row.phone_field}")
				

				return value  # Return phone_field if user_type matches

		return None  # Return None if no match is found

		
	@frappe.whitelist()
	def create_log(self):
		# Create WA Logs entry
		if self.status=="Created":
			self.sync_members_with_whatsapp()
		else:
			# frappe.msgprint("create_log")

			if self.status=="Draft":
				#append cerator as member
				self.append("members", {
					"user_id": self.creator_id.split(":")[0],
					"is_super_admin":True,
					"user_type":"WA Account",
					"user": self.channel_creator
					})  # Assuming 'members' is a child table with 'user' field

				doc=frappe.get_doc({
					"doctype": "WA Log",
					"channel_type": "Group",  
					"channel_creator": self.channel_creator,
					"wa_channel": self.name,
					"type": "Create Group",
					"ref_doctype": self.doctype,
					"ref_document": self.name,
					"status": "Queued",
					"sender":self.channel_creator
				}).insert()
				if doc:
					self.status="Pending"
					self.save()
					
		
		#if name is changed
		#check if phone is the same
		
	


	def validate(self):
		if self.status=="Created":
			self.sync_members_with_whatsapp()
		
			
	def sync_members_with_whatsapp(self):
		# Fetch existing records from the database **AFTER SAVING**
		frappe.db.commit()  # Ensure DB is updated
		existing_members = frappe.get_all(
			"WA Channel User",
			filters={"parent": self.name},
			fields=["user_id", "is_admin", "is_removed"]
		)

		existing_data = {member["user_id"]: member for member in existing_members}
		current_data = {member.user_id: member.as_dict() for member in self.members}

		# Debugging prints
		frappe.msgprint(f"Existing Data: {existing_data}")
		frappe.msgprint(f"Current Data: {current_data}")

		# Identify added, removed, and modified members
		added_members = [m for uid, m in current_data.items() if uid not in existing_data]
		removed_members = [m for uid, m in existing_data.items() if uid not in current_data]
		
		promoted_members = []
		demoted_members = []

		for uid, m in current_data.items():
			if uid in existing_data:  # Ensure the user exists in both lists before comparing
				old_member = existing_data[uid]
				if m['is_admin'] == 1 and old_member['is_admin'] == 0:
					promoted_members.append(m)
				elif m['is_admin'] == 0 and old_member['is_admin'] == 1:
					demoted_members.append(m)
				elif m['is_removed'] == 1 and old_member['is_removed'] == 0:
					removed_members.append(m)

		# Debugging prints
		frappe.msgprint(f"Added: {added_members}")
		frappe.msgprint(f"Removed: {removed_members}")
		frappe.msgprint(f"Promoted: {promoted_members}")
		frappe.msgprint(f"Demoted: {demoted_members}")

		# Call WhatsApp update function
		if added_members:
			self.update_whatsapp_group(added_members, "Add User")
		if removed_members:
			self.update_whatsapp_group(removed_members, "Remove User")
		if promoted_members:
			self.update_whatsapp_group(promoted_members, "Promote User")
		if demoted_members:
			self.update_whatsapp_group(demoted_members, "Demote User")

	def update_whatsapp_group(self, members,type):
		"""
		Call your WhatsApp API here to update the group.
		"""
		for member in members:
			frappe.get_doc({
			"doctype": "WA Log",
			"channel_type": "Group",  
			"channel_creator": self.channel_creator,
			"wa_channel": self.name,
			"type": type,
			"ref_doctype": self.doctype,
			"ref_document": self.name,
			"status": "Queued",
			"sender":self.channel_creator,
			"receiver_id":self.channel_id,
			"user_id":member.user_id
		}).insert()
			if member.is_admin:
				frappe.get_doc({
				"doctype": "WA Log",
				"channel_type": "Group",  
				"channel_creator": self.channel_creator,
				"wa_channel": self.name,
				"type": "Promote User",
				"ref_doctype": self.doctype,
				"ref_document": self.name,
				"status": "Queued",
				"sender":self.channel_creator,
				"receiver_id":self.channel_id,
				"user_id":member.user_id
				}).insert()

			
		

