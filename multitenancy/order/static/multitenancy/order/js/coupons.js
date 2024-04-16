$(document).ready(function() {
    // Initialize DataTable
    var table = $("#coupon-table").DataTable({
        ajax: {
            url: "/api/coupons",  // Replace with your API endpoint
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
            { data: "code" },
            { data: "discount" },
            { data: "start_date" },
            { data: "end_date" },
            { data: "usage_limit" },
            { data: "is_active" },
            { data: "minimum_order_amount" },
            { data: "redeem_by" },
            { data: "usage_count" },
            // { data: "valid_for.name" }  // Display related Product's name field
        ]
    });
});