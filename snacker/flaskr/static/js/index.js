/* Search snack given index's form */
function searchSnacks() {
    let snack_brand = document.getElementById("index_search_brand").value;
    window.console.log(snack_brand);
    let snack_name = document.getElementById("index_search_name").value;
    window.console.log(snack_name);
    let available_at_locations = document.getElementById("index_search_location").value;
    window.console.log(available_at_locations);
    window.console.log('fdssfd')
    window.location.href = "find_snacks/snack_name=" + snack_name + "+snack_brand=" + snack_brand +
        "+available_at_locations=" + available_at_locations;
}