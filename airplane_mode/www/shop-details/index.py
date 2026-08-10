import frappe

def get_context(context):
    name = frappe.form_dict.get("name")

    if not name:
        frappe.throw("Shop not specified")

    context.shop = frappe.get_doc("Shop", name)
    