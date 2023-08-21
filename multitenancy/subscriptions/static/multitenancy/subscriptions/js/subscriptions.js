$(document).ready(function () {
	// Initialize DataTable
	var table = $("#subscriptions-table").DataTable({
		ajax: {
			url: "/api/subscriptions/", // Replace with your API endpoint
			dataSrc: "", // Since the data is directly an array
		},
		paging: true,
		lengthChange: true,
		searching: true,
		ordering: true,
		info: true,
		autoWidth: false,
		responsive: true,
		columns: [
			{ data: "id" },
			{ data: "cycle" },
			{ data: "subscription_duration" },
			{ data: "start_date" },
			{ data: "end_date" },
			{ data: "created_date" },
			{ data: "renewal_date" },
			{ data: "reference" },
			// { data: "last_updated" },
			// { data: "product_type" },
			{ data: "reason" },
			{ data: "status" },
		],
	});
});
