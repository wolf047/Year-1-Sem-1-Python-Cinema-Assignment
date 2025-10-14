# One-time usage: to generate seat layout, with aisle spaces added manually
# def generate_seat_layout():
#     rows = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     with open("Cinema/Database/auditorium_info.txt", "r") as f:
#         next(f)
#         for line in f:
#             entry = [i.strip() for i in line.strip().split(",")]
#             auditorium_id = entry[0]
#             with open("Cinema/Database/auditorium_sitting.txt", "a") as g:
#                 g.write(auditorium_id + "\n")
#             for i in range(int(entry[3]) + 1):
#                 row_seats = []
#                 row = rows[i]
#                 for j in range(1, (int(entry[4]) + 1)):
#                     column = j
#                     seat

from datetime import datetime, timedelta
import time
import os

# File names - Change these if your files have different names
MOVIE_FILE = "Cinema/Database/movie_listings.txt"
SHOWTIME_FILE = "Cinema/Database/movie_showtimes.txt"
BOOKING_FILE = "Cinema/Database/movie_bookings.txt"
AUDITORIUM_FILE = "Cinema/Database/auditorium_info.txt"


def view_movies():
    """Show all movies"""
    print("\n========== AVAILABLE MOVIES ==========")

    file = open(MOVIE_FILE, 'r')
    lines = file.readlines()
    file.close()

    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue

        parts = lines[i].split(',')
        movie_id = parts[0].strip()
        movie_name = parts[1].strip().replace('"', '')
        genre = parts[4].strip()

        print(f"{movie_id} - {movie_name} ({genre})")

    print("=" * 40)


def view_auditoriums():
    """Show all auditoriums"""
    print("\n========== AUDITORIUMS ==========")

    file = open(AUDITORIUM_FILE, 'r')
    lines = file.readlines()
    file.close()

    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue

        parts = lines[i].split(',')
        audi_id = parts[0].strip()
        audi_type = parts[1].strip()
        capacity = parts[2].strip()
        price = parts[5].strip()

        print(f"{audi_id} - {audi_type} Hall | Capacity: {capacity} | Price: RM{price}")

    print("=" * 40)


def view_showtimes():
    """Show all showtimes"""
    print("\n========== MOVIE SHOWTIMES ==========")

    file = open(SHOWTIME_FILE, 'r')
    lines = file.readlines()
    file.close()

    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue

        parts = lines[i].split(',')
        showtime_id = parts[0].strip()
        movie_id = parts[1].strip()
        audi_id = parts[2].strip()
        date = parts[3].strip()
        start = parts[4].strip()

        print(f"{showtime_id}: Movie {movie_id} | Hall {audi_id} | {date} at {start}")

    print("=" * 40)


def view_bookings():
    """Show all bookings"""
    print("\n========== ALL BOOKINGS ==========")

    file = open(BOOKING_FILE, 'r')
    lines = file.readlines()
    file.close()

    count = 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue

        parts = lines[i].split(',')
        booking_id = parts[0].strip()
        movie_id = parts[1].strip()
        customer_id = parts[3].strip()
        seats = parts[4].strip()

        print(f"{booking_id}: Movie {movie_id} | Customer {customer_id} | Seats: {seats}")
        count = count + 1

    if count == 0:
        print("No bookings yet.")

    print("=" * 40)


def book_ticket():
    """Book a new ticket"""
    print("\n========== BOOK TICKET ==========")

    view_movies()
    view_auditoriums()
    view_showtimes()

    # Get booking info
    print("\nEnter details:")
    movie_id = input("Movie ID: ")
    auditorium_id = input("Auditorium ID: ")
    showtime_id = input("Showtime ID: ")
    customer_id = input("Customer ID: ")
    seats = input("Seats (A1 or A1|A2): ")
    tickets = input("Tickets (normal|discount like 1|0): ")

    # Check all fields filled
    if not movie_id or not auditorium_id or not showtime_id or not customer_id or not seats or not tickets:
        print("\nERROR: Fill all fields!")
        return

    # Check tickets format
    if "|" not in tickets:
        print("\nERROR: Tickets must be like 1|0 or 2|1")
        return

    # Count seats
    if "|" in seats:
        seat_list = seats.split('|')
        total_seats = len(seat_list)
    else:
        seat_list = [seats]
        total_seats = 1

    # Count tickets
    ticket_parts = tickets.split('|')
    normal = int(ticket_parts[0])
    discount = int(ticket_parts[1])
    total_tickets = normal + discount

    # Check seats = tickets
    if total_seats != total_tickets:
        print(f"\nERROR: {total_seats} seats but {total_tickets} tickets!")
        return

    # Check for duplicate seats
    file = open(BOOKING_FILE, 'r')
    lines = file.readlines()
    file.close()

    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue
        parts = lines[i].split(',')
        if len(parts) < 5:
            continue

        booked_showtime = parts[2].strip()
        if booked_showtime == showtime_id:
            booked_seats = parts[4].strip()
            if "|" in booked_seats:
                already_booked = booked_seats.split('|')
            else:
                already_booked = [booked_seats]

            for seat in seat_list:
                if seat.strip() in [s.strip() for s in already_booked]:
                    print(f"\nERROR: Seat {seat} already booked!")
                    return

    # Get price from showtime file
    file = open(SHOWTIME_FILE, 'r')
    lines = file.readlines()
    file.close()

    normal_price = None
    discount_price = None

    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue
        parts = lines[i].split(',')
        if parts[0].strip() == showtime_id:
            # Column 6 = normal_price, Column 7 = discounted_price
            normal_price = float(parts[6].strip())
            discounted_price_str = parts[7].strip()

            # If discounted_price is empty or 0.00, no discount available
            if discounted_price_str != "" and float(discounted_price_str) > 0:
                discount_price = float(discounted_price_str)
            else:
                discount_price = normal_price
            break

    # Check if showtime was found
    if normal_price is None:
        print(f"\nERROR: Showtime {showtime_id} not found!")
        return

    total_price = (normal * normal_price) + (discount * discount_price)

    # Generate booking ID
    file = open(BOOKING_FILE, 'r')
    lines = file.readlines()
    file.close()

    booking_count = len(lines) - 1
    booking_id = f"B{booking_count + 1:03d}"

    # Show summary
    print("\n========== SUMMARY ==========")
    print(f"Booking ID: {booking_id}")
    print(f"Movie: {movie_id}")
    print(f"Hall: {auditorium_id}")
    print(f"Showtime: {showtime_id}")
    print(f"Seats: {seats}")
    print(f"Normal: {normal} x RM{normal_price:.2f}")
    print(f"Discount: {discount} x RM{discount_price:.2f}")
    print(f"TOTAL: RM{total_price:.2f}")
    print("=" * 30)

    confirm = input("\nConfirm? (Y/N): ")
    if confirm.upper() != "Y":
        print("Cancelled.")
        return

    # Save booking
    file = open(BOOKING_FILE, 'a')
    file.write(
        f"{booking_id}, {movie_id}, {showtime_id}, {customer_id}, {seats}, {tickets}, {total_price:.2f}, {auditorium_id}\n")
    file.close()

    print("\n✓ Booking successful!")
    print(f"Booking ID: {booking_id}")


def cancel_booking():
    """Cancel a booking"""
    print("\n========== CANCEL BOOKING ==========")

    view_bookings()

    booking_id = input("\nBooking ID to cancel: ")
    if not booking_id:
        print("ERROR: Enter booking ID!")
        return

    # Read all bookings
    file = open(BOOKING_FILE, 'r')
    lines = file.readlines()
    file.close()

    found = False
    new_lines = [lines[0]]

    for i in range(1, len(lines)):
        if lines[i].strip() == "":
            continue

        parts = lines[i].split(',')
        if parts[0].strip() == booking_id:
            found = True
            print(f"\nFound: {lines[i].strip()}")

            confirm = input("Cancel? (Y/N): ")
            if confirm.upper() == "Y":
                print(f"\n✓ Booking {booking_id} cancelled!")
            else:
                new_lines.append(lines[i])
                print("Cancelled.")
        else:
            new_lines.append(lines[i])

    if not found:
        print(f"ERROR: Booking {booking_id} not found!")
        return

    # Save updated bookings
    file = open(BOOKING_FILE, 'w')
    file.writelines(new_lines)
    file.close()


def main_ticketing_clerk():
    """Main program"""
    print("=" * 50)
    print("   CINEMA TICKETING SYSTEM")
    print("=" * 50)

    while True:
        print("\n========== MENU ==========")
        print("1. View Movies")
        print("2. View Auditoriums")
        print("3. View Showtimes")
        print("4. Book Ticket")
        print("5. View Bookings")
        print("6. Cancel Booking")
        print("7. Exit")
        print("=" * 27)

        choice = input("\nChoice (1-7): ")

        if choice == "1":
            view_movies()
        elif choice == "2":
            view_auditoriums()
        elif choice == "3":
            view_showtimes()
        elif choice == "4":
            book_ticket()
        elif choice == "5":
            view_bookings()
        elif choice == "6":
            cancel_booking()
        elif choice == "7":
            print("\nGoodbye!")
            main()
        else:
            print("ERROR: Choose 1-7")

        input("\nPress Enter...")






RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

AUDITORIUM_OPTIONS = ["AUD01", "AUD02", "AUD03", "AUD04", "AUD05", "AUD06", "AUD07", "AUD08"]
CLASSIFICATION_OPTIONS = ["U", "P12", "13", "16", "18+", "18SG", "18SX"]
BUFFER = timedelta(minutes=15)

MOVIE_CONFIRMATION_KEYS = ["Movie Name", "Release Date", "Running Time", "Genre", "Classification", "Spoken language", "Subtitle language", "Directors", "Casts", "Description", "Eligibility for discount"]
SHOWTIME_CONFIRMATION_KEYS = ["Movie ID", "Auditorium ID", "Date", "Start Time", "End Time", "Normal Price", "Discounted Price", "Discount ID"]
DISCOUNT_CONFIRMATION_KEYS = ["Discount Name", "Discount Type", "Discount Amount", "Discount Rate", "Discount Policies"]


def color_error_message(message):
    """
    Wraps a string with ANSI escape codes to display it in red.

    Args:
        message (str): The error message to be colorized.

    Returns:
        str: The error message wrapped with red color and reset codes.
    """
    colored_message = RED + message + RESET
    return colored_message


def color_completion_message(message):
    """
    Wraps a string with ANSI escape codes to display it in green.

    Args:
        message (str): The completion message to be colorized.

    Returns:
        str: The completion message wrapped with green color and reset codes.
    """
    colored_message = GREEN + message + RESET
    return colored_message


