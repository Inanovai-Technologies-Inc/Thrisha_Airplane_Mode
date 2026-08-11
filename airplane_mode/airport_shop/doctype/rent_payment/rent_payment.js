frappe.ui.form.on("Rent Payment", {
	shop(frm) {
		if (frm.doc.shop) {
			frappe.db.get_value("Shop", frm.doc.shop, "tenant").then((r) => {
				if (r.message && r.message.tenant) {
					frm.set_value("tenant", r.message.tenant);
				} else {
					frm.set_value("tenant", "");
					frappe.msgprint("No tenant is assigned to this shop.");
				}
			});
		} else {
			frm.set_value("tenant", "");
		}
	},

	refresh(frm) {
		frm.set_df_property("tenant", "read_only", 1);
	},
});
