import frappe
import random

from frappe.model.document import Document


class AirplaneTicket(Document):
    def before_insert(self):

        number = random.randint(1, 99)

        letter = random.choice(["A","B","C","D","E"])

        self.seat = f"{number}{letter}"
    def before_insert(self):
        
        if self.flight:
            self.gate_number = frappe.db.get_value(
                "Airplane Flight",
                self.flight,
                "gate_number"
            )

    def validate(self):

        self.calculate_total()

        self.remove_duplicate_addons()

    def calculate_total(self):

        total = self.flight_price

        for addon in self.add_ons:

            total += addon.amount

        self.total_amount = total

    def remove_duplicate_addons(self):

        unique = []

        seen = set()

        for row in self.add_ons:

            if row.item not in seen:

                seen.add(row.item)

                unique.append(row)

        self.set("add_ons", unique)

    def on_submit(self):

        if self.status != "Boarded":

            frappe.throw("Ticket can only be submitted when passenger has boarded.")