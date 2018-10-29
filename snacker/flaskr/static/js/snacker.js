/* Search snack given index's form */
function searchSnacks() {
    let snack_brand = document.getElementById("index_search_brand").value;
    let snack_name = document.getElementById("index_search_name").value;
    let available_at_locations = document.getElementById("index_search_location").value;
    window.location.href = "find_snacks/snack_name=" + snack_name + "+snack_brand=" + snack_brand +
        "+available_at_locations=" + available_at_locations;
}

function indexRegister() {
    let email = document.getElementById("index_email").value;;
    let interval = 10; // ms
    window.location.href = "register";
    window.setTimeout(function() {
        if (window.location.href.includes("register")) {
            setEmail(email)
        } else {
            window.setTimeout(arguments.callee, interval);
        }
    }, interval);
}

// This is not working, the email user inputs in index won't go to register at this point
function setEmail(email) {
    console.log(email);
    document.getElementById("register_email").value = email;
}