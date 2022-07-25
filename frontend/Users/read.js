
const api_url = "http://34.207.70.31:5000/emp";

async function getapi(url) {

    // Storing response
    const response = await fetch(url);
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}
// Calling that async function
getapi(api_url);

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
// Function to define innerHTML for HTML table
function show(data) {
    let tab =
        `<tr>
                <th>fullName</th>
                <th>telephoneNumber</th>
                <th>Age</th>
        </tr>`;

    // Loop to access all rows 
    for (let r of data) {
        tab += `<tr> 
                    <td>${r.fullName} </td>
                    <td>${r.telephoneNumber}</td>
                    <td>${r.Age}</td>        
                </tr>`;
    }
    // Setting innerHTML as tab variable
    document.getElementById("users").innerHTML = tab;
}
