import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()

	total_revenue = sum(row["revenue"] for row in data)

	chart = {
		"data": {
			"labels": [row["airline"] for row in data],
			"datasets": [{"values": [row["revenue"] for row in data]}],
		},
		"type": "donut",
	}

	report_summary = [
		{"label": _("Total Revenue"), "value": total_revenue, "indicator": "Green", "datatype": "Currency"}
	]

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 250,
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 180,
		},
	]


def get_data():
	airlines = frappe.get_all("Airline", fields=["name"])
	revenue_map = {}
	for airline in airlines:
		revenue_map[airline.name] = 0

	tickets = frappe.get_all("Airplane Ticket", filters={"docstatus": 1}, fields=["flight", "flight_price"])

	for ticket in tickets:
		flight = frappe.db.get_value("Airplane Flight", ticket.flight, "airplane")

		if not flight:
			continue
		airline = frappe.db.get_value("Airplane", flight, "airline")

		if airline:
			revenue_map[airline] += ticket.flight_price or 0

	data = []

	for airline, revenue in revenue_map.items():
		data.append(
			{
				"airline": airline,
				"revenue": revenue,
			}
		)

	return data
