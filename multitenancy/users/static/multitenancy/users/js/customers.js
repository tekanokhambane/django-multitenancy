$(document).ready(function() {
    
	// Initialize DataTable
	var table = $("#customers-table").DataTable({
		ajax: {
			url: "/api/users/customers", // Replace with your API endpoint
			dataSrc: "", // Since the data is directly an array
		},
		paging: true,
		lengthChange: true,
		searching: true,
		ordering: true,
		info: true,
		autoWidth: false,
        responsive: true,
        buttons: [
            { extend: 'create',  },
            { extend: 'edit',  },
            { extend: 'remove',  }
        ],
		columns: [
			{ data: "id" },
			
			{ data: "first_name" },
			{ data: "last_name" },
			{ data: "username" },
			{ data: "email" },
			{ data: "last_login" },
			
		],
	});
});