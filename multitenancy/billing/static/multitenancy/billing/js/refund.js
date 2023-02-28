let data = [];

    var table = new Tabulator("#refunds-table", {
        data: data,
        height: "300px",
        rowHeight: 40, //set rows to 40px height
        layout: "fitColumns",
        movableColumns: true,
        layoutColumnsOnNewData: true,
        columns: [
            {title: "ID", field: "id", width: 80, },
            {title: "Invoice", field: "invoice"},
            {title: "Amount", field: "amount"},
            {title: "Date", field: "date"},
            {title: "Reason", field: "reason"},
             

        ],
    });
    async function getRefunds() {
        // gets the response from the api and put it inside a constant
        const response = await fetch('/api/billing/refunds');
        //the response have to be converted to json type file, so it can be used
        const data = await response.json();
        //the addData adds the object "data" to an array
        addData(data)


        table.setData(data)
    }

    function addData(object) {
        // the push method add a new item to an array
        // here it will be adding the object from the function getRandomUser each time it is called
        data.push(object);
        //the fetched data is available only on this scope

    }

    //Calls the function that fetches the data
    getRefunds()
    const form = document.getElementById("filter-form");
    // perfom a query then set new data
    form.addEventListener("keyup", async function(event) {
        const input = event.target;
        const value = input.value;
        const response = await fetch(`/api/billing/refunds/?q=${value}`);
        const data = await response.json();
        table.setData(data)
    });