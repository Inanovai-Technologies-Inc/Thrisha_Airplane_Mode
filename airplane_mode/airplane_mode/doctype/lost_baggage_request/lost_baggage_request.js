// Copyright (c) 2026, Thrisha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Lost Baggage Request", {
	refresh(frm) {
		add_delivery_button(frm);
		set_delivery_address_visibility(frm);
	},

	customer(frm) {
		if (frm.doc.customer) {
			frappe.db.get_value("Customer", frm.doc.customer, "customer_primary_address", (r) => {
				if (r && r.customer_primary_address) {
					frm.set_value("customer_address", r.customer_primary_address);
				} else {
					frm.set_value("customer_address", "");
				}
			});
		} else {
			frm.set_value("customer_address", "");
		}
	},

	delivery_preference(frm) {
		set_delivery_address_visibility(frm);
	},

	use_different_address(frm) {
		set_delivery_address_visibility(frm);
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
function set_delivery_address_visibility(frm) {
	const is_airport_delivery = frm.doc.delivery_preference === "Airport Delivery";

	// Show checkbox only for Airport Delivery
	frm.toggle_display("use_different_address", is_airport_delivery);

	// Show delivery address only when checkbox is checked
	const show_delivery_address = is_airport_delivery && frm.doc.use_different_address === 1;

	frm.toggle_display("delivery_address", show_delivery_address);
}

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
