frappe.listview_settings['Lost Baggage Request'] = {
    get_indicator: function (doc) {

        if (doc.status === 'Submitted') {
            return [__('Submitted'), 'orange', 'status,=,Submitted'];
        }

        if (doc.status === 'Under Investigation') {
            return [__('Under Investigation'), 'blue', 'status,=,Under Investigation'];
        }

        if (doc.status === 'Baggage Located') {
            return [__('Baggage Located'), 'green', 'status,=,Baggage Located'];
        }

        if (doc.status === 'Ready for Delivery') {
            return [__('Ready for Delivery'), 'orange', 'status,=,Ready for Delivery'];
        }

        if (doc.status === 'Delivered') {
            return [__('Delivered'), 'green', 'status,=,Delivered'];
        }

        if (doc.status === 'Closed') {
            return [__('Closed'), 'grey', 'status,=,Closed'];
        }
    }
};