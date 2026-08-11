// Copyright (c) 2026, Thrisha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lost Baggage Request", {
	refresh(frm) {
		add_delivery_button(frm);
	},

	delivery_status(frm) {
		if (frm.doc.delivery_status === "Pending") {
			frappe.msgprint({
				title: __("Delivery Pending"),
				message: __("The lost baggage is not yet ready for delivery."),
				indicator: "orange",
			});
		} else if (frm.doc.delivery_status === "Ready for Delivery") {
			frappe.msgprint({
				title: __("Ready for Delivery"),
				message: __("The lost baggage is ready to be delivered to the customer."),
				indicator: "blue",
			});

			add_delivery_button(frm);
		}
	},
});

function add_delivery_button(frm) {
	if (!frm.is_new() && frm.doc.delivery_status === "Ready for Delivery") {
		frm.add_custom_button(__("Deliver Lost Baggage"), () => {
			frappe.confirm(
				__("Are you sure you want to mark this baggage as delivered to the customer?"),
				() => {
					frm.set_value("delivery_status", "Delivered");
					frm.set_value("delivered_on", frappe.datetime.now_datetime());

					frm.save().then(() => {
						frappe.msgprint({
							title: __("Success"),
							message: __("Lost baggage delivered successfully."),
							indicator: "green",
						});
					});
				}
			);
		});
	}
}
