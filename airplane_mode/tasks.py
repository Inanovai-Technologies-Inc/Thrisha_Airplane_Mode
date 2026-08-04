import frappe
from frappe.utils import getdate

def send_rent_reminders():

    print("Scheduler Working")

    enabled = frappe.db.get_single_value(
        "Airport Shop Settings",
        "enable_rent_reminder"
    )

    if not enabled:
        print("Rent reminders disabled")
        return

    shops = frappe.get_all(
        "Shop",
        filters={
            "status": "Occupied"
        },
        fields=[
            "name",
            "shop_name",
            "tenant",
            "rent_amount",
            "contract_end"
        ]
    )

#     for shop in shops:

#         if shop.contract_end and shop.contract_end < getdate():
#             continue

#         tenant = frappe.get_doc("Tenant", shop.tenant)

#         print(f"Sending reminder to {tenant.email}")

#         frappe.sendmail(
#             recipients=[tenant.email],
#             subject="Rent Due Reminder",
#             message=f"""
# Dear {tenant.tenant_name},

# This is a reminder that your monthly rent for Shop
# {shop.shop_name} is due.

# Amount: ₹{shop.rent_amount}

# Thank you.
# """
#         )

#     print("Completed")
    for shop in shops:

        print(f"Checking shop: {shop.shop_name}")

        if shop.contract_end and shop.contract_end < getdate():
            print("Contract expired")
            continue

        print(f"Tenant: {shop.tenant}")

        tenant = frappe.get_doc("Tenant", shop.tenant)

        print(f"Sending to: {tenant.email}")

        frappe.sendmail(
            recipients=[tenant.email],
            subject="Rent Due Reminder",
            message=f"""
    Dear {tenant.tenant_name},

    This is a reminder that your monthly rent for Shop {shop.shop_name} is due.

    Amount: ₹{shop.rent_amount}

    Thank you.
    """
        )

    print("Completed")