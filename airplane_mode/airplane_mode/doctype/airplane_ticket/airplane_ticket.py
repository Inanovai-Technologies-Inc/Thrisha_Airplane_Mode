import frappe
import random

from frappe.model.document import Document

class AirplaneTicket(Document):

    def before_insert(self):
        # Generate a seat number
        number = random.randint(1, 99)
        letter = random.choice(["A", "B", "C", "D", "E"])
        self.seat = f"{number}{letter}"

        # Get gate number from the selected flight
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
        # Ticket can be submitted only after passenger has boarded
        if self.status != "Boarded":
            frappe.throw(
                "Ticket can only be submitted when passenger has boarded."
            )

        # Create one Sales Invoice for this ticket
        self.create_sales_invoice()

    def create_sales_invoice(self):

        # Prevent duplicate invoice creation
        if self.sales_invoice:
            return

        # Get passenger
        passenger = frappe.get_doc(
            "Flight Passenger",
            self.passenger
        )

        # Passenger must have a Customer
        if not passenger.customer:
            frappe.throw(
                "Please set a Customer for the Flight Passenger "
                "before submitting the ticket."
            )

        # Create Sales Invoice
        invoice = frappe.new_doc("Sales Invoice")

        invoice.customer = passenger.customer
        invoice.posting_date = frappe.utils.today()

        # Add flight ticket as invoice item
        invoice.append("items", {
            "item_code": "AIRPLANE-TICKET",
            "qty": 1,
            "rate": self.flight_price
        })

        # Add ticket add-ons to the invoice
        for addon in self.add_ons:

            invoice.append("items", {
                "item_code": addon.item,
                "qty": 1,
                "rate": addon.amount
            })

        # Save as Draft
        invoice.insert()

        # Store invoice reference in Airplane Ticket
        self.db_set("sales_invoice", invoice.name)

