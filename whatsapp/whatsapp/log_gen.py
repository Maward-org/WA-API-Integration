import json

import frappe
from frappe.utils import now_datetime, getdate
from frappe.utils.data import time_diff_in_seconds
from frappe.utils.pdf import get_pdf


def apply(doc, state):
    """DocEvent hook used to trigger WA Automation Rule on document change."""

    # أثناء install / migrate / patch لا تشغّل أي منطق إضافي
    if getattr(frappe.flags, "in_migrate", False) or getattr(
        frappe.flags, "in_patch", False
    ) or getattr(frappe.flags, "in_install", False):
        return

    # لو DocType نفسه لسه ما نزل من JSON للـ DB لا تعمل شيء
    if not frappe.db.exists("DocType", "WA Automation Rule"):
        return

    try:
        rules = frappe.get_list(
            "WA Automation Rule",
            filters={"enabled": 1, "document_type": doc.doctype},
            pluck="name",
        )
    except Exception:
        # احتياط إضافي لو الميتا للحين ما تجهّزت
        return

    if not rules:
        return

    for rule_name in rules:
        rule = frappe.get_doc("WA Automation Rule", rule_name)

        sender = rule.sending_account
        receiver = None

        if rule.channel_type == "Direct":
            receiver = doc.get(rule.recipient_phone_field)

        if not sender:
            frappe.log_error(
                title="WA Automation Rule: Missing Sending Account",
                message=f"Rule {rule.name}: sending_account is not set.",
            )
            continue

        if rule.channel_type == "Direct" and not receiver:
            frappe.log_error(
                title="WA Automation Rule: Missing Receiver",
                message=(
                    f"Rule {rule.name}: field '{rule.recipient_phone_field}' "
                    f"is empty on document {doc.doctype} {doc.name}"
                ),
            )
            continue

        if rule.channel_type == "Group" and not rule.group_id:
            frappe.log_error(
                title="WA Automation Rule: Missing Group ID",
                message=f"Rule {rule.name}: group_id is not set.",
            )
            continue

        try:
            # متوقّع أن send موجودة على DocType WA Automation Rule
            rule.send(doc)
        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                title=f"WA Automation Rule execution failed ({rule.name})",
            )


@frappe.whitelist()
def process_whatsapp_pop_up(data, doctype, docname):
    """
    Send WhatsApp message from popup (single document).

    Expected 'data':
        receiver (Contact name)
        message
        attach_document_print (bool)
        send_copy (bool)
        print_language
        print_format
        checked_attachments (list of file urls)
    """
    if isinstance(data, str):
        data = json.loads(data or "{}")

    # Resolve module and WA account for this module
    module = frappe.get_meta(doctype).module
    wa_settings = frappe.get_single("WA Setting")

    account = ""
    for row in wa_settings.account_module_settings:
        if row.module == module:
            account = row.sending_account
            break

    if not account:
        frappe.throw(f"Account is not set for module {module} in WA Setting")

    receiver_name = data.get("receiver")
    if not receiver_name:
        frappe.throw("Receiver is required")

    msg = data.get("message") or ""
    is_attach_print = data.get("attach_document_print")
    send_copy = data.get("send_copy")
    lang = data.get("print_language")
    attachments = data.get("checked_attachments") or []

    doc = frappe.get_doc(doctype, docname)
    sender_doc = frappe.get_doc("WA Account", account)
    to = frappe.get_doc("Contact", receiver_name)

    # Attach print as PDF if requested
    if is_attach_print:
        if lang:
            frappe.local.lang = lang

        frappe.local.site = getattr(frappe.local, "site", None) or frappe.get_site_path()
        frappe.local.signed_query_string = True

        print_format = data.get("print_format")
        pdf_data = frappe.get_print(
            doctype=doctype,
            name=docname,
            print_format=print_format,
            as_pdf=True,
            doc=doc,
        )

        filename = f"{doctype}-{docname}-{doc.creation}.pdf"
        file_doc = frappe.get_doc(
            {
                "doctype": "File",
                "file_name": filename,
                "is_private": 1,
                "content": pdf_data,
                "attached_to_doctype": doctype,
                "attached_to_name": docname,
            }
        ).insert(ignore_permissions=True)

        if file_doc:
            attachments.append(file_doc.file_url)

    # Create WA Log for each attachment
    for attach in attachments:
        generate_log(
            sender=account,
            reciever=to.custom_wa_number,
            type="Send Attach",
            doctype=doctype,
            ref_doc=docname,
            channel_type="Direct",
            content=msg,
            url=attach,
        )

        if send_copy:
            # Send copy to sender's device number
            sender_number = (sender_doc.device_id or "").split(":")[0]
            if sender_number:
                generate_log(
                    sender=account,
                    reciever=sender_number,
                    type="Send Attach",
                    doctype=doctype,
                    ref_doc=docname,
                    channel_type="Direct",
                    content=msg,
                    url=attach,
                )


