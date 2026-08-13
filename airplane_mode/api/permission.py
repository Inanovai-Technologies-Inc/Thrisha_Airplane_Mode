import frappe


def has_app_permission():
    allowed_roles = {
        "System Manager",
        "Airport Authority Personnel",
        "Fleet Manager",
        "Flight Crew Member",
        "Travel Agent",
    }

    return bool(set(frappe.get_roles()) & allowed_roles)