def color_confirmation_message(message):
    """
    Wraps a string with ANSI escape codes to display it in blue.

    Args:
        message (str): The confirmation message to be colorized.

    Returns:
        str: The confirmation message wrapped with blue color and reset codes.
    """
    colored_message = BLUE + message + RESET
    return colored_message


def clear_terminal():
    """Clears the terminal screen.

    Returns:
        None
    """
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For macOS and Linux
    else:
        _ = os.system("clear")


def validate_yes_no(prompt):
    """
    Ensures that input is either Y or N.

    Args:
        prompt (str): Input prompt shown to the user.

    Returns:
        str: "Y or "N" entered by the user.
    """
    while True:
        value = input(prompt).upper().strip()
        if value in ("Y", "N"):
            return value
        print(color_error_message("Invalid input: please enter 'Y' or 'N'."))


def validate_int(prompt):
    """
    Ensures that input is an integer.

    Args:
        prompt (str): Input prompt shown to the user.

    Returns:
        int: Integer entered by the user.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            return value
        except ValueError:
            print(color_error_message("Invalid input: please enter an integer."))


def validate_float(prompt):
    """
    Ensures that input is a float and rounds it to two decimal places.

    Args:
        prompt (str): Input prompt shown to the user.

    Returns:
        float: Float entered by the user, rounded to two decimal places.
    """
    while True:
        try:
            value = round(float(input(prompt).strip()), 2)
            return value
        except ValueError:
            print(color_error_message("Invalid input: please enter a float to 2 decimal places (e.g., 0.00)."))


def validate_date(prompt):
    """
    Ensures that input is a date formatted as DD-MM-YYYY.

    Args:
        prompt (str): Input prompt shown to the user.

    Returns:
        str: Date entered by the user, formatted as DD-MM-YYYY.
    """
    while True:
        try:
            value = datetime.strptime(input(prompt).strip(), "%d-%m-%Y")
            return value.strftime("%d-%m-%Y")
        except ValueError:
            print(color_error_message("Invalid input: please enter a date in the format DD-MM-YYYY (e.g., 31-12-2000)."))


def validate_time(prompt):
    """
    Ensures that input is a time formatted as HHMM.

    Args:
        prompt (str): Input prompt shown to the user.

    Returns:
        str: Time entered by the user, formatted as HHMM.
    """
    while True:
        try:
            value = datetime.strptime(input(prompt).strip(), "%H%M")
            return value.strftime("%H%M")
        except ValueError:
            print(color_error_message("Invalid input: please enter a time in the format HHMM (e.g., 2359)."))


def lint_item(value):
    """
    Formats a list or string to be entered in text file.

    Args:
        value (Any): Item to be formatted. Lists are joined with "|". Joined lists or strings are wrapped in quotation marks if they contain a comma or space.

    Returns:
        str: Formatted string.
    """
    if isinstance(value, list):
        value = "|".join(value)
    value = str(value).strip()
    return f'"{value}"' if "," in value or " " in value else value


def add_entry(filename, entry_detail_list):
    """
    Adds a formatted entry to a text file.

    Args:
        filename (str): Path to the file where the entry is to be added.
        entry_detail_list (list): List of items to be formatted and written as a single line.

    Returns:
        None
    """
    with open(filename, "r") as f:
        first_line = f.readline()
        single_line = not first_line.endswith("\n")
    with open(filename, "a") as f:
        if single_line:
            f.write("\n")
        formatted_entry = []
        for item in entry_detail_list:
            formatted_entry.append(lint_item(item))
        f.write(", ".join(formatted_entry) + "\n")


def update_entry(filename, entry_id, detail_index, entry_detail_item):
    """
    Updates a specific field in an entry within a text file.

    Args:
        filename (str): Path to the file containing the entry.
        entry_id (str): ID of the entry to be updated.
        detail_index (int): Index of the field within the entry to be updated.
        entry_detail_item (Any): New value to replace the existing one.

    Returns:
        None
    """
    with open(filename, "r") as f:
        entries = f.readlines()
        updated_entries = []
        for entry in entries:
            entry = [i.strip() for i in entry.split(",")]
            if entry[0] == entry_id:
                entry[detail_index] = lint_item(entry_detail_item)
            updated_entries.append(", ".join(entry) + "\n")
    with open(filename, "w") as f:
        f.writelines(updated_entries)


def remove_entry(filename, entry_id):
    """
    Removes a specific entry within a text file.

    Args:
        filename (str): Path to the file containing the entry.
        entry_id (str): ID of the entry to be removed.

    Returns:
        None
    """
    with open(filename, "r") as f:
        entries = f.readlines()
        updated_entries = []
        for entry in entries:
            entry = [i.strip() for i in entry.split(",")]
            if entry[0] != entry_id:
                updated_entries.append(", ".join(entry) + "\n")
    with open(filename, "w") as f:
        f.writelines(updated_entries)


def view_all_entries(filename):
    """
    Displays all entries from a text file.

    Args:
        filename (str): Path to the file containing the entries.

    Returns:
        None
    """
    with open(filename, "r") as f:
        header = f.readline().upper()
        print(header, end="")
        print("-" * len(header))
        entries = f.readlines()
        if not entries:
            print("No entries found.")
        else:
            for entry in entries:
                print(entry, end="")
            print("\n")


def lookup_entry(filename, entry_id="", header=0):
    """
    Retrieves either the header or a specific entry from a text file.

    Args:
        filename (str): Path to the file containing entry.
        entry_id (str, optional): ID of the entry to be retrieved. Defaults to "".
        header (int, optional): If set to 1, returns the header row instead of searching for an entry. If set to 0, searches for an entry. Defaults to 0.

    Returns:
        list or None: Header or matching entry, or None if not found.
    """
    with open(filename, "r") as f:
        if header:
            details = [detail.strip() for detail in f.readline().split(",")]
            return details
        for line in f:
            entry = [i.strip() for i in split_line(line)]
            if entry[0] == entry_id:
                return entry
    return None


def split_line(line):
    """
    Splits a line into fields using comma as separator, while refraining from splitting when wrapped in double quotation marks.

    Args:
        line (str): The line to be split.
    
    Returns:
        fields (list): A list of the fields that makes up the line.
    """
    fields = []
    placeholder = ''
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
            placeholder += char
        elif char == ',' and not in_quotes:
            fields.append(placeholder.strip())
            placeholder = ''
        else:
            placeholder += char
    if placeholder:
        fields.append(placeholder.strip())
    fields = [i.strip('"') for i in fields]
    return fields


def id_counter(item_counted):
    """
    Retrieves and increments a persistent ID counter for a given item type.

    Reads the current ID value from a text file specific to the item type, increments it, writes the updated value back to the file, and returns the original ID. If the file does not exist, a new one is created and the starting ID is set to 1.

    Args:
        item_counted (str): The name of the item type (e.g., "movie", "showtime") used to locate the counter file.

    Returns:
        int: The current ID number before incrementing.

    """
    filename = f'Cinema/Database/COUNTER_{item_counted}_id.txt'
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            id_no = int(content) if content else 1
    except FileNotFoundError:
        id_no = 1
    with open(filename, "w") as f:
        f.write(str(id_no + 1))
    return id_no


def view_movie_listing():
    """
    Displays all movie listings.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/movie_listings.txt")
    while True:
        done = input("Press ENTER to return to cinema manager menu...")
        if done == "":
            main_cinema_manager()
            break


def add_movie_listing():
    """
    Collects movie details from user input and adds a new movie listing entry.

    Returns:
        None
    """
    while True:
        movie_name = input("Enter movie name: ")
        if movie_name:
            break
        print(color_error_message("Invalid input: movie listing must have movie name."))

    release_date = validate_date("Enter release date (DD-MM-YYYY): ")

    while True:
        running_time = validate_int("Enter running time (total number of minutes): ")
        if 0 < running_time < 500:
            break
        print(color_error_message("Invalid input: running time should be greater than 0 and lesser than 500."))

    genre = [genre.strip().title() for genre in input("Enter genres (lists should be comma-separated): ").split(",")]

    for index, field in enumerate(CLASSIFICATION_OPTIONS, start=1):
        print(f'[{index}] {field}', end="   ")
    print()
    while True:
        classification_selection = validate_int("Select classification (enter number 1-7): ")
        if (1 <= classification_selection <= 7):
            classification = CLASSIFICATION_OPTIONS[classification_selection - 1]
            break
        print(color_error_message("Invalid option: please enter a number 1-7."))

    spoken_language = input("Enter spoken language (full form): ").title()

    subtitle_language = [language.strip().title() for language in input("Enter subtitle languages (full form, lists should be comma-separated): ").split(",")]

    directors = [director.strip().title() for director in input("Enter director names (lists should be comma-separated): ").split(",")]

    casts = [cast.strip().title() for cast in input("Enter cast names (lists should be comma-separated): ").split(",")]

    description = input("Enter movie description: ")

    eligibility_for_discount = validate_yes_no("Select eligibility for discount [Y/N]: ")

    movie_listing = [movie_name, release_date, running_time, genre, classification, spoken_language, subtitle_language, directors, casts, description, eligibility_for_discount]

    clear_terminal()
    for i in range(len(MOVIE_CONFIRMATION_KEYS)):
        print(f'{color_confirmation_message(MOVIE_CONFIRMATION_KEYS[i])}: {movie_listing[i] if not isinstance(movie_listing[i], list) else ", ".join(movie_listing[i])}')

    confirmed = validate_yes_no("Confirm and add movie listing? [Y/N]: ") == "Y"
    if confirmed:
        movie_id_no = id_counter("movie")
        movie_id = f'M{movie_id_no:03}'
        movie_listing.insert(0, movie_id)
        add_entry("Cinema/Database/movie_listings.txt", movie_listing)
        notification = f'SUCCESS: Movie listing {movie_id} for "{movie_name}" added.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Add another movie listing? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            add_movie_listing()
        else:
            main_cinema_manager()
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_movie_listing()
        else:
            main_cinema_manager()


