import frappe
from frappe.model.document import Document


class LostBaggageRequest(Document):
	def on_update(self):
		if self.has_value_changed("status"):
			self.send_status_update_email()

	def send_status_update_email(self):
		if self.email:
			template = frappe.get_doc("Email Template", "Lost Baggage Status Update")

			email = template.get_formatted_email(self.as_dict())

			frappe.sendmail(
				recipients=[self.email],
				subject=email["subject"],
				message=email["message"],
			)
