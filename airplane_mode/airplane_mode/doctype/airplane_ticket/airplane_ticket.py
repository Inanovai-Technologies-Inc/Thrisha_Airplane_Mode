import random

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
	def before_insert(self):
		# Generate a seat number
		number = random.randint(1, 99)
		letter = random.choice(["A", "B", "C", "D", "E"])
		self.seat = f"{number}{letter}"

		# Fetch flight details from the selected Airplane Flight
		if self.flight:
			flight = frappe.db.get_value(
				"Airplane Flight",
				self.flight,
				[
					"source_airport_code",
					"destination_airport_code",
					"date_of_departure",
					"time_of_departure",
					"duration",
					"flight_price",
					"gate_number",
				],
				as_dict=True,
			)

			if flight:
				# Automatically fetch flight information
				self.source_airport_code = flight.source_airport_code
				self.destination_airport_code = flight.destination_airport_code
				self.departure_date = flight.date_of_departure
				self.departure_time = flight.time_of_departure
				self.duration_of_flight = flight.duration
				self.flight_price = flight.flight_price
				self.gate_number = flight.gate_number

	def after_insert(self):
		# Automatically submit tickets created through the Web Form
		if frappe.flags.in_web_form and self.docstatus == 0:
			self.submit()

	def validate(self):
		self.calculate_total()
		self.remove_duplicate_addons()

	def calculate_total(self):
		total = self.flight_price or 0

		for addon in self.add_ons:
			total += addon.amount or 0

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
		# Send confirmation email after ticket is confirmed
		self.send_confirmation_email()

	def send_confirmation_email(self):
		# Get passenger information
		passenger = frappe.get_doc("Flight Passenger", self.passenger)

		# Check whether passenger has an email
		if not passenger.email:
			frappe.msgprint(_("Passenger does not have an email address."))
			return

		# Send confirmation email
		frappe.sendmail(
			recipients=[passenger.email],
			subject=f"Flight Ticket Confirmed - {self.name}",
			message=f"""
                <h3>Flight Ticket Confirmed</h3>

                <p>Dear {passenger.full_name},</p>

                <p>
                    Your flight ticket has been successfully confirmed.
                </p>

                <p>
                    <b>Ticket:</b> {self.name}<br>
                    <b>Flight:</b> {self.flight}<br>
                    <b>From:</b> {self.source_airport_code}<br>
                    <b>To:</b> {self.destination_airport_code}<br>
                    <b>Departure Date:</b> {self.departure_date}<br>
                    <b>Departure Time:</b> {self.departure_time}<br>
                    <b>Duration:</b> {self.duration_of_flight}<br>
                    <b>Flight Price:</b> ₹{self.flight_price}<br>
                    <b>Seat:</b> {self.seat}<br>
                    <b>Gate:</b> {self.gate_number}
                </p>

                <p>
                    Thank you for booking with us.
                </p>
            """,
		)
