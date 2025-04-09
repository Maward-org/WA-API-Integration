# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []

		# columns
	columns = [
		{"label": "Date", "fieldname": "log_date", "fieldtype": "Date", "width": 100},
		{"label": "Sent", "fieldname": "sent", "fieldtype": "Int", "width": 100},
		{"label": "Failed", "fieldname": "failed", "fieldtype": "Int", "width": 100}
	]

	# data
	from frappe import db
	from frappe.utils import getdate

	data = []

	results = db.sql("""
		SELECT 
			DATE(creation) as log_date,
			SUM(CASE WHEN status = 'Sent' THEN 1 ELSE 0 END) as sent,
			SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) as failed
		FROM `tabWA Log`
		GROUP BY DATE(creation)
		ORDER BY DATE(creation)
	""", as_dict=1)

	data = results
	return columns, data

		
		# return columns, data
