frappe.ui.form.on("Shop", {
	refresh(frm) {
		frm.set_query("shop_type", function () {
			return {
				filters: {
					enabled: 1,
				},
			};
		});
	},
});
