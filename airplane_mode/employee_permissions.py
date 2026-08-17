import frappe

# Map ERPNext Department names to the exact Role names in your system
DEPARTMENT_ROLE_MAP = {
	"HR": "HR User",
	"Purchasing": "Purchase User",
	"Marketing": "Marketing User",
}


def update_employee_company_permission(doc, method=None):
	if not doc.user_id or not doc.company:
		return

	user = doc.user_id

	# 1. Update Company User Permissions
	frappe.db.delete(
		"User Permission",
		{
			"user": user,
			"allow": "Company",
		},
	)

	# If assigned to a Group Company, leave User Permissions empty so they see all companies
	if is_group_company(doc.company):
		child_companies = frappe.get_all("Company", filters={"parent_company": doc.company}, pluck="name")
		for child in child_companies:
			frappe.get_doc(
				{
					"doctype": "User Permission",
					"user": user,
					"allow": "Company",
					"for_value": child,
				}
			).insert(ignore_permissions=True)

		frappe.get_doc(
			{
				"doctype": "User Permission",
				"user": user,
				"allow": "Company",
				"for_value": doc.company,
			}
		).insert(ignore_permissions=True)
	else:
		frappe.get_doc(
			{
				"doctype": "User Permission",
				"user": user,
				"allow": "Company",
				"for_value": doc.company,
			}
		).insert(ignore_permissions=True)

	# 2. Automatically sync User Role based on Employee Department
	sync_employee_role(user, doc.department)


def is_group_company(company_name):
	"""Check if the assigned company is a Group Company in ERPNext"""
	return frappe.db.get_value("Company", company_name, "is_group")


def sync_employee_role(user_id, department):
	"""Assigns the department role and removes other department roles"""
	if not department:
		return

	# Extract base department name (handles nested departments like "HR - II")
	dept_name = department.split(" - ")[0] if " - " in department else department
	target_role = DEPARTMENT_ROLE_MAP.get(dept_name)

	if not target_role:
		return

	user_doc = frappe.get_doc("User", user_id)
	dept_roles = set(DEPARTMENT_ROLE_MAP.values())

	# Filter out existing department roles and add the target role
	updated_roles = [r for r in user_doc.roles if r.role not in dept_roles]
	updated_roles.append({"role": target_role})

	user_doc.roles = updated_roles
	user_doc.save(ignore_permissions=True)
