const csrftoken = Cookies.get('csrftoken');


$(document).ready(function () {

	// Initialize DataTable
	var table = $("#staff-table").DataTable({
		ajax: {
			url: "/api/users/staff", // Replace with your API endpoint
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
			{ extend: 'create', },
			{ extend: 'edit', },
			{ extend: 'remove', }
		],
		columns: [
			{ data: "id" },
			{
				data: "avatar", render: function (data, type, row) {
					// Custom rendering logic for the cell
					if (data == null) {
						return `<img class="img-circle bg-dark" src="http://www.gravatar.com/avatar/5d032fa2a3fe3be0f5b406fad098459c?s=100&d=mm" width="50" height="50"/>`;
					} else {
						return `<img class="img-circle bg-dark" src="${data}" width="50" height="50"/>`;

					}
				}
			},
			{ data: "first_name" },
			{ data: "last_name" },
			{ data: "username" },
			{ data: "email" },
			{ data: "last_login" },

		],
	});
});

var emailInput = document.getElementById("id_email");

$("#invite-user-button").on("click", function () {
	let formData = new FormData();
	formData.append("email", emailInput.value);
	fetch("/admin/staff/users/invite/", {
		method: "POST",
		headers: {
			"X-CSRFToken": csrftoken,
		},
		body: formData,
	}).then(response => {
		if (response.ok) {
			console.log("User invited successfully!");
			$("#modal-default").modal("hide");
			table.ajax.reload();
		} else {
			console.log("Failed to invite user.");
		}
	})

})
