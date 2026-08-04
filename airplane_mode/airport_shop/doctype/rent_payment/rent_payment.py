# Copyright (c) 2026, Thrisha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class RentPayment(Document):
    def before_insert(self):
        year=datetime.now().year
        count=frappe.db.count("Rent Payment")+1
        self.receipt_number=f"REC-{year}-{count:04d}"
        
    def validate(self):
        exists = frappe.db.exists(
            "Rent Payment",
            {
                "shop": self.shop,
                "month": self.month,
                "name": ["!=", self.name]
            }
        )
        if exists:
            frappe.throw(
                "Rent has already been paid for this month."
            )