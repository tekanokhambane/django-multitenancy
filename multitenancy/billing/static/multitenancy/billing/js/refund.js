$(document).ready(function () {
	// Initialize DataTable
	var table = $("#refunds-table").DataTable({
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
			{ data: "invoice" },
			{ data: "amount" },
			{ data: "date" },
			{ data: "reason" },
			
		],
	});
});

