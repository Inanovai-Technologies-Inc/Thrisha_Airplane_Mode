(function () {
	const AIRPLANE_ITEMS = ["Airplane Mode", "Airline Operations", "Airport Shops"];

	function is_airplane_mode() {
		const route = frappe.get_route();

		if (!route || route[0] !== "Workspaces") {
			return false;
		}

		const workspace = (route[1] || "").toLowerCase();

		return ["airplane mode", "airline operations", "airport shops"].includes(
			workspace.replace(/-/g, " ")
		);
	}

	function update_airplane_sidebar() {
		const airplane_mode = is_airplane_mode();

		document.querySelectorAll(".sidebar-item-container").forEach((container) => {
			const name = container.getAttribute("item-name");

			if (!name) {
				return;
			}

			if (airplane_mode) {
				if (AIRPLANE_ITEMS.includes(name)) {
					container.style.setProperty("display", "block", "important");
				} else {
					container.style.setProperty("display", "none", "important");
				}
			} else {
				if (AIRPLANE_ITEMS.includes(name)) {
					container.style.setProperty("display", "none", "important");
				} else {
					container.style.removeProperty("display");
				}
			}
		});
	}

	function update_airplane_logo() {
		const navbar_home = document.querySelector(".navbar-home");

		if (!navbar_home) {
			return;
		}

		const logo = navbar_home.querySelector(".app-logo");

		if (!logo) {
			return;
		}

		const airplane_logo = "/assets/airplane_mode/icons/airplane.svg";
		const frappe_logo = "/assets/frappe/images/frappe-framework-logo.svg";

		if (is_airplane_mode()) {
			if (navbar_home.getAttribute("href") !== "/app/airplane-mode") {
				navbar_home.setAttribute("href", "/app/airplane-mode");
			}

			if (logo.getAttribute("src") !== airplane_logo) {
				logo.setAttribute("src", airplane_logo);
			}

			logo.setAttribute("alt", "Airplane Mode");
		} else {
			if (navbar_home.getAttribute("href") !== "/app") {
				navbar_home.setAttribute("href", "/app");
			}

			if (logo.getAttribute("src") !== frappe_logo) {
				logo.setAttribute("src", frappe_logo);
			}

			logo.setAttribute("alt", "Frappe Framework");
		}
	}

	function refresh_sidebar() {
		setTimeout(() => {
			update_airplane_sidebar();
			update_airplane_logo();
		}, 100);
	}

	refresh_sidebar();

	$(document).on("page-change", refresh_sidebar);

	const observer = new MutationObserver(function () {
		refresh_sidebar();
	});

	observer.observe(document.body, {
		childList: true,
		subtree: true,
	});
})();
