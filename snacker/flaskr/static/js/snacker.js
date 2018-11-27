/* Search snack given index's form */
function searchSnacks(query) {
    let snack_brand = query.index_search_brand.value;
    let snack_name = query.index_search_name.value;
    let available_at_locations = query.index_search_location.value;
    window.location.href = "find_snacks/snack_name=" + snack_name + "+snack_brand=" + snack_brand +
        "+available_at_locations=" + available_at_locations;
}

function indexRegister(form) {
    let email = form.email.value;
    window.location.href = "register?email=" + email
}

/*Login the user*/
function authenticate(form) {
    console.log(form.login_email.value);
    $.ajax({
        type: "POST",
        url: "/login",
        data: {
            "email": form.login_email.value,
            "password": form.login_password.value
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
function register_user(form) {
    console.log(form.register_company.value);
    $.ajax({
        type: "POST",
        url: "/register",
        data: {
            "email": form.register_email.value,
            "password": form.register_password.value,
            "company_name": form.register_company.value,
            "first_name": form.register_first.value,
            "last_name": form.register_last.value,
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

function createSnack(form, selected_snack_brand) {
    // A snack submission should always create a snack regardless of the ip API status
    var location = form.available_at_location.value;
    $.getJSON( "https://ipapi.co/json/", function( data ) {})
        .always( function( data ) {
            $.ajax({
                type: "POST",
                url: "/create-snack/selected_brand=" + selected_snack_brand,
                data: {
                    "snack_name": form.snack_name.value,
                    "available_at_locations": (location != "Nothing Selected" ? location
                                                : data ? data.country_name
                                                : null),
                    "snack_brand": form.snack_brand.value,
                    "category": form.category.value,
                    "description": form.description.value,
                },
                success: function (result) {
                    window.location.replace("/index");
                },
                error: function (result) {
                    alert('Something wrong ' + result);
                }
            });
        });
}

function createReview(form, snack_id) {
    // A review submission should always create a review regardless of the ip API status
    $.getJSON( "https://ipapi.co/json/", function() {})
        .always( function( data ) {
            $.ajax({
                type: "POST",
                url: "/create-review/snack_id=" + snack_id,
                data: {
                    "description": form.description.value,
                    "review_country": (data ? data.country_name : null),
                    "overall_rating": form.overall_rating.value,
                    "sourness": form.sourness.value,
                    "spiciness": form.spiciness.value,
                    "saltiness": form.saltiness.value,
                    "bitterness": form.bitterness.value,
                    "sweetness": form.sweetness.value,
                },
                success: function (result) {
                    window.location.href="/snack_reviews/snack_id="+snack_id
                },
                error: function (result) {
                    alert('Something wrong ' + result);
                }
            });
        });
}

function verify_snack(snack_id) {
    console.log(snack_id);
    $.ajax({
        type: "POST",
        url: "/verify-snack",
        data: {
            "snack_id": snack_id
        },
        dataType: "json",
        success: function (result) {
            alert("Snack verified!");
            window.location.href="/snack_reviews/snack_id="+snack_id;
        },
        error: function (result) {
            alert('Something wrong ' + result);
        }
    });
}
function get_current_url(){
    var url=window.location.href;
    return url
    }

function add_to_fav(snack_id) {

    var prev_url = window.location.href;

    console.log(snack_id);
    $.ajax({
        type: "POST",
        url: "/add_to_fav",
        data: {
            "snack_id": snack_id,
            "prev_url": prev_url,
            "test":"test"
        },
        dataType: "json",
        success: function (result) {
            alert("Snack added to favourite!");
        },
        error: function (result) {
            alert("snacker added to fav");
        }
    });
}
