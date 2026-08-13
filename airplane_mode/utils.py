def import_workspace():
    """Import workspace JSON into the site DB (idempotent)."""
    import json
    import frappe

    path = frappe.get_app_path("airplane_mode", "workspace", "airplane_mode", "airplane_mode.json")
    with open(path) as f:
        data = json.load(f)

    name = data.get("name")
    workspace_fields = {
        "doctype": "Workspace",
        "name": name,
        "label": data.get("label"),
        "title": data.get("title"),
        "module": data.get("module"),
        "public": data.get("public"),
        "is_default": data.get("is_default"),
        "content": data.get("content"),
        "links": data.get("links"),
    }

    if frappe.db.exists("Workspace", name):
        doc = frappe.get_doc("Workspace", name)
        for k, v in workspace_fields.items():
            if k in ("doctype", "name"):
                continue
            try:
                doc.set(k, v)
            except Exception:
                pass
        doc.save()
        return f"Updated Workspace {name}"
    else:
        frappe.get_doc(workspace_fields).insert(ignore_permissions=True)
        return f"Inserted Workspace {name}"


def list_workspaces():
    import frappe
    return [d.name for d in frappe.get_all("Workspace")]


def get_workspace_meta():
    import frappe
    meta = frappe.get_meta("Workspace")
    return {
        "autoname": meta.autoname,
        "fields": [f.fieldname for f in meta.fields if hasattr(f, "fieldname")],
        "mandatory": [f.fieldname for f in meta.fields if getattr(f, "reqd", 0)],
    }


def get_workspace_doc():
    import frappe
    name = "airplane_mode"
    if frappe.db.exists("Workspace", name):
        import json
        return json.dumps(frappe.get_doc("Workspace", name).as_dict(), default=str)
    return None


def print_workspace_doc():
    import frappe, json
    name = "airplane_mode"
    if frappe.db.exists("Workspace", name):
        print(json.dumps(frappe.get_doc("Workspace", name).as_dict(), default=str))
    else:
        print("Workspace not found")


def create_slug_workspace():
    """Create a workspace with label 'airplane_mode' (name will be 'airplane_mode') by copying the existing 'Airplane Mode' workspace."""
    import frappe
    src_name = "Airplane Mode"
    dst_label = "airplane_mode"
    if frappe.db.exists("Workspace", dst_label):
        return f"Workspace {dst_label} already exists"

    if not frappe.db.exists("Workspace", src_name):
        return f"Source workspace {src_name} not found"

    src = frappe.get_doc("Workspace", src_name)
    new = frappe.new_doc("Workspace")
    new.label = dst_label
    new.title = getattr(src, "title", src.label)
    new.module = getattr(src, "module", None)
    if hasattr(src, "public"):
        new.public = src.public
    if hasattr(src, "is_default"):
        new.is_default = src.is_default
    new.content = getattr(src, "content", None)
    new.links = getattr(src, "links", None)
    new.insert(ignore_permissions=True)
    return f"Created workspace {dst_label}"


def dump_airplane_workspaces():
    """Print workspace docs whose name or label contains 'airplane' (for debugging)."""
    import frappe, json
    results = []
    for w in frappe.get_all("Workspace", fields=["name", "label", "title"]):
        if (w.get("name") and "airplane" in w.get("name").lower()) or (w.get("label") and "airplane" in w.get("label").lower()):
            results.append(frappe.get_doc("Workspace", w.get("name")).as_dict())

    if results:
        print(json.dumps(results, default=str))
    else:
        print('No airplane workspaces found')
