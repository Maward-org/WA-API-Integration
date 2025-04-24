# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document


class WALog(Document):
			
	def validate(self):
		if self.status=="Queued":
			self.send_wa_log_to_n8n()



	

	def send_wa_log_to_n8n(self):
		"""
		Send WA Logs data to the configured webhook in n8n.

		:param log_data: Dictionary containing WA Logs data.
		:return: Response from the webhook.
		"""
		url = "https://n8n.maward.org/webhook/process-log-pos.yemenfrappe.com"
		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
		}

		# Convert log_data to a format suitable for Form URL-Encoded requests
		payload = {
			"name": self.get("name"),
			# "sender": self.get("sender"),
			# "wa_automation_rule": self.get("wa_automation_rule") if self.get("wa_automation_rule") else "" ,
			# "receiver_id": self.get("receiver_id")
		}

		try:
			response = requests.post(url, headers=headers, data=payload, timeout=5)
			response.raise_for_status()  # Raise an error for HTTP error responses
			return response.json()  # Return JSON response from webhook
		except requests.exceptions.RequestException as e:
			return {"error": str(e)}


