import frappe
import os
# from frappe.utils.pdf import get_pdf as _get_pdf
from frappe.utils.pdf import get_pdf
from frappe.utils.file_manager import save_file


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



@frappe.whitelist()
def process_whatsapp_pop_up(data,doctype,doc):
        import json

        if isinstance(data, str):
                data = json.loads(data)
        
        # #fecth needed info


        # sender = frappe.db.get_single_value('WA Setting', 'hrms_sender')

        module = frappe.get_meta(doctype).module


        doc = frappe.get_single("WA Setting") 
        account=""
        for row in doc.account_module_settings:
                if row.module ==module:
                        account= row.sending_account 

        
        if not account:
                frappe.throw(f"Account is not set for module{module} in WA Setting")

        

        receiver = data.get("receiver")
        msg = data.get("message")
        is_attach_print=data.get("attach_document_print")
        send_copy=data.get("send_copy")
        doc_details = frappe.get_doc(doctype, doc)
        lang=data.get("print_language")
        attachments = data.get("checked_attachments") or []
        sender_doc=frappe.get_doc("WA Account",account)
        to=frappe.get_doc("Contact",receiver)

        # frappe.msgprint(len(attachments))

        # frappe.msgprint(f"doc: {to}")
                

        # frappe.msgprint(f"is_attach_print {is_attach_print}")

        
        # Generate PDF
        if is_attach_print:
                if lang:
                        frappe.local.lang = lang
                frappe.local.site = frappe.local.site or frappe.get_site_path()
                frappe.local.signed_query_string = True

                
                
                print_foramt=data.get("print_format")
                pdf_data = frappe.get_print(
                        doctype=doctype,
                        print_format=print_foramt,
                        # lang=lang,
                        as_pdf=True,
                        doc=doc_details
                        )


                filename = f"SalarySlip-{doc}-{doc_details.creation}.pdf"
                file_doc = frappe.new_doc("File")
                file_doc.update({
                        "file_name": filename,
                        "is_private": 0,
                        "content": pdf_data,
                        "dt":"Salary Slip",
                        "dn":doc,
                        "is_private":1
                })
                file_doc.save(ignore_permissions=True)
                # frappe.msgprint(f"{len(data.get("checked_attachments"))}")
                
#                 frappe.msgprint("jere")
                if file_doc:	
                        attachments.append(file_doc.file_url)
                # print("Attachmentsss:", attachments)

                # frappe.msgprint(", ".join(attachments))

        for attach in attachments:
                frappe.msgprint(f"loop{to}")
                # Generate Log
                generate_log(account,to.custom_wa_number,"Send Attach",doctype,doc,"Direct",msg,attach)
                
                
                if send_copy:
                        #get sending account phone num
                        
                        #Generate Log
                        generate_log(account,sender_doc.device_id.split(':')[0],"Send Attach",doctype,doc,"Direct",msg,attach)


@frappe.whitelist()
def process_report_whatsapp_pop_up(data):

        import json
     

        if isinstance(data, str):
            data = json.loads(data)
        doctype = data.get("doctype")
        letter_head = data.get("letter_head")
        rows=data.get("data")
        columns=data.get("columns")
        orientation=data.get("orientation")
        msg=data.get("message")
        receiver=data.get("receiver")
        to=frappe.get_doc("Contact",receiver)
        
        html=data.get("html")
        send_copy=data.get("send_copy")

        if letter_head:
                letterhead_html = frappe.get_doc("Letter Head", letter_head).content


       

        module = frappe.get_meta(data.get("doctype")).module
        doc = frappe.get_single("WA Setting") 
        account=""
        for row in doc.account_module_settings:
                if row.module ==module:
                        account= row.sending_account 

        
        if not account:
                frappe.throw(f"Account is not set for module{module} in WA Setting")

        # If you're passing pre-rendered HTML (from client side)
        if html:
                # Step 1: Generate PDF binary from the HTML
                pdf_data = get_pdf(html, {"orientation": orientation or "Landscape"})

                # Step 2: Save it as a File
                file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": f"Report-{frappe.utils.now_datetime()}.pdf",
                        "is_private": 1,
                        "content": pdf_data
                })
                file_doc.save(ignore_permissions=True)
                

                generate_log(account,to.custom_wa_number,"Send Attach",doctype,doc,"Direct",msg,file_doc.file_url)

                if send_copy:
                    sender_doc=frappe.get_doc("WA Account",account)

                    generate_log(account,sender_doc.device_id.split(':')[0],"Send Attach",doctype,doc,"Direct",msg,file_doc.file_url)


        # from frappe.utils.pdf import get_pdf
        # from frappe.templates.pages.print import print_report
        # from frappe.utils.print_format import print_report

                
from frappe.utils import now_datetime
from frappe.utils.data import time_diff_in_seconds
from frappe.utils import getdate


# from frappe.utils import time_diff_in_minutes


def months_apart(date1, date2):
        """Return number of full months between two dates"""
        print("months_apart")
        d1 = getdate(date1)
        d2 = getdate(date2)
        return (d2.year - d1.year) * 12 + d2.month - d1.month