@frappe.whitelist()
def process_report_whatsapp_pop_up(data):
    """
    Send a report as PDF over WhatsApp.

    Expected 'data':
        doctype
        letter_head
        data
        columns
        orientation
        message
        receiver (Contact name)
        html (pre-rendered HTML)
        send_copy (bool)
    """
    if isinstance(data, str):
        data = json.loads(data or "{}")

    doctype = data.get("doctype")
    if not doctype:
        frappe.throw("doctype is required")

    receiver_name = data.get("receiver")
    if not receiver_name:
        frappe.throw("Receiver is required")

    msg = data.get("message") or ""
    html = data.get("html")
    orientation = data.get("orientation") or "Landscape"
    send_copy = data.get("send_copy")

    to = frappe.get_doc("Contact", receiver_name)

    # Resolve module and WA account
    module = frappe.get_meta(doctype).module
    wa_settings = frappe.get_single("WA Setting")

    account = ""
    for row in wa_settings.account_module_settings:
        if row.module == module:
            account = row.sending_account
            break

    if not account:
        frappe.throw(f"Account is not set for module {module} in WA Setting")

    if not html:
        frappe.throw("No HTML content provided for report")

    # Generate PDF from HTML
    pdf_data = get_pdf(html, {"orientation": orientation})

    # Save file
    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": f"Report-{now_datetime()}.pdf",
            "is_private": 1,
            "content": pdf_data,
        }
    ).insert(ignore_permissions=True)

    # Create WA logs
    generate_log(
        sender=account,
        reciever=to.custom_wa_number,
        type="Send Attach",
        doctype=doctype,
        ref_doc=doctype,  # لا يوجد مستند معيّن، نستخدم اسم الـ Doctype كمرجع
        channel_type="Direct",
        content=msg,
        url=file_doc.file_url,
    )

    if send_copy:
        sender_doc = frappe.get_doc("WA Account", account)
        sender_number = (sender_doc.device_id or "").split(":")[0]
        if sender_number:
            generate_log(
                sender=account,
                reciever=sender_number,
                type="Send Attach",
                doctype=doctype,
                ref_doc=doctype,
                channel_type="Direct",
                content=msg,
                url=file_doc.file_url,
            )


def months_apart(date1, date2):
    """Return number of full months between two dates."""
    d1 = getdate(date1)
    d2 = getdate(date2)
    return (d2.year - d1.year) * 12 + d2.month - d1.month