def update_movie_listing():
    """
    Updates a specific field in an existing movie listing entry.

    Prompts the user for a movie ID, validates its existence, displays editable fields, and allows selection of one field to update.

    Returns:
        None
    """
    movie_id = input("Enter ID of movie to be edited: ").upper().strip()
    movie_listing = lookup_entry("Cinema/Database/movie_listings.txt", entry_id=movie_id)
    if not movie_listing:
        print(color_error_message("Invalid input: this movie ID does not exist."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_movie_listing()
        else:
            main_cinema_manager()

    details = lookup_entry("Cinema/Database/movie_listings.txt", header=1)
    for index, field in enumerate(details[1:], start=1):
        print(f'[{index}] {field}')

    detail_selection = validate_int("Select detail (enter number 1-11): ")

    match detail_selection:
        case 1:
            while True:
                update_details = input("Enter update movie name: ")
                if update_details:
                    break
                print(color_error_message("Invalid input: movie listing must have movie name."))
        case 2:
            update_details = validate_date("Enter updated release date (DD-MM-YYYY): ")
        case 3:
            while True:
                update_details = validate_int("Enter updated running time (total number of minutes): ")
                if 0 < update_details < 500:
                    break
                print(color_error_message("Invalid input: running time should be greater than 0 and lesser than 500."))
        case 4:
            update_details = [genre.strip().title() for genre in input("Enter updated genres (lists should be comma-separated): ").split(",")]
        case 5:
            for index, field in enumerate(CLASSIFICATION_OPTIONS, start=1):
                print(f'[{index}] {field}', end="   ")
            print()
            while True:
                classification_selection = validate_int("Select classification (enter number 1-7): ")
                if (1 <= classification_selection <= 7):
                    update_details = CLASSIFICATION_OPTIONS[classification_selection - 1]
                    break
                print(color_error_message("Invalid option: please enter a number 1-7."))
        case 6:
            update_details = input("Enter updated spoken language (full form): ").title()
        case 7:
            update_details = [language.strip().title() for language in input("Enter updated subtitle languages (full form, lists should be comma-separated): ").split(",")]
        case 8:
            update_details = [director.strip().title() for director in input("Enter updated director names (lists should be comma-separated): ").split(",")]
        case 9:
            update_details = [cast.strip().title() for cast in input("Enter updated cast names (lists should be comma-separated): ").split(",")]
        case 10:
            update_details = input("Enter updated description: ")
        case 11:
            update_details = validate_yes_no("Select updated eligibility for discount [Y/N]: ")
        case _:
            print(color_error_message("Invalid option."))
            detail_selection = validate_int("Select detail (enter number 1-11): ")
            
    clear_terminal()       
    print(f'{color_confirmation_message(MOVIE_CONFIRMATION_KEYS[detail_selection - 1])}: {update_details if not isinstance(update_details, list) else ", ".join(update_details)}')
    
    confirmed = validate_yes_no("Confirm and update movie listing? [Y/N]: ") == "Y"
    if confirmed:
        update_entry("Cinema/Database/movie_listings.txt", movie_id, detail_selection, update_details)
        notification = f'SUCCESS: Movie listing {movie_id} for "{lookup_entry("Cinema/Database/movie_listings.txt", entry_id=movie_id)[1]}" updated.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Update another movie listing? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            update_movie_listing()
        else:
            main_cinema_manager()
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_movie_listing()
        else:
            main_cinema_manager()
            

def remove_movie_listing():
    """
    Removes a specific movie listing entry.

    Prompts the user for a movie ID, validates its existence, then deletes corresponding movie listing.

    Returns:
        None
    """
    movie_id = input("Enter ID of movie to be removed: ").upper().strip()
    movie_listing = lookup_entry("Cinema/Database/movie_listings.txt", entry_id=movie_id)
    if not movie_listing:
        print(color_error_message("Invalid input: this movie ID does not exist."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            remove_movie_listing()
        else:
            main_cinema_manager()
    remove_entry("Cinema/Database/movie_listings.txt", movie_id)
    notification = f'SUCCESS: Movie listing {movie_id} for "{movie_listing[1]}" removed.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Remove another movie listing? [Y/N]: ") == "Y"
    if another:
        clear_terminal()
        remove_movie_listing()
    else:
        main_cinema_manager()


def view_showtime():
    """
    Displays all movie showtimes.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/movie_showtimes.txt")
    while True:
        done = input("Press ENTER to return to cinema manager menu...")
        if done == "":
            main_cinema_manager()
            break


def calculate_discount(discount_id, normal_price):
    """
    Calculates the discounted price based on a discount policy.

    Retrieves the discount policy using the given discount ID, then applies either a fixed amount or percentage-based discount to the normal price. Rounds the result to two decimal places.

    Args:
        discount_id (str): ID of the discount policy.
        normal_price (float): Original price before discount.

    Returns:
        float or None: The discounted price, or None if the policy is not found or invalid.
    """
    discounted_price = None
    entry = lookup_entry("Cinema/Database/discount_policies.txt", entry_id=discount_id)
    if entry[2] == "fixed":
        discounted_price = round((float(normal_price) - float(entry[3])), 2)
    elif entry[2] == "percentage":
        discounted_price = round((float(normal_price) * (1 - float(entry[4]))), 2)
    return f'{discounted_price:.2f}'


def round_time(end_time):
    """
    Rounds up a time to the nearest 5 minutes if needed.

    Args:
        end_time (datetime.datetime): The time to be rounded.

    Returns:
        datetime.datetime: The time rounded to the nearest 5 minutes.
    """
    end_time = end_time.replace(second=0, microsecond=0)
    minutes_to_add = (5 - end_time.minute % 5) % 5
    if minutes_to_add:
        end_time += timedelta(minutes=minutes_to_add)
    return end_time


def add_showtime():
    """
    Collects showtime details from user input and adds a new movie showtime entry.

    Returns:
        None
    """
    movie_id = input("Enter movie ID: ").upper().strip()
    movie_listing = lookup_entry("Cinema/Database/movie_listings.txt", entry_id=movie_id)
    if not movie_listing:
        print(color_error_message("Invalid input: this movie ID does not exist."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_showtime()
        else:
            main_cinema_manager()

    #CHECK DATE AND TIME FIRST SO CAN CHOOSE AUDI BASED ON AVAILABILITY
    date = validate_date("Enter date (DD-MM-YYYY): ")
    duration = timedelta(minutes=int(movie_listing[3]))
    start_time = validate_time("Enter start time (HHMM): ")
    parsed_start_time = datetime.strptime(start_time, "%H%M")
    parsed_end_time = round_time(parsed_start_time + duration)
    end_time = datetime.strftime(parsed_end_time, "%H%M")
    same_day_showtimes = []
    same_time_showtimes = []
    with open("Cinema/Database/movie_showtimes.txt", "r") as f:
        for line in f:
            entry = [i.strip() for i in line.split(",")]
            if entry[3] == date:
                same_day_showtimes.append(entry)
    for showtime in same_day_showtimes:
        existing_start_time = datetime.strptime(showtime[4], "%H%M")
        existing_end_time = datetime.strptime(showtime[5], "%H%M")
        if not (parsed_start_time > existing_end_time + BUFFER or parsed_end_time + BUFFER < existing_start_time):
            same_time_showtimes.append(showtime)
    available_auditoriums = AUDITORIUM_OPTIONS.copy()
    for showtime in same_time_showtimes:
        unavailable_auditorium_id = showtime[2]
        if unavailable_auditorium_id in available_auditoriums:
            available_auditoriums.remove(unavailable_auditorium_id)
    if not available_auditoriums:
        print(color_error_message("Unavailable time: no auditoriums are available for this time slot."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_showtime()
        else:
            main_cinema_manager()

    end_auditorium_number = len(available_auditoriums)
    for index, field in enumerate(available_auditoriums, start=1):
        print(f'[{index}] {field}', end="   ")
    print()
    while True:
        auditorium_selection = validate_int(f'Select auditorium (enter number 1-{end_auditorium_number}): ')
        if (1 <= auditorium_selection <= end_auditorium_number):
            auditorium_id = available_auditoriums[auditorium_selection - 1]
            break
        print(color_error_message(f'Invalid option: please enter a number 1-{end_auditorium_number}.'))
    auditorium_info = lookup_entry("Cinema/Database/auditorium_info.txt", entry_id=auditorium_id)
    normal_price = round(float(auditorium_info[5]), 2)
    discounted_price = None

    if movie_listing[11] == "Y":
        discount_id = input("Enter discount ID: ").upper().strip()
        discount_policy = lookup_entry("Cinema/Database/discount_policies.txt", entry_id=discount_id)
        if not discount_policy:
            print(color_error_message("Invalid input: this discount ID does not exist."))
            tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
            if tryagain:
                clear_terminal()
                add_showtime()
            else:
                main_cinema_manager()
        discounted_price = calculate_discount(discount_id, normal_price)
    else:
        discount_id = None

    showtime = [movie_id, auditorium_id, date, start_time, end_time, f'{normal_price:.2f}', discounted_price if discounted_price is not None else "", discount_id if discount_id is not None else ""]
    
    clear_terminal()
    for i in range(len(SHOWTIME_CONFIRMATION_KEYS)):
        print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[i])}: {showtime[i] if showtime[i] != "" else "N/A"}')
    
    confirmed = validate_yes_no("Confirm and add movie showtime? [Y/N]: ") == "Y"
    if confirmed:
        showtime_id_no = id_counter("showtime")
        showtime_id = f'ST{showtime_id_no:04}'
        showtime.insert(0, showtime_id)
        add_entry("Cinema/Database/movie_showtimes.txt", showtime)
        notification = f'SUCCESS: Showtime {showtime_id} for {movie_id} at {start_time}, {date} added.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Add another movie showtime? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            add_showtime()
        else:
            main_cinema_manager()
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_showtime()
        else:
            main_cinema_manager()


def update_showtime():
    """
    Updates a specific field in an existing movie showtime entry.

    Prompts the user for a showtime ID, validates its existence, displays editable fields, and allows selection of one field to update.

    Returns:
        None
    """

    def check_auditorium_availability(date, start_time, showtime_id):
        """
        Determines the available auditoriums for a certain date and timeframe.

        Args:
            date (str): The date of the showtime.
            start_time (str): The start time of the showtime.
            showtime_id (str): The ID of the showtime to be updated.

        Returns:
            update_details (list): A list containing the auditorium ID of the selected auditorium, the end time, the normal price based on the auditorium, and the discounted price based on the normal price and the existing discount ID if the movie is eligible for discount.
        """
        movie_showtime = lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
        movie_id = movie_showtime[1]
        movie_listing = lookup_entry("Cinema/Database/movie_listings.txt", entry_id=movie_id)
        duration = timedelta(minutes=int(movie_listing[3]))
        parsed_start_time = datetime.strptime(start_time, "%H%M")
        parsed_end_time = round_time(parsed_start_time + duration)
        end_time = datetime.strftime(parsed_end_time, "%H%M")
        same_day_showtimes = []
        same_time_showtimes = []
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for line in f:
                entry = [i.strip() for i in line.split(",")]
                if entry[3] == date:
                    same_day_showtimes.append(entry)
        for showtime in same_day_showtimes:
            existing_start_time = datetime.strptime(showtime[4], "%H%M")
            existing_end_time = datetime.strptime(showtime[5], "%H%M")
            if not (parsed_start_time > existing_end_time + BUFFER or parsed_end_time + BUFFER < existing_start_time):
                same_time_showtimes.append(showtime)
        available_auditoriums = AUDITORIUM_OPTIONS.copy()
        for showtime in same_time_showtimes:
            unavailable_auditorium_id = showtime[2]
            if unavailable_auditorium_id in available_auditoriums:
                available_auditoriums.remove(unavailable_auditorium_id)
        if not available_auditoriums:
            print(color_error_message("Unavailable time: no auditoriums are available for this time slot."))
            tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
            if tryagain:
                clear_terminal()
                update_showtime()
            else:
                main_cinema_manager()

        end_auditorium_number = len(available_auditoriums)
        for index, field in enumerate(available_auditoriums, start=1):
            print(f'[{index}] {field}', end="   ")
        print()
        while True:
            auditorium_selection = validate_int(f'Select auditorium (enter number 1-{end_auditorium_number}): ')
            if (1 <= auditorium_selection <= end_auditorium_number):
                auditorium_id = available_auditoriums[auditorium_selection - 1]
                break
            print(color_error_message(f'Invalid option: please enter a number 1-{end_auditorium_number}.'))
        auditorium_info = lookup_entry("Cinema/Database/auditorium_info.txt", entry_id=auditorium_id)
        normal_price = round(float(auditorium_info[5]), 2)
        discounted_price = None
        
        if movie_listing[11] == "Y":
            discount_id = movie_showtime[8]
            discounted_price = calculate_discount(discount_id, normal_price)
        else:
            discount_id = None
        
        update_details = [auditorium_id, end_time, f'{normal_price:.2f}', discounted_price if discounted_price is not None else ""]
        return update_details


    showtime_id = input("Enter ID of showtime to be edited: ").upper().strip()
    movie_showtime = lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
    if not movie_showtime:
        print(color_error_message("Invalid input: this showtime ID does not exist."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_showtime()
        else:
            main_cinema_manager()

    details = lookup_entry("Cinema/Database/movie_showtimes.txt", header=1)
    for index, field in enumerate(details[1:5] + [details[8]], start=1):
        print(f'[{index}] {field}')

    detail_selection = validate_int("Select detail (enter number 1-5): ")

    match detail_selection:
        case 1:
            update_details = input("Enter updated movie ID: ").upper().strip()
            movie_listing = lookup_entry("Cinema/Database/movie_listings.txt", entry_id=update_details)
            if not movie_listing:
                print(color_error_message(
                    "Invalid input: this movie ID does not exist."))
                tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_showtime()
                else:
                    main_cinema_manager()
        case 2:
            date = movie_showtime[3]
            start_time = movie_showtime[4]
            update_details = check_auditorium_availability(date, start_time, showtime_id)
        case 3:
            date = validate_date("Enter updated date (DD-MM-YYYY): ")
            start_time = movie_showtime[4]
            update_details = check_auditorium_availability(date, start_time, showtime_id)
        case 4:
            date = movie_showtime[3]
            start_time = validate_time("Enter updated start time (HHMM): ")
            update_details = check_auditorium_availability(date, start_time, showtime_id)
        case 5:
            movie_showtime = lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
            movie_id = movie_showtime[1]
            movie_listing = lookup_entry("Cinema/Database/movie_listings.txt", entry_id=movie_id)
            if movie_listing[11] == "Y":
                discount_id = input("Enter updated discount ID: ").upper().strip()
                discount_policy = lookup_entry("Cinema/Database/discount_policies.txt", entry_id=discount_id)
                if not discount_policy:
                    print(color_error_message("Invalid input: this discount ID does not exist."))
                    tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
                    if tryagain:
                        clear_terminal()
                        update_showtime()
                    else:
                        main_cinema_manager()
                normal_price = movie_showtime[6]
                discounted_price = calculate_discount(discount_id, normal_price)
                update_details = [discounted_price, discount_id]
            else:
                print(color_error_message("Invalid option: this movie is not eligible for discounts."))
                tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_showtime()
                else:
                    main_cinema_manager()
        case _:
            print(color_error_message("Invalid option."))
            detail_selection = validate_int("Select detail (enter number 1-5): ")


    clear_terminal()
    match detail_selection:
        case 1:
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[0])}: {update_details}')
        case 2 | 3 | 4:
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[1])}: {update_details[0]}')
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[2])}: {date}')
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[3])}: {start_time}')
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[4])}: {update_details[1]}')
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[5])}: {update_details[2]}')
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[6])}: {update_details[3] if update_details[3] != "" else "N/A"}')
        case 5:
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[7])}: {update_details[1]}')
            print(f'{color_confirmation_message(SHOWTIME_CONFIRMATION_KEYS[6])}: {update_details[0]}')
        
    confirmed = validate_yes_no("Confirm and update movie showtime? [Y/N]: ") == "Y"
    if confirmed:
        match detail_selection:
            case 1:
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, detail_selection, update_details)
            case 2 | 3 | 4:
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 2, update_details[0])
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 5, update_details[1])
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 6, update_details[2])
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 7, update_details[3])
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 3, date)
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 4, start_time)
            case 5:
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 7, update_details[0])
                update_entry("Cinema/Database/movie_showtimes.txt", showtime_id, 8, update_details[1])

        notification = f'SUCCESS: Showtime {showtime_id} for {lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)[1]} at {lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)[3]}, {lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)[4]} updated.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Update another movie showtime? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            update_showtime()
        else:
            main_cinema_manager()
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_showtime()
        else:
            main_cinema_manager()


def remove_showtime():
    """
    Removes a specific movie showtime entry.

    Prompts the user for a showtime ID, validates its existence, then deletes corresponding movie listing.

    Returns:
        None
    """
    showtime_id = input("Enter ID of showtime to be removed: ").upper().strip()
    movie_showtime = lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
    if not movie_showtime:
        print(color_error_message("Invalid input: this showtime ID does not exist."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            remove_showtime()
        else:
            main_cinema_manager()
    remove_entry("Cinema/Database/movie_showtimes.txt", showtime_id)
    notification = f'SUCCESS: Showtime {showtime_id} for {movie_showtime[1]} at {movie_showtime[3]}, {movie_showtime[4]} removed.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Remove another movie showtime? [Y/N]: ") == "Y"
    if another:
        clear_terminal()
        remove_showtime()
    else:
        main_cinema_manager()


def view_discount():
    """
    Displays all discount policies.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/discount_policies.txt")
    while True:
        done = input("Press ENTER to return to cinema manager menu...")
        if done == "":
            main_cinema_manager()
            break


def add_discount():
    """
    Collects discount details from user input and adds a new duscount policy entry.

    Returns:
        None
    """
    while True:
        discount_name = input("Enter discount name: ")
        if discount_name:
            break
        print(color_error_message("Invalid input: discount policy must have discount name."))

    discount_type_options = ["fixed", "percentage"]
    for index, field in enumerate(discount_type_options[0: 2], start=1):
        print(f'[{index}] {field}', end="   ")
    print()
    discount_type_selection = validate_int("Select discount type (enter number 1-2): ")
    match discount_type_selection:
        case 1:
            discount_type = discount_type_options[0]
            discount_amount = validate_float("Enter discount amount (2 decimal float): ")
            discount_rate = None
        case 2:
            discount_type = discount_type_options[1]
            discount_amount = None
            discount_rate = validate_float(
                "Enter discount rate (2 decimal float): ")
        case _:
            print(color_error_message("Invalid option."))
            discount_type_selection = validate_int("Select discount type (enter number 1-2): ")
    discount_policies = input("Enter discount policies: ")

    discount_policy = [discount_name, discount_type, f'{discount_amount:.2f}' if discount_amount is not None else "", f'{discount_rate:.2f}' if discount_rate is not None else "", discount_policies]
    
    
    clear_terminal()
    for i in range(len(DISCOUNT_CONFIRMATION_KEYS)):
        print(f'{color_confirmation_message(DISCOUNT_CONFIRMATION_KEYS[i])}: {discount_policy[i] if discount_policy[i] != "" else "N/A"}')
    
    confirmed = validate_yes_no("Confirm and add discount policy? [Y/N]: ") == "Y"
    if confirmed:
        discount_id_no = id_counter("discount")
        discount_id = f'D{discount_id_no:02}'
        discount_policy.insert(0, discount_id)
        add_entry("Cinema/Database/discount_policies.txt", discount_policy)
        notification = f'SUCCESS: Discount {discount_id} for {discount_name} added.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Add another discount policy? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            add_discount()
        else:
            main_cinema_manager()
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_discount()
        else:
            main_cinema_manager()


def update_discount():
    """
    Updates a specific field in an existing discount policy entry.

    Prompts the user for a discount ID, validates its existence, displays editable fields, and allows selection of one field to update.

    Returns:
        None
    """
    discount_id = input("Enter ID of discount to be edited: ").upper().strip()
    discount_policy = lookup_entry(
        "Cinema/Database/discount_policies.txt", entry_id=discount_id)
    if not discount_policy:
        print(color_error_message("Invalid input: this discount ID does not exist."))
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_discount()
        else:
            main_cinema_manager()

    details = lookup_entry(
        "Cinema/Database/discount_policies.txt", header=1)
    for index, field in enumerate(details[1:], start=1):
        print(f'[{index}] {field}')

    detail_selection = validate_int("Select detail (enter number 1-5): ")

    match detail_selection:
        case 1:
            while True:
                update_details = input("Enter discount name: ")
                if update_details:
                    break
                print(color_error_message(
                    "Invalid input: discount policy must have discount name."))
        case 2:
            if discount_policy[2] == "fixed":
                discount_type = "percentage"
                discount_amount = None
                discount_rate = validate_float("Enter updated discount rate (2 decimal float): ")
            elif discount_policy[2] == "percentage":
                discount_type = "fixed"
                discount_amount = validate_float("Enter updated discount amount (2 decimal float): ")
                discount_rate = None
            update_details = [discount_type, f'{discount_amount:.2f}' if discount_amount is not None else "", f'{discount_rate:.2f}' if discount_rate is not None else ""]
        case 3:
            if discount_policy[2] != "fixed":
                print(color_error_message("Invalid selection: discount amount cannot be edited for percentage discounts."))
                tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_discount()
                else:
                    main_cinema_manager()
            else:
                update_details = validate_float("Enter updated discount amount (2 decimal float): ")
                update_details = f'{update_details:.2f}'
        case 4:
            if discount_policy[2] != "percentage":
                print(color_error_message("Invalid selection: discount rate cannot be edited for fixed discounts."))
                tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_discount()
                else:
                    main_cinema_manager()
            else:
                update_details = validate_float("Enter updated discount rate (2 decimal float): ")
                update_details = f'{update_details:.2f}'
        case 5:
            update_details = input("Enter updated discount policies: ")
        case _:
            print(color_error_message("Invalid option."))
            detail_selection = validate_int("Select detail (enter number 1-5): ")
      
    clear_terminal()      
    match detail_selection:
        case 2:
            print(f'{color_confirmation_message(DISCOUNT_CONFIRMATION_KEYS[1])}: {update_details[0]}')
            print(f'{color_confirmation_message(DISCOUNT_CONFIRMATION_KEYS[2])}: {update_details[1] if update_details[1] != "" else "N/A"}')
            print(f'{color_confirmation_message(DISCOUNT_CONFIRMATION_KEYS[3])}: {update_details[2] if update_details[2] != "" else "N/A"}')
        case _:
            print(f'{color_confirmation_message(DISCOUNT_CONFIRMATION_KEYS[detail_selection - 1])}: {update_details}')

    confirmed = validate_yes_no("Confirm and update discount policy? [Y/N]: ") == "Y"
    if confirmed:
        match detail_selection:
            case 2:
                update_entry("Cinema/Database/discount_policies.txt",
                            discount_id, 2, update_details[0])
                update_entry("Cinema/Database/discount_policies.txt",
                            discount_id, 3, update_details[1])
                update_entry("Cinema/Database/discount_policies.txt",
                            discount_id, 4, update_details[2])
            case _:
                update_entry("Cinema/Database/discount_policies.txt",
                        discount_id, detail_selection, update_details)
            
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for line in f:
                showtime = [i.strip() for i in line.split(",")]
                if len(showtime) == 9:
                    if showtime[8] == discount_id:
                        normal_price = showtime[6]
                        discounted_price = calculate_discount(discount_id, normal_price)
                        update_entry("Cinema/Database/movie_showtimes.txt", showtime[0], 7, discounted_price)
        
        notification = f'SUCCESS: Discount {discount_id} for {lookup_entry("Cinema/Database/discount_policies.txt", entry_id=discount_id)[1]} updated.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Update another discount policy? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            update_discount()
        else:
            main_cinema_manager()   
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_discount()
        else:
            main_cinema_manager() 


def remove_discount():
    """
    Removes a specific discount policy entry.

    Prompts the user for a discount ID, validates its existence, then deletes corresponding movie listing.

    Returns:
        None
    """
    discount_id = input("Enter ID of discount to be removed: ").upper().strip()
    discount_policy = lookup_entry("Cinema/Database/discount_policies.txt", entry_id=discount_id)
    if not discount_policy:
        print(color_error_message("Invalid input: this discount ID does not exist."))
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            remove_discount()
        else:
            main_cinema_manager()
    remove_entry("Cinema/Database/discount_policies.txt", discount_id)
    notification = f'SUCCESS: Discount {discount_id} for {discount_policy[1]} removed.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Remove another discount policy? [Y/N]: ") == "Y"
    if another:
        clear_terminal()
        remove_discount()
    else:
        main_cinema_manager()


def view_auditorium():
    """
    Displays all auditoriums.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/auditorium_info.txt")
    while True:
        done = input("Press ENTER to return to cinema manager menu...")
        if done == "":
            main_cinema_manager()
            break


def update_price():
    """
    Updates the default normal price field in an existing auditorium info entry.

    Prompts the user for an auditorium ID, validates its existence, and updates price field.

    Returns:
        None
    """
    for index, field in enumerate(AUDITORIUM_OPTIONS, start=1):
        print(f'[{index}] {field}', end="   ")
    print()
    while True:
        auditorium_selection = validate_int("Select auditorium (enter number 1-8): ")
        if (1 <= auditorium_selection <= 8):
            auditorium_id = AUDITORIUM_OPTIONS[auditorium_selection - 1]
            break
        print(color_error_message("Invalid option: please enter a number 1-8."))
    print("\n")
    update_details = validate_float("Enter updated price (2 decimal float): ")
    
    clear_terminal()
    print(f'{color_confirmation_message("Auditorium ID")}: {auditorium_id}')
    print(f'{color_confirmation_message("Updated Price")}: {update_details:.2f}')
    
    confirmed = validate_yes_no("Confirm and update price? [Y/N]: ") == "Y"
    if confirmed:
        update_entry("Cinema/Database/auditorium_info.txt", auditorium_id, 5, f'{update_details:.2f}')
        notification = f'SUCCESS: Price for auditorium {auditorium_id} updated.'
        print("-" * len(notification))
        print(color_completion_message(notification))
        print("\n")
        another = validate_yes_no("Update another price? [Y/N]: ") == "Y"
        if another:
            clear_terminal()
            update_price()
        else:
            main_cinema_manager()
    else:
        tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_price()
        else:
            main_cinema_manager()



def view_booking_reports():
    """
    Displays booking entries, optionally filtered by movie ID.

    Returns:
        None
    """
    specific_movie = validate_yes_no("View the report for a specific movie? [Y/N] ") == "Y"
    clear_terminal()
    entries = []
    with open("Cinema/Database/movie_bookings.txt", "r") as f:
        header = f.readline().upper()
    header = [i.strip() for i in header.split(",")]
    header.insert(1, "MOVIE_NAME")
    header.insert(2, "DATE")
    header.insert(3, "START TIME")
    header = ", ".join(header)

    if specific_movie:
        movie_id = input("Enter movie ID: ").upper().strip()
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for showtime_line in f:
                showtime_entry = [i.strip() for i in showtime_line.split(",")]
                if showtime_entry[1] == movie_id:
                    with open("Cinema/Database/movie_bookings.txt", "r") as g:
                        for booking_line in g:
                            entry = [i.strip() for i in booking_line.split(",")]
                            if entry[1] == showtime_entry[0]:
                                entries.append(", ".join(entry) + "\n")

    else:
        with open("Cinema/Database/movie_bookings.txt", "r") as f:
            next(f)
            entries = f.readlines()
            
    booking_info = []
    
    for booking in entries:
        booking = [i.strip() for i in booking.split(",")]
        showtime_id = booking[1]
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for showtime_line in f:
                showtime_entry = [i.strip() for i in showtime_line.split(",")]
                if showtime_entry[0] == showtime_id:
                    movie_id = showtime_entry[1]
                    with open("Cinema/Database/movie_listings.txt", "r") as g:
                        for movie_line in g:
                            movie_entry = [i.strip() for i in movie_line.split(",")] 
                            if movie_entry[0] == movie_id:
                                movie_name = movie_entry[1]
                                booking.insert(1, movie_name)
                    date = showtime_entry[3]
                    start_time = showtime_entry[4]
                    booking.insert(2, date)
                    booking.insert(3, start_time)
                    booking_info.append(booking)
                    
    booking_info = [", ".join(item) for item in booking_info]
    print(header)
    print("-" * len(header))
    if not booking_info:
        print("No entries found.")
    else:
        for line in booking_info:
            print(line)
        print("\n")

    while True:
        done = input("Press ENTER to return to cinema manager menu...")
        if done == "":
            main_cinema_manager()
            break


def view_revenue_summary():
    """
    Calculates and displays total revenue from movie bookings.

    Returns:
        None
    """
    normal_total_revenue = 0
    discounted_total_revenue = 0
    with open("Cinema/Database/movie_bookings.txt", "r") as f:
        next(f)
        for line in f:
            booking = [i.strip() for i in line.split(",")]
            tickets = [int(i.strip()) for i in booking[4].split("|")]
            showtime_id = booking[1]
            movie_showtime = lookup_entry("Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
            if not movie_showtime:
                normal_price = 0
                discounted_price = 0
            else:
                normal_price = float(movie_showtime[6])
                discounted_price = float(movie_showtime[7]) if movie_showtime[7] else 0.00
            normal_total_revenue += round((tickets[0] * normal_price), 2)
            discounted_total_revenue += round((tickets[1] * discounted_price), 2)

    total_revenue = normal_total_revenue + discounted_total_revenue
    print(f'REVENUE FROM NORMAL TICKETS: {normal_total_revenue:.2f}')
    print(f'REVENUE FROM DISCOUNTED TICKETS: {discounted_total_revenue:.2f}')
    print(max(len(f'REVENUE FROM NORMAL TICKETS: {normal_total_revenue:.2f}'), len(f'REVENUE FROM DISCOUNTED TICKETS: {discounted_total_revenue:.2f}')) * "-")
    print(f'TOTAL REVENUE: {total_revenue}')
    print()
    while True:
        done = input("Press ENTER to return to cinema manager menu...")
        if done == "":
            main_cinema_manager()
            break


def main_cinema_manager():
    """
    Displays the cinema manager menu and executes selected actions.

    Prompts the user to select an action, confirms intent, and executes the corresponding function. 

    Returns:
        None
    """
    clear_terminal()
    print("==== CINEMA MANAGER MENU ====\n\nAvailable actions:\n-----------------------------")
    actions = ["View movie listings", "Add movie listing", "Update movie listing", "Remove movie listing", "View showtimes", "Add showtime", "Update showtime", "Remove showtime", "View discounts",
               "Add discount", "Update discount", "Remove discount", "View auditoriums", "Update normal price", "View booking report", "View revenue summary", "Exit cinema manager role"]

    for index, action in enumerate(actions, start=1):
        print(f'[{index}] {action}')
    print("-----------------------------")

    action_functions = {
        1: view_movie_listing,
        2: add_movie_listing,
        3: update_movie_listing,
        4: remove_movie_listing,
        5: view_showtime,
        6: add_showtime,
        7: update_showtime,
        8: remove_showtime,
        9: view_discount,
        10: add_discount,
        11: update_discount,
        12: remove_discount,
        13: view_auditorium,
        14: update_price,
        15: view_booking_reports,
        16: view_revenue_summary,
        17: main
    }

    while True:
        action_choice = validate_int("Select action (enter number 1-17): ")
        if action_choice in action_functions:
            break
        print(color_error_message("Invalid input: please enter a number 1-17."))
    confirmed = validate_yes_no(
        f'Confirm action: {actions[action_choice - 1].lower()}? [Y/N]: ') == "Y"
    if confirmed:
        clear_terminal()
        action_functions[action_choice]()
    else:
        clear_terminal()
        main_cinema_manager()

    while True:
        action_choice = validate_int("Select action (enter number 1-17): ")
        if action_choice in action_functions:
            break
        print("Invalid input: please enter a number 1-17.")
    confirmed = validate_yes_no(
        f'Confirm action: {actions[action_choice - 1].lower()}? [Y/N]: ') == "Y"
    if confirmed:
        clear_terminal()
        action_functions[action_choice]()
    else:
        clear_terminal()
        main_cinema_manager()





def load_movie(filename=r"Cinema/Database/movie_listings.txt"):
    movies = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if not line.strip():
                    continue
                movie = {
                    "movie_data": line  # keep raw text
                }
                movies.append(movie)
    except FileNotFoundError:
        print("⚠️ movie_listing.txt not found! Please put it in Cinema\\Database\\movie_listing.txt or adjust the path.")
    return movies


def display_movies(movies):
    if not movies:
        print("⚠️ No movies available.")
        return

    print("\n🎬==============================================🎬")
    print("                 MOVIE  LISTINGS")
    print("==============================================")

    for i, m in enumerate(movies, start=1):
        print(f"\n🎞️  Movie #{i}")
        print("--------------------------------------------------")

        # Replace commas with newlines for easy reading
        formatted = m["movie_data"].replace(",", "\n")

        # Add simple labels for clarity
        print(f"""
Movie ID      : {formatted.splitlines()[0]}
Movie Name    : {formatted.splitlines()[1]}
Release Date  : {formatted.splitlines()[2]}
Running Time  : {formatted.splitlines()[3]} minutes
Genre         : {formatted.splitlines()[4]}
Classification: {formatted.splitlines()[5]}
Language      : {formatted.splitlines()[6]}
Subtitles     : {formatted.splitlines()[7]}
Director      : {formatted.splitlines()[8]}
Casts         : {formatted.splitlines()[9]}
Description   : {formatted.splitlines()[10]}
""")

        print("--------------------------------------------------")

    print("\n✅ End of Movie List")
    print("🎬==============================================🎬")

# ================== ISSUES (robust, deduped) ==================
ISSUES_FILE = "issues.txt"
AUDITORIUMS = [f"Auditorium {i}" for i in range(1, 9)]
EQUIPMENT_LIST = ["Projector", "Sound", "Air Conditioner"]


def load_issues(filename=ISSUES_FILE):
    """
    Load issues.txt into a dict keyed by (auditorium, equipment) -> status.
    Last occurrence in file wins (but usually file will be written by save_issues,
    so each pair appears once).
    """
    issues = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # split by '|' into at most 3 parts
                parts = [p.strip() for p in line.split("|", 2)]
                if len(parts) < 3:
                    continue
                aud, equip, status = parts[0], parts[1], parts[2]
                issues[(aud, equip)] = status
    except FileNotFoundError:
        # no file yet -> return empty dict
        pass
    return issues


def save_issues(issues, filename=ISSUES_FILE):
    """
    Save the issues dict to file (one canonical line per pair).
    """
    with open(filename, "w", encoding="utf-8") as f:
        # sort for stable ordering (optional)
        for (aud, equip), status in sorted(issues.items()):
            f.write(f"{aud} | {equip} | {status}\n")


# ----- action: report new issue (set Under Maintenance) -----
def report_issue():
    # Auditorium selection
    print("\nSelect Auditorium:")
    for i, a in enumerate(AUDITORIUMS, 1):
        print(f"{i}. {a}")
    choice = input("Enter choice (1-8): ")
    try:
        auditorium = AUDITORIUMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    # Equipment selection
    print("\nSelect Equipment:")
    for i, e in enumerate(EQUIPMENT_LIST, 1):
        print(f"{i}. {e}")
    choice = input("Enter choice (1-3): ")
    try:
        equipment = EQUIPMENT_LIST[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    # Load, update, save (this prevents duplicate lines)
    issues = load_issues()
    issues[(auditorium, equipment)] = "Under Maintenance"
    save_issues(issues)
    print(
        f"✅ Issue reported successfully: {auditorium} - {equipment} (Under Maintenance)")


# ----- view-only: show current equipment status for a chosen auditorium -----
def confirm_readiness():
    # (kept the old function name since it's option 3 in your menu)
    print("\nSelect Auditorium to view status:")
    for i, a in enumerate(AUDITORIUMS, 1):
        print(f"{i}. {a}")
    choice = input("Enter choice (1-8): ")
    try:
        auditorium = AUDITORIUMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    issues = load_issues()  # dict
    print(f"\n📋 Current equipment status for {auditorium}:")
    found_any = False
    # show all equipment types with status (default "No record")
    for equip in EQUIPMENT_LIST:
        status = issues.get((auditorium, equip), None)
        if status is None:
            print(f"   {equip}: READY ")
        else:
            print(f"   {equip}: {status}")
            found_any = True

    if not found_any:
        print("   (No recorded statuses yet for this auditorium.)")


# ----- resolve: set a specific equipment to Resolved -----
def mark_resolved():
    print("\nSelect Auditorium:")
    for i, a in enumerate(AUDITORIUMS, 1):
        print(f"{i}. {a}")
    choice = input("Enter choice (1-8): ")
    try:
        auditorium = AUDITORIUMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    print("\nSelect Equipment:")
    for i, e in enumerate(EQUIPMENT_LIST, 1):
        print(f"{i}. {e}")
    choice = input("Enter choice (1-3): ")
    try:
        equipment = EQUIPMENT_LIST[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    issues = load_issues()
    key = (auditorium, equipment)
    if key in issues:
        if issues[key] == "Under Maintenance":
            issues[key] = "Resolved"
            save_issues(issues)
            print(f"✅ Issue resolved: {auditorium} - {equipment}")
        elif issues[key] == "Resolved":
            print(
                f"ℹ️ Equipment already marked Resolved: {auditorium} - {equipment}")
        else:
            # if it was "OK" or other status, still update if you want:
            issues[key] = "Resolved"
            save_issues(issues)
            print(
                f"✅ Status updated to Resolved for {auditorium} - {equipment}")
    else:
        print("⚠️ No record found for that auditorium/equipment. Nothing to resolve.")

def reset_all_equipment():
    # Auditorium and equipment setup
    auditoriums = [f"Auditorium {i}" for i in range(1, 9)]
    equipment_list = ["Projector", "Sound", "Air Conditioner"]

    with open("issues.txt", "w", encoding="utf-8") as f:
        for auditorium in auditoriums:
            for equipment in equipment_list:
                f.write(f"{auditorium} | {equipment} | READY\n")

    print("🔄 All equipment has been reset to READY.")

# ================== MAIN MENU ==================
def main_technician():
    while True:
        print("\n===== 🎥 Cinema Technician System =====")
        print("1. View movie listings")
        print("2. Report technical issue")
        print("3. View equipment status for an auditorium")
        print("4. Mark equipment issue as resolved")
        print("5. Reset All Equipment to Ready ")
        print("6. Exit")

        choice = input("Enter choice (1-6): ")
        if choice == "1":
            movies = load_movie()
            display_movies(movies)
        elif choice == "2":
            report_issue()
        elif choice == "3":
            confirm_readiness()   # view-only now
        elif choice == "4":
            mark_resolved()
        elif choice == "5":
            reset_all_equipment()
        elif choice == "6":
            print("👋 Goodbye!")
            main()
        else:
            print("!! Invalid Choice, Please Use 1 2 3 ... Format !!")





# FILE PATHS (plain strings)
BASE =  r"Cinema/Database"
MOVIE_FILE    = BASE + r"/movie_listings.txt"      # where movie rows are stored
SHOW_FILE     = BASE + r"/movie_showtimes.txt"     # where showtime rows are stored
CUSTOMER_FILE = BASE + r"/customer.txt"      # where customer rows are stored
BOOKING_FILE  = BASE + r"/movie_bookings.txt"      # where booking rows are stored

# BASIC INPUT / STRING HELPERS
def safe_input(msg):                        # define a function that shows a message and reads user typing
    text = input(msg)                       # show the prompt and get the typed text
    return text.strip()                     # remove spaces/newlines at both ends then return it

def read_int(msg):                          # define a function that keeps asking until user types digits only
    while True:                             # infinite loop; we leave only when we "return"
        t = safe_input(msg)                 # ask the question and trim spaces
        if t.isdigit():                     # check the text is all digits (like "0", "12")
            return int(t)                   # convert to an integer and return it
        print("Please enter digits only.")  # if not digits, show error and loop again

def split_csv_line(line):                   # turn one CSV-ish line into a list of fields
    parts = line.split(",")                 # split by comma into pieces
    out = []                                # we'll build a cleaned list here
    for p in parts:                         # go through each piece
        out.append(p.strip().strip('"'))    # remove spaces and surrounding double quotes, then keep it
    return out                              # return the cleaned list

def join_csv(items):                        # turn a list like ["A","B","C"] into "A, B, C"
    texts = []                              # we'll store string versions here
    for it in items:                        # go through each item
        texts.append(str(it))               # make sure it's a string and keep it
    return ", ".join(texts)                 # join with comma+space and return

#  SIMPLE FILE HELPERS 
def read_all_lines(filename):                                           # read all lines from a file
    f = open(filename, "r", encoding="utf-8")                           # open the file for Reading text
                                                                         # encoding="utf-8" tells Python how to convert
                                                                         # bytes in the file into characters correctly.
    raw = f.readlines()                                                  # read all lines (each ends with "\n")
    f.close()                                                            # close the file (good habit)
    out = []                                                             # we'll store cleaned lines here
    for ln in raw:                                                       # go through each raw line
        out.append(ln.rstrip("\n"))                                      # remove the trailing newline only
    return out                                                           # return the cleaned list

def append_line(filename, one_line):                                     # add exactly one line at the end of a file
    f = open(filename, "a", encoding="utf-8")                            # open for Appending text (creates if missing,
                                                                         # but we assume files already exist to keep it simple)
    f.write(one_line + "\n")                                             # write the text and add a newline at the end
    f.close()                                                            # close the file

def write_all_lines(filename, lines):                                    # replace the whole file with our lines
    f = open(filename, "w", encoding="utf-8")                            # open for Writing text (this clears the file)
    for ln in lines:                                                     # go through each line we want to save
        f.write(ln + "\n")                                               # write it and add a newline
    f.close()                                                            # close the file

# SMALL ID HELPERS 
def pad4(n):                                                             # make numbers 1,2,3 look like "0001","0002","0003"
    s = str(n)                                                           # convert number to string
    while len(s) < 4:                                                    # while it's shorter than 4 characters
        s = "0" + s                                                      # add a "0" to the front
    return s                                                             # return the padded string

def next_id_by_count(filename, prefix):                                  # build id as prefix + (number of data rows + 1)
    lines = read_all_lines(filename)                                     # read all lines from the file
    if len(lines) == 0:                                                  # if file is empty (shouldn't be in this simple version)
        count = 0                                                        # then we say there are 0 data rows
    else:
        count = len(lines) - 1                                           # data rows = total lines - header
    next_number = count + 1                                              # the next new row number
    return prefix + pad4(next_number)                                    # example: "C0001" or "B0001"

# LOADERS (read files into lists of simple dicts)
def load_movies():                                                       # read movies we care about (id + name)
    movies = []                                                          # start with an empty list
    f = open(MOVIE_FILE, "r", encoding="utf-8")                          # open movies file for reading
    first = True                                                         # a flag to skip the header line
    for line in f:                                                       # read one line at a time
        if first:                                                        # if this is the first line (header)
            first = False                                                # mark header as consumed
            continue                                                     # and skip it
        parts = split_csv_line(line)                                     # split row into fields
        if len(parts) >= 2:                                              # we need at least movie_id and movie_name
            movie = {"movie_id": parts[0], "movie_name": parts[1]}       # build a small dictionary
            movies.append(movie)                                         # add it to our list
    f.close()                                                            # close the file
    return movies                                                        # return the list (maybe empty)

def load_showtimes():                                                    # read showtimes we care about
    shows = []                                                           # start with an empty list
    f = open(SHOW_FILE, "r", encoding="utf-8")                           # open showtimes file for reading
    first = True                                                         # skip-header flag
    for line in f:                                                       # read line by line
        if first:                                                        # first line is header
            first = False                                                # mark consumed
            continue                                                     # skip it
        parts = split_csv_line(line)                                     # split row into fields
        if len(parts) >= 6:                                              # we need at least 6 fields we use below
            show = {                                                     # make a dictionary with just the fields we print
                "showtime_id": parts[0],                                 # e.g., ST0001
                "movie_id":    parts[1],                                 # which movie this showtime belongs to
                "auditorium":  parts[2],                                 # e.g., AUD01
                "date":        parts[3],                                 # "YYYY-MM-DD"
                "start_time":  parts[4],                                 # start time like "18:00"
                "end_time":    parts[5]                                  # end time like "20:45"
            }
            shows.append(show)                                           # store it in the list
    f.close()                                                            # close the file
    return shows                                                         # return list (maybe empty)

# LOOKUPS 
def find_row_by_id(filename, id_index, target_id):                       # find a row where a specific column equals target_id
    lines = read_all_lines(filename)                                     # read all lines
    for i in range(1, len(lines)):                                       # loop from 1 to skip header at index 0
        parts = split_csv_line(lines[i])                                 # split the row into fields
        if len(parts) > id_index and parts[id_index] == target_id:       # check we have that column and it matches
            return parts                                                 # return the fields list for that row
    return None                                                          # if not found, return None

# VALIDATED PROMPTS (keep asking until correct) 
def ask_existing_customer_login():                                          # ask user for a real customer id
    while True:                                                          # keep asking until we can return
        cid = safe_input("Enter your customer ID (e.g. C0001): ")        # ask for id
        if find_row_by_id(CUSTOMER_FILE, 0, cid):                        # check column 0 in customers file
            return cid                                                   # valid -> return it
        print("Customer ID not found. Try again.")                       # otherwise tell and loop

def ask_existing_movie_id():                                             # ask user for a real movie id
    movies = load_movies()                                               # read movies for display
    if len(movies) == 0:                                                 # if there are no data rows
        print("No movies found in", MOVIE_FILE)                          # tell the user to put some data
    else:
        print("=== Movies ===")                                          # heading
        for m in movies:                                                 # show "M0001 - Title"
            print(m["movie_id"] + " - " + m["movie_name"])
    while True:                                                          # keep asking until valid
        mid = safe_input("Enter Movie ID (e.g. M0001): ")                # ask for a movie id
        if find_row_by_id(MOVIE_FILE, 0, mid):                           # check column 0 in movies file
            return mid                                                   # valid -> return it
        print("Invalid Movie ID. Try again.")                            # otherwise loop

def ask_existing_showtime_id_for_movie(movie_id):                        # ask for a showtime that belongs to that movie
    shows = load_showtimes()                                             # read all showtimes
    any_printed = False                                                  # track if we printed at least one

    # We’ll print the header once, with an empty line before/after for clarity
    for s in shows:                                                      # look through showtimes
        if s["movie_id"] == movie_id:                                    # filter for this movie
            if not any_printed:                                          # print heading only once
                print("\n=== Showtimes for", movie_id, "===\n")          # ← NEW: blank line before + after the header
            any_printed = True
            # print one showtime per line, with a blank line after each for readability
            print(" " + s["showtime_id"], "|", s["date"],                # ← NEW: leading space for a small indent
                  s["start_time"] + "-" + s["end_time"], "| Aud:", s["auditorium"])
            print()                                                      # ← NEW: blank line after each showtime

    if not any_printed:                                                  # if none found
        print("No showtimes for that movie.")                            # tell the user
        print()                                                          # ← NEW: blank line after the message

    while True:                                                          # keep asking until valid
        sid = safe_input("Enter Showtime ID (e.g. ST0001): ")            # ask for a showtime id
        row = find_row_by_id(SHOW_FILE, 0, sid)                          # see if that id exists
        if row is not None and len(row) > 1 and row[1] == movie_id:      # also check it belongs to the same movie
            print()                                                      # ← NEW: blank line after a valid selection
            return sid                                                   # valid -> return it
        print("Invalid showtime for that movie. Try again.\n")           # ← NEW: error + trailing blank line

def ask_existing_customer_login():
    # Ask for ID + password and verify against customers.txt
    while True:
        cid = safe_input("Customer ID (e.g. C0001): ")
        pwd = safe_input("Password: ")
        lines = read_all_lines(CUSTOMER_FILE)          # read all customer rows
        for i in range(1, len(lines)):                 # skip header
            parts = split_csv_line(lines[i])           # split into fields
            # expected order: [id, name, phone, email, password]
            if len(parts) >= 5 and parts[0] == cid and parts[4] == pwd:
                return cid                             # success
        print("ID or password is incorrect. Try again.")


# Register + Update personal details 
def register_customer():                                                 # add a new row to customers.txt
    lines = read_all_lines(CUSTOMER_FILE)                                # read all current lines
    cust_id = next_id_by_count(CUSTOMER_FILE, "C")                       # build next id like "C0001"
    name  = safe_input("Name: ")                                         # ask for name (any text)
    phone = safe_input("Phone (digits only, include 60): ")                          # ask for phone
    while not phone.isdigit():                                           # check phone is digits only
        print("Phone must be digits only.")
        phone = safe_input("Phone (digits only): ")
    email = safe_input("Email: ")                                        # ask for email
    while "@" not in email:                                              # very simple email check
        print("Email must contain '@'.")
        email = safe_input("Email: ")
    while True:
        pwd1 = safe_input("Create password: ")
        pwd2 = safe_input("Confirm password: ")
        if pwd1 != "" and pwd1 == pwd2:
            break
        print("Passwords fo not match or are empty. Try again!")

    new_row = join_csv([cust_id, name, phone, email, pwd1])                    # build a CSV-like line
    append_line(CUSTOMER_FILE, new_row)                                  # append to customers file
    print("Registered! Your customer ID is:", cust_id)                   # show the new id

def update_my_details():                                                 # define a function to edit your saved details
    lines = read_all_lines(CUSTOMER_FILE)                                # read every line from customers.txt into a list
    if len(lines) <= 1:                                                  # if the file has only the header (no data rows)
        print("No customers yet.")                                       # tell the user there’s nothing to edit
        return                                                           # stop the function

    cid = ask_existing_customer_login()                                  # ask for Customer ID + Password; returns a valid ID

    # find the row index for this customer
    idx = -1                                                             # we'll store the line number here (start with -1 = not found)
    cur = None                                                           # we'll store the current fields for this user here
    for i in range(1, len(lines)):                                       # loop over all data rows (skip header at index 0)
        parts = split_csv_line(lines[i])                                 # split the CSV-ish row into a list of fields
        if parts[0] == cid:                                              # if the first field (customer_id) matches the login ID
            idx = i                                                      # remember which line number this row is on
            cur = parts                                                  # remember the current values (list like [id,name,phone,email,password])
            break                                                        # stop looping—we found the row we need
    if idx == -1:                                                        # safety check—if not found (shouldn’t happen if login worked)
        print("Unexpected: customer not found.")                         # show a message so it’s clear something’s off
        return                                                           # stop the function

    print("Leave blank to keep current value in [brackets].")            # explain how to keep old values
    new_name  = safe_input("Name  [" + cur[1] + "]: ") or cur[1]         # ask for a new name; if blank, keep cur[1]
    new_phone = safe_input("Phone [" + cur[2] + "]: ") or cur[2]         # ask for a new phone; if blank, keep cur[2]
    new_email = safe_input("Email [" + cur[3] + "]: ") or cur[3]         # ask for a new email; if blank, keep cur[3]

    if not new_phone.isdigit():                                          # validate: phone should be digits only
        print("Phone must be digits only. Keeping old.")                 # show why we’re ignoring their input
        new_phone = cur[2]                                               # revert to the old phone number
    if "@" not in new_email:                                             # validate: email must contain '@' (very simple check)
        print("Email must contain '@'. Keeping old.")                    # show why we’re ignoring their input
        new_email = cur[3]                                               # revert to the old email

    # Optional password change
    change = safe_input("Change password? (Y/N): ").strip().upper()      # ask if they want to change password; normalize the answer
    if change == "Y":                                                    # if they said yes
        while True:                                                      # loop until they enter matching non-empty passwords
            p1 = safe_input("New password: ")                            # ask for new password
            p2 = safe_input("Confirm new password: ")                    # ask to confirm the same password
            if p1 != "" and p1 == p2:                                    # accept only if not empty and both match
                new_pass = p1                                            # store the new password
                break                                                    # leave the loop
            print("Passwords do not match or are empty. Try again.")     # otherwise, try again
    else:                                                                # if they said no
        new_pass = cur[4]                                                # keep the old password (position 4 in the row)

    # write once with all 5 columns (id, name, phone, email, password)
    lines[idx] = join_csv([cid, new_name, new_phone, new_email, new_pass])  # rebuild that one line with updated values
    write_all_lines(CUSTOMER_FILE, lines)                                # overwrite the whole file with our updated lines list
    print("Details updated.")                                            # confirm success to the user



# View current vs upcoming movies 
def view_all_movie_showtimes():                      # define a function with no inputs (we'll call it from the menu)
    # Load movies and showtimes
    movies = load_movies()                           # call our helper to read movie_listings.txt -> list of dicts (id + name)
    shows  = load_showtimes()                        # call our helper to read movie_showtimes.txt -> list of dicts (show info)

    # Basic empty check
    if len(movies) == 0 or len(shows) == 0:          # if either list is empty (no movies OR no showtimes)
        print("No movies or showtimes to display.")  # tell the user there’s nothing to list
        return                                       # leave the function early (stop here)

    # Map movie_id -> movie_name for easy lookup
    name_of = {}                                     # create an empty dictionary (we’ll fill it with id -> name)
    for m in movies:                                 # loop through every movie dictionary in the movies list
        name_of[m["movie_id"]] = m["movie_name"]     # store the name under its id, e.g. name_of["M0001"] = "Interstellar"

    # Print every showtime in a numbered list (keep date format as-is)
    print("=== All Movie Showtimes ===")             # print a simple heading so the output looks nice
    n = 1                                            # start our numbering at 1 (for "1.", "2.", "3.", ...)
    for s in shows:                                  # loop through every showtime dictionary in the shows list
        movie_name = name_of.get(                    # look up the movie title for this showtime’s movie_id
            s["movie_id"],                           # key to look up (e.g. "M0001")
            "(title not found)"                      # default text if the id is missing in our name_of map
        )
        print(str(n) + ". Movie:", movie_name)       # e.g. "1. Movie: Interstellar"  (str(n) turns 1 into "1")
        print("   date:", s["date"])                 # print the date exactly as stored, e.g. 2025-10-04
        print("   time:", s["start_time"])           # print the start time, e.g. 18:00
        print("   venue:", s["auditorium"])          # print the auditorium id, e.g. AUD01
        print()                                      # print a blank line to separate entries (just for readability)
        n = n + 1                                    # increase the number for the next showtime (1 -> 2 -> 3 ...)


# helpers for bookings 
def seats_taken_for_show(showtime_id):                                   # make a list of seats already booked for this show
    lines = read_all_lines(BOOKING_FILE)                                 # read booking rows
    taken = []                                                           # empty list for seat codes
    for i in range(1, len(lines)):                                       # skip header
        parts = split_csv_line(lines[i])                                 # split booking row
        if len(parts) >= 4 and parts[1] == showtime_id:                  # parts[1] is showtime_id
            seats_text = parts[3]                                        # parts[3] is seats like "A01|A02"
            pieces = seats_text.split("|")                               # split by pipe into a list
            for s in pieces:                                             # go through each seat text
                seat = s.strip()                                         # remove spaces
                if seat != "":                                           # ignore empty
                    taken.append(seat)                                   # remember this seat as taken
    return taken                                                         # return full list

# TASK 3: Book tickets / Cancel tickets
def book_ticket():                                                       # create a new booking row
    cid = ask_existing_customer_login()                                     # ask for a real customer id
    mid = ask_existing_movie_id()                                        # ask for a real movie id
    sid = ask_existing_showtime_id_for_movie(mid)                        # ask for a real showtime of that movie
    # choose seats
    while True:                                                          # keep asking until valid and free
        raw = safe_input("Seats (e.g. A01|A02): ")                       # ask for seat codes separated by |
        pieces = raw.split("|")                                          # split into a list
        chosen = []                                                      # will store cleaned unique seats
        for p in pieces:                                                 # check each typed piece
            s = p.strip()                                                # remove spaces
            if s != "" and s not in chosen:                              # ignore empty and duplicates
                chosen.append(s)                                         # keep it
        if len(chosen) == 0:                                             # must have at least one
            print("Enter at least one seat.")
            continue                                                     # ask again
        taken = seats_taken_for_show(sid)                                # list of already booked seats
        conflict = False                                                 # assume no conflicts first
        for s in chosen:                                                 # check each chosen seat
            if s in taken:                                               # if already taken
                print("Seat", s, "already taken. Pick others.")          # show message
                conflict = True                                          # mark conflict
        if conflict:                                                     # if any conflict happened
            continue                                                     # ask again
        # rebuild normalized seats text like "A01|A02|B03" using a loop
        seats_text = ""                                                  # start empty
        for i in range(len(chosen)):                                     # go through indexes
            if i == 0:                                                   # first element
                seats_text = chosen[i]                                   # assign directly
            else:                                                        # later elements
                seats_text = seats_text + "|" + chosen[i]                # add pipe and seat code
        break                                                            # leave loop; seats are valid
    # ticket counts
    normal = read_int("Normal tickets: ")                                # ask for normal count
    disc   = read_int("Discounted tickets: ")                            # ask for discounted count
    # build booking id and row
    bid = next_id_by_count(BOOKING_FILE, "B")                            # booking id like "B0001"
    tickets_text = str(normal) + "|" + str(disc)                         # store "normal|discount"
    new_row = join_csv([bid, sid, cid, seats_text, tickets_text])        # build the CSV-like line
    append_line(BOOKING_FILE, new_row)                                   # append to bookings file
    print("Booked! Your Booking ID is:", bid)                            # confirm to the user

def cancel_ticket():                                                     # delete one of my bookings
    lines = read_all_lines(BOOKING_FILE)                                 # read all bookings
    cid = ask_existing_customer_login()                                     # which customer
    # list my bookings and collect their ids
    my_ids = []                                                          # empty list to collect booking ids
    print("=== Your Bookings ===")                                       # heading
    for i in range(1, len(lines)):                                       # skip header
        parts = split_csv_line(lines[i])                                 # split row
        if len(parts) >= 3 and parts[2] == cid:                          # if booking belongs to me
            my_ids.append(parts[0])                                      # remember booking id
            print("Booking:", parts[0], "| Show:", parts[1], "| Seats:", parts[3])  # show a summary
    if len(my_ids) == 0:                                                 # if I have no bookings
        print("You have no bookings.")                                   # tell user
        return                                                           # nothing to cancel
    # ask which booking id to cancel
    while True:                                                          # keep asking until valid
        bid = safe_input("Enter Booking ID to cancel: ")                 # ask for the id
        if bid in my_ids:                                                # if id is one of my bookings
            break                                                        # good -> continue
        print("That booking doesn't belong to you. Try again.")          # otherwise loop
    # write back all rows except the one chosen
    new_lines = [lines[0]]                                               # start with header unchanged
    for i in range(1, len(lines)):                                       # loop through data rows
        parts = split_csv_line(lines[i])                                 # split row
        if parts[0] != bid:                                              # if this row is NOT the one we cancel
            new_lines.append(lines[i])                                   # keep it
    write_all_lines(BOOKING_FILE, new_lines)                             # overwrite file with remaining rows
    print("Booking", bid, "cancelled.")                                  # confirm

# Booking history / Seat info
def view_booking_history():                                              # print all bookings for a given customer
    lines = read_all_lines(BOOKING_FILE)                                 # read all bookings
    cid = ask_existing_customer_login()                                     # ask whose history
    any_printed = False                                                  # track if we showed anything
    print("=== Booking History for", cid, "===")                         # heading
    for i in range(1, len(lines)):                                       # skip header
        parts = split_csv_line(lines[i])                                 # split row
        if len(parts) >= 3 and parts[2] == cid:                          # if row belongs to this customer
            any_printed = True                                           # mark that we printed something
            print("Booking ID:", parts[0])                               # show booking id
            print(" Show ID:", parts[1])                                 # showtime id
            print(" Seats:", parts[3])                                   # seats text
            print(" Tickets (normal|discount):", parts[4])               # ticket counts text
            print("-" * 30)                                              # separator
    if not any_printed:                                                  # if nothing printed
        print("No bookings found.")                                      # message

def view_seat_info_for_showtime():                                       # show taken seats for a chosen showtime
    mid = ask_existing_movie_id()                                        # pick a valid movie
    sid = ask_existing_showtime_id_for_movie(mid)                        # pick a valid showtime for that movie
    taken = seats_taken_for_show(sid)                                    # list of taken seats
    print("=== Seat Info for", sid, "===")                               # heading
    print("Taken seats count:", len(taken))                              # how many
    if len(taken) == 0:                                                  # if none
        print("Taken seats: (none)")                                     # say none
    else:
        # build one line like "A01, A02, B03" using a loop
        line = ""                                                        # start empty
        for i in range(len(taken)):                                      # go through each taken seat
            if i == 0:                                                   # first one
                line = taken[i]                                          # just assign it
            else:                                                        # others
                line = line + ", " + taken[i]                            # add comma, space, and the seat
        print("Taken seats:", line)                                      # print the built line

# MENU (only the 4 tasks)
def main_customer():                                                              # main menu loop
    while True:                                                          # keep showing options until user exits
        print("\n=== CUSTOMER MENU ===")                                 # a blank line then the title
        print("[1] Register / Create account")                           # option 1
        print("[2] Update my account details")                           # option 2
        print("[3] View all movie showtimes (Movie/Date/Time/Venue)")                     # option 3
        print("[4] Book tickets")                                        # option 4
        print("[5] Cancel my ticket")                                    # option 5
        print("[6] View my booking history")                             # option 6
        print("[7] View seat info for a showtime")                       # option 7
        print("[0] Exit")                                                # option 0
        choice = read_int("Enter your choice: ")                          # read a number safely

        if choice == 1:   register_customer()                            # run register
        elif choice == 2: update_my_details()                            # run update
        elif choice == 3: view_all_movie_showtimes()             # run view current/upcoming
        elif choice == 4: book_ticket()                                  # run book
        elif choice == 5: cancel_ticket()                                # run cancel
        elif choice == 6: view_booking_history()                         # run history
        elif choice == 7: view_seat_info_for_showtime()                  # run seat info
        elif choice == 0:                                                 # exit
            main()                                                        # leave the loop and end program
        else:
            print("Invalid choice. Try again.")                          # anything else -> error then loop




def main():
    """
    Displays the main menu and dispatches to role-specific interfaces.

    Returns:
        None
    """
    clear_terminal()
    print("==== MAIN MENU ====\n\nAvailable role:\n-------------------")
    roles = ["Ticketing Clerk", "Cinema Manager", "Technician", "Customer"]

    for index, role in enumerate(roles, start=1):
        print(f'[{index}] {role}')
    print("-------------------")

    role_functions = {
        1: main_ticketing_clerk,
        2: main_cinema_manager,
        3: main_technician,
        4: main_customer,
    }

    while True:
        role_choice = validate_int("Select role (enter number 1-4): ")
        if role_choice in role_functions:
            break
        print(color_error_message("Invalid input: please enter a number 1-4."))
    confirmed = validate_yes_no(
        f'Confirm role: {roles[role_choice - 1].lower()}? [Y/N]: ') == "Y"
    if confirmed:
        clear_terminal()
        role_functions[role_choice]()
    else:
        clear_terminal()
        main()


if __name__ == "__main__":
    # This code will only run when the script is executed directly (ie. will not run when imported)
    clear_terminal()
    starting_message = "STARTING PROGRAM..."
    for char in starting_message:
        print(char, end="", flush=True)
        time.sleep(0.1)
    main()
