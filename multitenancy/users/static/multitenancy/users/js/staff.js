let data = [];

    var table = new Tabulator("#staff-table", {
        data: data,
        pagination:true, //enable.
        paginationSize:3, // this option can take any positive integer value
        height: "300px",
        rowHeight: 60, //set rows to 40px height
        layout: "fitColumns",
        movableColumns: true,
        layoutColumnsOnNewData: true,
        columns: [
            {title: "ID", field: "id", width: 60, },
            {title:"Avatar", field:"avatar",hozAlign:"center", width:80, formatter:function(cell, formatterParams){
                var value = cell.getValue();
                if (value == null) {
                    return `<img class="img-circle" src="http://www.gravatar.com/avatar/5d032fa2a3fe3be0f5b406fad098459c?s=100&d=mm" width="50"/>`;     
                } else {
                    return `<img class="img-circle" src="${value}" width="50"/>`;
                    
                 }
                 
             }},
            {title: "First Name", field: "first_name"},
            {title: "Last Name", field: "last_name"},
            {title: "Username", field: "username"},
            {title: "Email", field: "email"},
            {title: "Last Login", field: "last_login"},

        ],
    });
    async function getTemplates() {
        // gets the response from the api and put it inside a constant
        const response = await fetch('/api/staff/');
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
    getTemplates()
    const form = document.getElementById("filter-form");
    // perfom a query then set new data
    form.addEventListener("keyup", async function(event) {
        const input = event.target;
        const value = input.value;
        const response = await fetch(`/api/staff/?q=${value}`);
        const data = await response.json();
        table.setData(data)
    });