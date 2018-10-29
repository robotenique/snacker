$( document ).ready(function() {
    if (window.sessionStorage.getItem("email")) {
        document.getElementById("if_account").innerText = "Account";
        document.getElementById('account_link').setAttribute('href', 'account');
        document.getElementById("join_us").style.display = "none";
    }
});

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

/*Login the user*/
function authenticate() {
    console.log(document.getElementById("login_email").value);
    $.ajax({
        type: "POST",
        url:"/login",
        data: {
            "email": document.getElementById("login_email").value,
            "password": document.getElementById("login_password").value
        },
        dataType:"json",
        success: function(result){
            console.log(result);
            window.sessionStorage.setItem("email", result.email);
            window.sessionStorage.setItem("first_name", result.first_name);
            window.sessionStorage.setItem("last_name", result.last_name);
            window.location.href = "index";
        },
        error: function(result) {
            alert('invalid username or password');
        }
    });
}

/*Login the user*/
function register_user() {
    console.log(document.getElementById("register_email").value);
    $.ajax({
        type: "POST",
        url:"/register",
        data: {
            "email": document.getElementById("register_email").value,
            "password": document.getElementById("register_password").value,
            "first_name": document.getElementById("register_first").value,
            "last_name": document.getElementById("register_last").value,
        },
        dataType:"json",
        success: function(result){
            console.log(result);
            window.sessionStorage.setItem("email", result.email);
            window.sessionStorage.setItem("first_name", result.first_name);
            window.sessionStorage.setItem("last_name", result.last_name);
            window.location.href = "index";
        },
        error: function(result) {
            alert('Something wrong ' + result);
        }
    });
}