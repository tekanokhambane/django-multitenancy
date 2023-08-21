$(document).ready(function () {
	// Initialize DataTable
	var table = $("#invoice-table").DataTable({
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
			{ data: "subscription" },
			{ data: "date_created" },
			{ data: "due_date" },
			{ data: "invoice_number" },
			{ data: "amount" },
			{ data: "credit_used" },
			{ data: "payment_method" },
			// { data: "last_updated" },
			// { data: "product_type" },
			{ data: "status" },
		],
	});
});


