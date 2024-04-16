$(document).ready(function () {
	// Initialize DataTable
	var table = $("#product-type-table").DataTable({
		ajax: {
			url: "/api/product-types", // Replace with your API endpoint
			dataSrc: "", // Since the data is directly an array
		},
		paging: false,
		lengthChange: true,
		searching: true,
		ordering: true,
		info: true,
		autoWidth: false,
		responsive: true,
		columns: [
			{ data: "id" },
			{ data: "name" },
			
			
		],
	});
});
