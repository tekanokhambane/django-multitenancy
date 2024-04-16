$(document).ready(function() {
    // Initialize DataTable
    var table = $("#payments-table").DataTable({
        ajax: {
            url: "/api/billing/payments",  // Replace with your API endpoint
            dataSrc: ""  // Since the data is directly an array
        },
        paging: true,
        lengthChange: true,
        searching: true,
        ordering: true,
        info: true,
        autoWidth: false,
        responsive: true,
        columns: [
            { data: "subscriber.username" },  // Display related User's username field
            { data: "amount" },
            { data: "gateway.name" },  // Display related PaymentGateWay's name field
            { data: "status" }
        ]
    });
});
