"""logs Views."""
from annoying.decorators import render_to


@render_to("logs/index.html")
def index(request):
    """Return the main page."""
    number_of_logs = 0
    number_of_ships = 0
    # For the students
    return {
        'number_of_logs': number_of_logs,
        'number_of_ships': number_of_ships,
    }
