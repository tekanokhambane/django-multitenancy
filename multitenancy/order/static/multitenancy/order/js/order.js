$(document).ready(function() {
    // Initialize DataTable
    var table = $("#orders-table").DataTable({
        ajax: {
            url: "/api/orders",  // Replace with your API endpoint
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
            { data: "user" },
            { data: "date_created" },
            { data: "order_number" },
            { data: "amount" },
            { data: "status" },
            { data: "payment_method" },
            { data: "billing_address" },
            { data: "notes" },
            { data: "coupon" }
        ]
    });
});