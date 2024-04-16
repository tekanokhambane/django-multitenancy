$(document).ready(function () {
	// Initialize DataTable
	var table = $("#credits-table").DataTable({
		ajax: {
			url: "/api/billing/invoices", // Replace with your API endpoint
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
			{ data: "customer" },
			{ data: "amount" },
			{ data: "created_at" },
			{ data: "updated_at" },
		
		],
	});
});


