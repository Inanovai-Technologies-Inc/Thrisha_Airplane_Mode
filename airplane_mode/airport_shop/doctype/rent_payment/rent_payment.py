# Copyright (c) 2026, Thrisha and contributors

import frappe
from frappe.model.document import Document
from datetime import datetime


class RentPayment(Document):

    def before_insert(self):
        year = datetime.now().year
        count = frappe.db.count("Rent Payment") + 1
        self.receipt_number = f"REC-{year}-{count:04d}"

    def validate(self):
        # Check that payment amount matches the shop's rent amount
        shop = frappe.get_doc("Shop", self.shop)

        if self.amount != shop.rent_amount:
            frappe.throw(
                f"Rent amount for this shop is ₹{shop.rent_amount:,.2f}. "
                "Please enter the correct rent amount."
            )

        # Treat the Month field as a month, regardless of the exact date
        month = frappe.utils.getdate(self.month)
        month_start = month.replace(day=1)

        if month.month == 12:
            next_month = month_start.replace(
                year=month.year + 1,
                month=1
            )
        else:
            next_month = month_start.replace(
                month=month.month + 1
            )

        # Check whether rent is already paid for this shop,
        # tenant and month
        exists = frappe.get_all(
            "Rent Payment",
            filters=[
                ["shop", "=", self.shop],
                ["tenant", "=", self.tenant],
                ["month", ">=", month_start],
                ["month", "<", next_month],
                ["name", "!=", self.name],
            ],
            limit=1
        )

        if exists:
            frappe.throw(
                "Rent has already been paid for this month."
            )

    def on_submit(self):
        self.create_sales_invoice()

    def create_sales_invoice(self):
        # Get Tenant
        tenant = frappe.get_doc("Tenant", self.tenant)

        # Tenant's Company field contains the ERPNext Customer
        customer = tenant.company

        if not customer:
            frappe.throw(
                "Please select a Customer in the Tenant's Company field."
            )

        # Get default Company
        company = frappe.defaults.get_user_default("Company")

        if not company:
            company = frappe.db.get_single_value(
                "Global Defaults",
                "default_company"
            )

        if not company:
            frappe.throw(
                "Please set a default Company in ERPNext."
            )

        # Create Sales Invoice
        invoice = frappe.new_doc("Sales Invoice")

        invoice.customer = customer
        invoice.company = company

        company_currency = frappe.db.get_value(
            "Company",
            company,
            "default_currency"
            )
        invoice.currency = company_currency
        invoice.conversion_rate = 1
        
        invoice.posting_date = (
            self.payment_date or frappe.utils.today()
        )

        invoice.append(
            "items",
            {
                "item_code": "Rent",
                "qty": 1,
                "rate": self.amount
            }
        )

        invoice.insert()
        invoice.submit()

        frappe.msgprint(
            f"Sales Invoice {invoice.name} created successfully."
        )

        # If Payment Date is entered, create Payment Entry
        if self.payment_date:
            self.create_payment_entry(invoice)

    def create_payment_entry(self, invoice):

        # Find Customer Receivable account
        receivable_account = frappe.db.get_value(
            "Account",
            {
                "company": invoice.company,
                "account_type": "Receivable",
                "is_group": 0
            },
            "name"
        )

        if not receivable_account:
            frappe.throw(
                "No Receivable account found for the Company."
            )

        # Find Bank or Cash account
        paid_from = frappe.db.get_value(
            "Account",
            {
                "company": invoice.company,
                "account_type": ["in", ["Bank", "Cash"]],
                "is_group": 0
            },
            "name"
        )

        if not paid_from:
            frappe.throw(
                "No Bank or Cash account found for the Company."
            )

        payment = frappe.new_doc("Payment Entry")

        payment.payment_type = "Receive"
        payment.company = invoice.company

        payment.posting_date = self.payment_date
        payment.reference_no = self.receipt_number
        payment.reference_date = self.payment_date
        payment.party_type = "Customer"

        payment.party = invoice.customer
        payment.paid_from = receivable_account
        payment.paid_to = paid_from

        payment.paid_amount = self.amount
        payment.received_amount = self.amount

        payment.append(
            "references",
            {
                "reference_doctype": "Sales Invoice",
                "reference_name": invoice.name,
                "allocated_amount": self.amount
            }
        )

        payment.insert()
        payment.submit()

        frappe.msgprint(
            f"Payment Entry {payment.name} created successfully."
        )