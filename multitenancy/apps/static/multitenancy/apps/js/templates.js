$(document).ready(function() {
    // Initialize DataTable
    var table = $("#templates-table").DataTable({
        ajax: {
            url: "/api/templates",  // Replace with your API endpoint
            dataSrc: ""  // Since the data is directly an array
        },
        paging: true,
        lengthChange: true,
        searching: true,
        ordering: true,
        info: true,
        // dom: 'Bfrtip',
        buttons: [
            'copy', 'excel', 'pdf'
        ],
        autoWidth: false,
        responsive: true,
        columns: [
            { data: "id" },
            { data: "name" },
            { data: "type" },
            { data: "description" },
            { data: "created" },
            { data: "modified" }
        ]
    });


});