@frappe.whitelist()
def process_scheduled_rule():
    """
    Scheduled task to process all enabled & scheduled WA Automation Rule records.
    Generates the defined report and sends it via WhatsApp.
    """

    # Safety: don't run if DocType does not exist yet
    if not frappe.db.exists("DocType", "WA Automation Rule"):
        return

    rules = frappe.get_all(
        "WA Automation Rule",
        filters={"enabled": 1, "scheduled": 1},
        fields=["*"],
    )

    for rule in rules:
        if not should_run(rule):
            continue

        module = frappe.get_meta(rule.document_type).module
        wa_settings = frappe.get_single("WA Setting")

        account = ""
        for row in wa_settings.account_module_settings:
            if row.module == module:
                account = row.sending_account
                break

        if not account:
            frappe.log_error(
                title="WA Scheduled Rule: Missing Account",
                message=f"Account is not set for module {module} in WA Setting",
            )
            continue

        # Generate report content
        report = frappe.get_doc("Report", rule.report_ref)
        columns, data = report.get_data(
            user="Administrator",
            as_dict=True,
            ignore_prepared_report=True,
        )

        grid_html = frappe.render_template(
            "whatsapp/templates/includes/jinja_print_grid.html",
            {
                "title": report.name,
                "subtitle": "",
                "columns": columns,
                "data": data,
                "original_data": data,
                "landscape": True,
                "can_use_smaller_font": True,
                "report": report,
            },
        )

        wrapper_html = frappe.render_template(
            "whatsapp/templates/includes/jinja_standard.html",
            {
                "content": grid_html,
                "letter_head": "<p>Letterhead</p>",
                "footer": "<p>Footer</p>",
                "print_settings": {"repeat_header_footer": 1},
            },
        )

        pdf_content = get_pdf(wrapper_html)

        file_doc = frappe.get_doc(
            {
                "doctype": "File",
                "file_name": f"Report-{now_datetime()}.pdf",
                "is_private": 1,
                "content": pdf_content,
            }
        ).insert(ignore_permissions=True)

        if not file_doc:
            continue

        log_created = generate_log(
            sender=account,
            reciever=rule.recipient,
            type="Send Attach",
            doctype="WA Automation Rule",
            ref_doc=rule.name,
            channel_type="Direct",
            content="",
            url=file_doc.file_url,
        )

        if not log_created:
            continue

        # Commit log + file, then update last_run
        frappe.db.commit()

        frappe.db.sql(
            """
            UPDATE `tabWA Automation Rule`
            SET last_run = %s
            WHERE name = %s
        """,
            (now_datetime(), rule.name),
        )

        frappe.db.commit()


def should_run(rule):
    """
    Decide if a scheduled rule should run now based on last_run and schedule_interval.
    """
    last_run = rule.get("last_run")
    now = now_datetime()

    if not last_run:
        # إذا لا يوجد last_run نستخدم start_date، ولو فاضي يشغل أول مرة الآن
        last_run = rule.get("start_date") or now

    if rule.schedule_interval == "Monthly":
        return months_apart(last_run, now) >= 1

    diff_minutes = time_diff_in_seconds(now, last_run) / 60
    interval = get_interval_in_minutes(rule.schedule_interval)

    return diff_minutes >= interval


def get_interval_in_minutes(schedule_type):
    if schedule_type == "Daily":
        return 1440
    if schedule_type == "Weekly":
        return 10080
    if schedule_type == "Yearly":
        return 525600  # 365 * 24 * 60

    # Fallback: effectively never
    return 9999999


def should_trigger(schedule_type, diff):
    """
    Legacy helper kept for compatibility if called from elsewhere.
    """
    if schedule_type == "Every Minute" and diff >= 1:
        return True
    if schedule_type == "Every 2 Minutes" and diff >= 2:
        return True
    if schedule_type == "Hourly" and diff >= 60:
        return True
    if schedule_type == "Daily" and diff >= 1440:
        return True

    return False


def generate_log(sender, reciever, type, doctype, ref_doc, channel_type, content, url=None):
    """
    Create WA Log entry.
    If a private URL is passed, normalise it to start from /private.
    """
    if url and "http" in str(url):
        private_index = url.find("/private")
        if private_index != -1:
            url = url[private_index:]

    doc = frappe.get_doc(
        {
            "doctype": "WA Log",
            "sender": sender,
            "receiver_id": reciever,
            "type": type,
            "ref_doctype": doctype,
            "ref_document": ref_doc,
            "status": "Queued",
            "channel_type": channel_type,
            "file_reference": url,
            "content": content,
        }
    ).insert()

    if doc:
        return True

    return False
