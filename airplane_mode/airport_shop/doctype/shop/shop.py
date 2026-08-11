# Copyright (c) 2026, Thrisha and contributors

# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Shop(Document):
    def before_insert(self):
        if not self.rent_amount:
            default_rent = frappe.db.get_single_value(
                "Airport Shop Settings", "default_rent_amount"
            )
            self.rent_amount = default_rent

    def on_update(self):
        self.update_airport_counts()

    def on_trash(self):
        self.update_airport_counts()

    def update_airport_counts(self):
        if not self.airport:
            return

        total = frappe.db.count("Shop", {"airport": self.airport})

        occupied = frappe.db.count(
            "Shop", {"airport": self.airport, "status": "Occupied"}
        )

        available = frappe.db.count(
            "Shop", {"airport": self.airport, "status": "Available"}
        )

        frappe.db.set_value(
            "Airport",
            self.airport,
            {
                "total_shops": total,
                "occupied_shops": occupied,
                "available_shops": available,
            },
        )