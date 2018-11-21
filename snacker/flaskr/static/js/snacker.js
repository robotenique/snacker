/* Search snack given index's form */
function searchSnacks() {
    let snack_brand = document.getElementById("index_search_brand").value;
    let snack_name = document.getElementById("index_search_name").value;
    let available_at_locations = document.getElementById("index_search_location").value;
    window.location.href = "find_snacks/snack_name=" + snack_name + "+snack_brand=" + snack_brand +
        "+available_at_locations=" + available_at_locations;
}

function indexRegister() {
    let email = document.getElementById("index_email").value;
    window.location.href = "register?email=" + email
}

/*Login the user*/
function authenticate() {
    console.log(document.getElementById("login_email").value);
    $.ajax({
        type: "POST",
        url: "/login",
        data: {
            "email": document.getElementById("login_email").value,
            "password": document.getElementById("login_password").value
        },
        dataType: "json",
        success: function (result) {
            console.log(result);
            window.location.href = "index";
        },
        error: function (result) {
            alert('invalid username or password');
        }
    });
}

/*Login the user*/
function register_user() {
    console.log(document.getElementById("register_company").value);
    $.ajax({
        type: "POST",
        url: "/register",
        data: {
            "email": document.getElementById("register_email").value,
            "password": document.getElementById("register_password").value,
            "company_name": document.getElementById("register_company").value,
            "first_name": document.getElementById("register_first").value,
            "last_name": document.getElementById("register_last").value,
        },
        dataType: "json",
        success: function (result) {
            console.log(result);
            window.location.href = "index";
        },
        error: function (result) {
            alert('Something wrong ' + result);
        }
    });
}

function createSnack() {
    if (document.getElementById("available_at_location").value != "Nothing Selected") {
        $.ajax({
            type: "POST",
            url: "/create-snack",
            data: {
                "snack_name": document.getElementById("snack_name").value,
                "available_at_locations": document.getElementById("available_at_location").value,
                "snack_brand": document.getElementById("snack_brand").value,
                "category": document.getElementById("category").value,
                "description": document.getElementById("description").value,
            },
            success: function (result) {
                window.location.href="index";
            },
            error: function (result) {
                alert('Something wrong ' + result);
            }
        });
    } else {
        $.getJSON( "https://ipapi.co/json/", function( data ) {
            $.ajax({
                type: "POST",
                url: "/create-snack",
                data: {
                    "snack_name": document.getElementById("snack_name").value,
                    "available_at_locations": data.country_name,
                    "snack_brand": document.getElementById("snack_brand").value,
                    "category": document.getElementById("category").value,
                    "description": document.getElementById("description").value,
                },
                success: function (result) {
                    window.location.href="index";
                },
                error: function (result) {
                    alert('Something wrong ' + result);
                }
            });
        });
    }
}

function createReview() {
    // Otherwise the country of the IP address of the user is added to the list of available locations for this snack
    $.getJSON( "https://ipapi.co/json/", function( data ) {
        $.ajax({
            type: "POST",
            url: "/create-review/snack_id=" + window.location.href.toString().split('=')[1],
            data: {
                "description": document.getElementById("description").value,
                "review_country": data.country_name,
                "overall_rating": document.getElementById("overall_rating").value,
                "sourness": document.getElementById("sourness").value,
                "spiciness": document.getElementById("spiciness").value,
                "saltiness": document.getElementById("saltiness").value,
                "bitterness": document.getElementById("bitterness").value,
                "sweetness": document.getElementById("sweetness").value,
            },
            success: function (result) {
                window.location.href= "/snack_reviews/snack_id=" + window.location.href.toString().split("=")[1];
            },
            error: function (result) {
                alert('Something wrong ' + result);
            }
        });
    });
}