let data = [];

    var table = new Tabulator("#invoice-table", {
        data: data,
        height: "300px",
        rowHeight: 40, //set rows to 40px height
        layout: "fitColumns",
        movableColumns: true,
        layoutColumnsOnNewData: true,
        columns: [
            {title: "ID", field: "id", width: 80, },
            {title: "Slug", field: "slug"},
            {title: "Name", field: "name"},
            {title: "Type", field: "type"},
            {title: "Date Create", field: "created"},
            {title: "Date Modified", field: "modified"},

        ],
    });
    async function getInvoices() {
        // gets the response from the api and put it inside a constant
        const response = await fetch('/api/billing/invoices');
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
    getInvoices()
    const form = document.getElementById("filter-form");
    // perfom a query then set new data
    form.addEventListener("keyup", async function(event) {
        const input = event.target;
        const value = input.value;
        const response = await fetch(`/api/billing/invoices/?q=${value}`);
        const data = await response.json();
        table.setData(data)
    });

    function updateDateRange() {
        var selectBox = document.getElementById("date-range");
        var selectedValue = selectBox.options[selectBox.selectedIndex].value;
      
        if (selectedValue === "") {
          return;
        }
      
        var endDate = new Date();
        var startDate = new Date(endDate);
        startDate.setDate(startDate.getDate() - parseInt(selectedValue));
      
        document.getElementById("date-range").value = "";
        document.getElementById("date-range").blur();
        alert("Start Date: " + startDate.toDateString() + "\nEnd Date: " + endDate.toDateString());
      }
      
      document.getElementById("date-range").addEventListener("change", updateDateRange);
      
