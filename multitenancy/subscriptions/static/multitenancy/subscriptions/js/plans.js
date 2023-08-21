$(document).ready(function () {
	// Initialize DataTable
	var table = $("#plans-table").DataTable({
		ajax: {
			url: "/api/plans", // Replace with your API endpoint
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
			{ data: "name" },
			{ data: "slug" },
			{ data: "description" },
			{ data: "price" },
			
		],
	});
});
