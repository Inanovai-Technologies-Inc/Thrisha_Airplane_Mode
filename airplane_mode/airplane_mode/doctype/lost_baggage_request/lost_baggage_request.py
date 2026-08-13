# Copyright (c) 2026, Thrisha and contributors

# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LostBaggageRequest(Document):
	def on_update(self):
		if self.has_value_changed("delivery_status"):
			self.send_status_update_email()

	def send_status_update_email(self):
		if self.email:
			template = frappe.get_doc("Email Template", "Lost Baggage Status Update")

			message = frappe.get_template(template.response_html).render(self.as_dict())

			frappe.sendmail(
				recipients=[self.email],
				subject=template.subject,
				message=message,
			)
