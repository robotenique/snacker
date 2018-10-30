from flask_table import Col, Table


# TODO: remove after implementing the front end.
class SnackResults(Table):
    """
    Test class that helps to display the readable snacks data to the front end in the format of a table.
    It allows us to test the backend and html rendering, without having to wait for the implementation
    of the final front end.
    """
    id = Col('Snack Id')
    snack_name = Col('snack_name')
    available_at_locations = Col('Location')
    snack_brand = Col('Brand')
    snack_company_name = Col('Company Name')
    photo_files = Col('Photo')
    description = Col('Description')
    is_verified = Col('if verified')
    category = Col('Category')


# TODO: remove after implementing the front end.
class ReviewResults(Table):
    """
    Test class that helps to display the readable snacks data to the front end in the format of a table.
    It allows us to test the backend and html rendering, without having to wait for the implementation
    of the final front end.
    """
    id = Col('Review Id')
    user_id = Col('User ID')
    snack_id = Col('Snack ID')
    description = Col('Description')
    overall_rating = Col('Overall Rating')
    geolocation = Col('Geolocation')