@frappe.whitelist()
def process_scheduled_rule():
        rules = frappe.get_all("WA Automation Rule", filters={
                "enabled": 1,
                "scheduled": 1
        }, fields=['*'])
        # print("here")
        for rule in rules:
                # print(f"rule{rule}")
                if should_run(rule):
                        # print("should_run")
                        module = frappe.get_meta(rule.document_type).module


                        doc = frappe.get_single("WA Setting") 
                        account=""
                        for row in doc.account_module_settings:
                                if row.module ==module:
                                        account= row.sending_account 

                        
                        if not account:
                                frappe.throw(f"Account is not set for module {module} in WA Setting")
                        # print("should run")
                        #generate pdf
                        report = frappe.get_doc("Report", rule.report_ref)
                        columns, data = report.get_data(
                        user="Administrator",  # or current user
                        # filters=filters,
                        as_dict=True,
                        ignore_prepared_report=True
                                )
                        # print(f"columns{columns}")
                        grid_html = frappe.render_template("whatsapp/templates/includes/jinja_print_grid.html", {
                                "title": report.name,
                                "subtitle": "",
                                "columns": columns,
                                "data": data,
                                "original_data": data,
                                "landscape": True,
                                "can_use_smaller_font": True,
                                "report": report
                        })
                        wrapper_html = frappe.render_template("whatsapp/templates/includes/jinja_standard.html", {
                                "content": grid_html,
                                "letter_head": "<p>Letterhead</p>",  # or pull from Company
                                "footer": "<p>Footer</p>",
                                "print_settings": {
                                        "repeat_header_footer": 1
                                }
                        })



                        
                        pdf_content = frappe.utils.pdf.get_pdf(wrapper_html)



                        # print(f"hrml{wrapper_html}")
                        # pdf_content = frappe.utils.pdf.get_pdf(html)
                        # print("PDF length:", len(pdf_content))

                        # save as File doc
                        # print("no error")
                        file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": f"Reportt-{frappe.utils.now_datetime()}.pdf",
                        "is_private": 1,
                        "content": pdf_content
                        })
                        file_doc.save(ignore_permissions=True)
                        # print(f"file_doc{file_doc}")

                        if file_doc:
                                log_created=generate_log(account,rule.recipient,"Send Attach","WA Automation Rule",rule.name,"Direct","",file_doc.file_url)
                                if log_created:
                                        print("created")
                                        frappe.db.commit()

                                        # safe update using SQL directly
                                        frappe.db.sql("""
                                                UPDATE `tabWA Automation Rule`
                                                SET last_run = %s
                                                WHERE name = %s
                                        """, (now_datetime(), rule.name))
                                        
                                        frappe.db.commit()
                        #         print("file_doc")
                        # file_doc = frappe.get_doc({
                        # "doctype": "File",
                        # "file_name": f"{report.name}.pdf",
                        # "content": pdf_content,
                        # "is_private": 1
                        # }).insert(ignore_permissions=True)

                        #save it as file_doc
                       

from frappe.utils import now

@frappe.whitelist()
def method_name():
        process_scheduled_rule()
        print("here")

        
        # doc=frappe.get_doc(
        #                 {
        #                         "doctype": "WA Log",
                        
        #                         "sender": "WA-ACC-012",
        #                         "receiver_id": "444444",
        #                         "type": "Send Message",
        #                         "ref_doctype": "Item",
        #                         "ref_document": "test4",
                        
                                
        #                         "status":"Queued",
        #                         "channel_type":"Direct",
        #                         # "file_reference":url,
        #                         # "content":content
        #                         # "group_id":self.group_id

                                
        #                 }
        #         ).insert() 
        # print(f"here{doc}")
        # frappe.db.commit()
    
        # frappe.logger().info(f"🔔 My scheduler task ran at {now()}")

def should_run(rule):
        last_run = rule.get("last_run")
        now = now_datetime()

        if not last_run:
                last_run = rule.get("start_date")

        if rule.schedule_interval == "Monthly":
                return months_apart(last_run, now) >= 1
        

        diff_minutes = time_diff_in_seconds(now, last_run) / 60
        print(f"diff_minutes{diff_minutes}")

        interval = get_interval_in_minutes(rule.schedule_interval)
        return diff_minutes >= interval

def get_interval_in_minutes(schedule_type):
        print(f"get_interval_in_minutes{schedule_type}")
        if schedule_type == "Daily":
                print("daily")

                return 1440
        if schedule_type == "Weekly":
                return 10080
        if schedule_type == "Yearly":
                return 525600  # 365 * 24 * 60
        return 9999999  # fallback for others


def months_apart(date1, date2):
	"""Return number of full months between two dates"""
	d1 = getdate(date1)
	d2 = getdate(date2)
	return (d2.year - d1.year) * 12 + d2.month - d1.month


def should_trigger(schedule_type, diff):
        if schedule_type == "Every Minute" and diff >= 1:
                return True
        if schedule_type == "Every 2 Minutes" and diff >= 2:
                return True
        if schedule_type == "Hourly" and diff >= 60:
                return True
        if schedule_type == "Daily" and diff >= 1440:
                return True
        # Add more as needed
        return False

               

                        
def generate_log(sender,reciever,type,doctype,ref_doc,channel_type,content,url=None):
        if url and "http" in url:
                url = url[url.find("/private"):]
                
        
                

        doc=frappe.get_doc(
                        {
                                "doctype": "WA Log",
                        
                                "sender": sender,
                                "receiver_id": reciever,
                                "type": type,
                                "ref_doctype": doctype,
                                "ref_document": ref_doc,
                        
                                
                                "status":"Queued",
                                "channel_type":channel_type,
                                "file_reference":url,
                                "content":content
                                # "group_id":self.group_id

                                
                        }
                ).insert() 
                
        if doc:
                return True

# return "Salary slips generated and saved."
