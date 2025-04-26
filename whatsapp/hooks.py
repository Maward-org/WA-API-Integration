app_name = "whatsapp"
app_title = "WhatsApp"
app_publisher = "Yemen Frappe"
app_description = "Whatsapp "
app_email = "yemen.frappe@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "whatsapp",
# 		"logo": "/assets/whatsapp/logo.png",
# 		"title": "WhatsApp",
# 		"route": "/whatsapp",
# 		"has_permission": "whatsapp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/whatsapp/css/whatsapp.css"
# app_include_js = "/assets/whatsapp/js/whatsapp.js"
app_include_js = ["/assets/whatsapp/js/custom_toolbar.js",
                  "/assets/whatsapp/js/wa_composer.js",
                  "/assets/whatsapp/js/report_wa_composer.js"
                  
]




# include js, css files in header of web template
# web_include_css = "/assets/whatsapp/css/whatsapp.css"
# web_include_js = "/assets/whatsapp/js/whatsapp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "whatsapp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Salary Slip" : "public/js/salary_slip.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "whatsapp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "whatsapp.utils.jinja_methods",
# 	"filters": "whatsapp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "whatsapp.install.before_install"
# after_install = "whatsapp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "whatsapp.uninstall.before_uninstall"
# after_uninstall = "whatsapp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "whatsapp.utils.before_app_install"
# after_app_install = "whatsapp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "whatsapp.utils.before_app_uninstall"
# after_app_uninstall = "whatsapp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "whatsapp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

#
override_doctype_class = {
    "Contact": "whatsapp.overrides.custom_contact.CustomContact"
}
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		# "on_update": "method",
		# "on_cancel": "method",
		# "on_trash": "method",
        "on_change": [
			"whatsapp.whatsapp.log_gen.apply",
			
		],
        
	},
   
    # "WA Channel": {
    #     "on_update": "whatsapp.whatsapp.wa_channel.wa_channel.create_log"
    # }
}

    


# Scheduled Tasks
# ---------------
scheduler_events = {
    "cron": {
        "* * * * *": [
            "whatsapp.whatsapp.log_gen.method_name"
        ]
    }
}


# scheduler_events = {
# 	"all": [
# 		"whatsapp.tasks.all"
# 	],
# 	"daily": [
# 		"whatsapp.tasks.daily"
# 	],
# 	"hourly": [
# 		"whatsapp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"whatsapp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"whatsapp.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "whatsapp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "whatsapp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "whatsapp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["whatsapp.utils.before_request"]
# after_request = ["whatsapp.utils.after_request"]

# Job Events
# ----------
# before_job = ["whatsapp.utils.before_job"]
# after_job = ["whatsapp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"whatsapp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

