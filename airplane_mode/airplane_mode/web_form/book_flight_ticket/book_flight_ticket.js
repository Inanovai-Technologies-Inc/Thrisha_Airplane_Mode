frappe.ready(function () {
	function fetch_flight_details() {
		const flight = frappe.web_form.get_value("flight");

		if (!flight) {
			return;
		}

		console.log("Selected Flight:", flight);

		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Airplane Flight",
				name: flight,
			},
			callback: function (r) {
				console.log("Flight response:", r);

				if (!r.message) {
					console.log("Flight not found");
					return;
				}

				const data = r.message;

				console.log("Flight data:", data);

				frappe.web_form.set_value("source_airport_code", data.source_airport_code || "");

				frappe.web_form.set_value(
					"destination_airport_code",
					data.destination_airport_code || ""
				);

				frappe.web_form.set_value("departure_date", data.date_of_departure || "");

				frappe.web_form.set_value("departure_time", data.time_of_departure || "");

				frappe.web_form.set_value("duration_of_flight", data.duration || "");

				frappe.web_form.set_value("flight_price", data.flight_price || 0);

				frappe.web_form.set_value("gate_number", data.gate_number || "");
			},
		});
	}

	// When user selects a flight
	frappe.web_form.on("flight", function () {
		fetch_flight_details();
	});

	// Also fetch details if Flight already has a value
	setTimeout(function () {
		fetch_flight_details();
	}, 500);

	// Make fetched fields read-only
	frappe.web_form.set_df_property("source_airport_code", "read_only", 1);

	frappe.web_form.set_df_property("destination_airport_code", "read_only", 1);

	frappe.web_form.set_df_property("departure_date", "read_only", 1);

	frappe.web_form.set_df_property("duration_of_flight", "read_only", 1);

	frappe.web_form.set_df_property("departure_time", "read_only", 1);

	frappe.web_form.set_df_property("flight_price", "read_only", 1);

	frappe.web_form.set_df_property("gate_number", "read_only", 1);
});
