$(document).ready(function() {
    // Initialize DataTable
    var table = $("#payment-gateway-table").DataTable({
        ajax: {
            url: "/api/billing/payment-gateways",  // Replace with your API endpoint
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
            { data: "name" },
            { data: "description" },
            { data: "status" },
            { data: "default" }
        ]
    });
});