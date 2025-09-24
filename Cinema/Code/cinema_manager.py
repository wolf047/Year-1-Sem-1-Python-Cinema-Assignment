
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

# NOT USED
# def generate_seat_ids():
#     rows = "ABCDEFGHIJKLMN"
#     with open("Cinema/Database/auditorium_info.txt", "r") as f:
#         next(f)
#         for line in f:
#             entry = [i.strip() for i in line.strip().split(",")]
#             auditorium_id = entry[0]
#             for i in range(int(entry[3]) + 1):
#                 row = rows[i]
#                 for j in range(1, (int(entry[4]) + 1)):
#                     column = j
#                     seat_id = f'SEAT-{row}{column:02}'
#                     with open("Cinema/Database/auditorium_sitting.txt", "a") as g:
#                         seat = [seat_id, auditorium_id]
#                         g.write(", ".join(seat) + "\n")

# ---------------------------------------------------------------------------------------------
from datetime import datetime
import time
import os

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'


def color_error_message(prompt):
    """
    Wraps a string with ANSI escape codes to display it in red.

    Args:
        prompt (str): The error message to be colorized.

    Returns:
        str: The error message wrapped with red color and reset codes.
    """

    colored_prompt = RED + prompt + RESET
    return colored_prompt


def color_completion_message(prompt):
    """
    Wraps a string with ANSI escape codes to display it in green.

    Args:
        prompt (str): The completion message to be colorized.

    Returns:
        str: The completion message wrapped with green color and reset codes.
    """
    colored_prompt = GREEN + prompt + RESET
    return colored_prompt


def clear_terminal():
    """Clears the terminal screen.

    Returns:
        None
    """
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')


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
            print(color_error_message(
                "Invalid input: please enter a float to 2 decimals (eg. 0.00)."))


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
            print(color_error_message(
                "Invalid input: please enter a date in the format DD-MM-YYYY (eg. 31-12-2000)."))


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
            print(color_error_message(
                "Invalid input: please enter a time in the format HHMM (eg. 2359)."))


def lint_entry(value):
    """
    Formats a list or string to be entered in text file.

    Args:
        value (list or str): Item to be formatted. Lists are joined with "|". Joined lists or strings are wrapped in quotation marks if they contain a comma or space.

    Returns:
        str: Formatted string.
    """
    if isinstance(value, list):
        value = "|".join(value)
    value = str(value)
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
        next(f)
        second_line = f.readline()
        single_line = second_line == ""
    with open(filename, "a") as f:
        if single_line:
            f.write("\n")
        formatted_entry = []
        for item in entry_detail_list:
            formatted_entry.append(lint_entry(item))
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
                entry[detail_index] = lint_entry(entry_detail_item)
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
            entry = [i.strip() for i in line.split(",")]
            if entry[0] == entry_id:
                return entry
    return None


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
    Displays all movie listings in a formatted table.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/movie_listings.txt")
    while True:
        done = validate_yes_no("Return to cinema manager menu [Y/N]: ")
        if done == "Y":
            main_cinema_manager()
            break


def add_movie_listing():
    """
    Collects movie details from user input and adds a new movie listing entry.

    Returns:
        None
    """
    movie_id_no = id_counter("movie")
    movie_id = f'M{movie_id_no:04}'

    while True:
        movie_name = input("Enter movie name: ")
        if movie_name:
            break
        print(color_error_message(
            "Invalid input: movie listing must have movie name."))

    release_date = validate_date(
        "Enter release date (in the format DD-MM-YYYY): ")

    while True:
        running_time = validate_int(
            "Enter running time (as the total number of minutes): ")
        if 0 < running_time < 500:
            break
        print(color_error_message(
            "Invalid input: running time should be greater than 0 and lesser than 500."))

    genre = [genre.strip() for genre in input(
        "Enter genres (as a comma-delimited list): ").split(",")]

    classification_options = ["U", "P12", "13", "16", "18+", "18SG", "18SX"]
    for index, field in enumerate(classification_options, start=1):
        print(f'[{index}] {field}', end="   ")
    print()
    while True:
        classification_selection = validate_int(
            "Select classification (enter number 1-7): ")
        if (1 <= classification_selection <= 7):
            classification = classification_options[classification_selection - 1]
            break
        print(color_error_message("Invalid option: please enter a number 1-7."))

    spoken_language = input("Enter spoken language (full name): ")

    subtitle_language = [language.strip() for language in input(
        "Enter subtitle languages (full name, as a comma-delimited list): ").split(",")]

    directors = [director.strip() for director in input(
        "Enter director names (as a comma-delimited list): ").split(",")]

    casts = [cast.strip() for cast in input(
        "Enter cast names (as a comma-delimited list): ").split(",")]

    description = input("Enter movie description: ")

    eligibility_for_discount = validate_yes_no(
        "Select eligibility for discount (Y/N): ")

    movie_listing = [movie_id, movie_name, release_date, running_time, genre, classification,
                     spoken_language, subtitle_language, directors, casts, description, eligibility_for_discount]
    add_entry("Cinema/Database/movie_listings.txt", movie_listing)
    notification = f'Movie listing for {movie_id}: "{movie_name}" created.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Add another movie listing [Y/N]: ") == "Y"
    if another:
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
    movie_listing = lookup_entry(
        "Cinema/Database/movie_listings.txt", entry_id=movie_id)
    if not movie_listing:
        print(color_error_message("Invalid input: this movie ID does not exist."))
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_movie_listing()
        else:
            main_cinema_manager()

    details = lookup_entry(
        "Cinema/Database/movie_listings.txt", header=1)
    for index, field in enumerate(details[1:], start=1):
        print(f'[{index}] {field}')

    detail_selection = validate_int("Select detail (enter number 1-10): ")

    match detail_selection:
        case 1:
            while True:
                update_details = input("Enter update movie name: ")
                if update_details:
                    break
                print(color_error_message(
                    "Invalid input: movie listing must have movie name."))
        case 2:
            update_details = validate_date(
                "Enter updated release date (in the format DD-MM-YYYY): ")
        case 3:
            while True:
                update_details = validate_int("Enter updated running time: ")
                if 0 < update_details < 500:
                    break
                print(color_error_message(
                    "Invalid input: running time should be greater than 0 and lesser than 500."))
        case 4:
            update_details = [genre.strip() for genre in input(
                "Enter updated genres (enter comma-delimited list): ").split(",")]
        case 5:
            classification_options = [
                "U", "P12", "13", "16", "18+", "18SG", "18SX"]
            for index, field in enumerate(classification_options, start=1):
                print(f'[{index}] {field}', end="   ")
            print()
            while True:
                classification_selection = validate_int(
                    "Select classification (enter number 1-7): ")
                if (1 <= classification_selection <= 7):
                    update_details = classification_options[classification_selection - 1]
                    break
                print(color_error_message(
                    "Invalid option: please enter a number 1-7."))
        case 6:
            update_details = input(
                "Enter updated spoken language (full form): ")
        case 7:
            update_details = [language.strip() for language in input(
                "Enter updated subtitle languages (full form, enter comma-delimited list): ").split(",")]
        case 8:
            update_details = [director.strip() for director in input(
                "Enter updated director names (enter comma-delimited list): ").split(",")]
        case 9:
            update_details = [cast.strip() for cast in input(
                "Enter updated cast names (enter comma-delimited list): ").split(",")]
        case 10:
            update_details = input("Enter updated description: ")
        case 11:
            update_details = validate_yes_no(
                "Select updated eligibility for discount (Y/N): ")
        case _:
            print(color_error_message("Invalid option."))
            detail_selection = validate_int(
                "Select detail (enter number 1-10): ")

    update_entry("Cinema/Database/movie_listings.txt",
                 movie_id, detail_selection, update_details)
    notification = f'Listing for {movie_id} updated.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Update another movie listing [Y/N]: ") == "Y"
    if another:
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
    movie_listing = lookup_entry(
        "Cinema/Database/movie_listings.txt", entry_id=movie_id)
    if not movie_listing:
        print(color_error_message("Invalid input: this movie ID does not exist."))
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            remove_movie_listing()
        else:
            main_cinema_manager()
    remove_entry("Cinema/Database/movie_listings.txt", movie_id)
    notification = f'Listing for {movie_id} removed.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Remove another movie listing [Y/N]: ") == "Y"
    if another:
        clear_terminal()
        remove_movie_listing()
    else:
        main_cinema_manager()


def view_showtime():
    """
    Displays all movie showtimes in a formatted table.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/movie_showtimes.txt")
    while True:
        done = validate_yes_no("Return to cinema manager menu [Y/N]: ")
        if done == "Y":
            main_cinema_manager()
            break


def add_showtime():
    """
    Collects showtime details from user input and adds a new movie showtime entry.

    Returns:
        None
    """
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
        entry = lookup_entry(
            "Cinema/Database/discount_policies.txt", entry_id=discount_id)
        if entry[2] == "fixed":
            discounted_price = round((normal_price - float(entry[3])), 2)
        elif entry[2] == "percentage":
            discounted_price = round((normal_price * (1 - float(entry[3]))), 2)
        return discounted_price

    showtime_id_no = id_counter("showtime")
    showtime_id = f'ST{showtime_id_no:05}'

    movie_id = input("Enter movie ID: ").upper().strip()
    movie_listing = lookup_entry(
        "Cinema/Database/movie_listings.txt", entry_id=movie_id)
    if not movie_listing:
        print(color_error_message("Invalid input: this movie ID does not exist."))
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_showtime()
        else:
            main_cinema_manager()

    auditorium_id = input("Enter auditorium ID: ").upper().strip()
    auditorium_info = lookup_entry(
        "Cinema/Database/auditorium_info.txt", entry_id=auditorium_id)
    if not auditorium_info:
        print("Invalid input: this auditorium ID does not exist.")
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            add_showtime()
        else:
            main_cinema_manager()

    normal_price = round(float(auditorium_info[5]), 2)
    date = validate_date("Enter date (enter in the format DD-MM-YYYY): ")
    start_time = validate_time("Enter start time (enter in the format HHMM): ")
    end_time = validate_time("Enter end time (enter in the format HHMM): ")

    discounted_price = None

    if movie_listing[11] == "Y":
        discount_id = input("Enter discount ID: ").upper().strip()
        discount_policy = lookup_entry(
            "Cinema/Database/discount_policies.txt", entry_id=discount_id)
        if not discount_policy:
            print(color_error_message(
                "Invalid input: this discount ID does not exist."))
            tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
            if tryagain:
                clear_terminal()
                add_showtime()
            else:
                main_cinema_manager()

        discounted_price = calculate_discount(discount_id, normal_price)

    showtime = [showtime_id, movie_id,
                auditorium_id, date, start_time, end_time, f'{normal_price:.2f}', f'{discounted_price:.2f}' if discounted_price is not None else ""]
    add_entry("Cinema/Database/movie_showtimes.txt", showtime)
    notification = f'Showtime {showtime_id} for {movie_id} created.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Add another movie showtime [Y/N]: ") == "Y"
    if another:
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
    showtime_id = input("Enter ID of showtime to be edited: ").upper().strip()
    movie_showtime = lookup_entry(
        "Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
    if not movie_showtime:
        print("Invalid input: this showtime ID does not exist.")
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            update_showtime()
        else:
            main_cinema_manager()

    details = lookup_entry(
        "Cinema/Database/movie_showtimes.txt", header=1)
    for index, field in enumerate(details[1: 6], start=1):
        print(f'[{index}] {field}')

    detail_selection = validate_int("Select detail (enter number 1-5): ")

    match detail_selection:
        case 1:
            update_details = input("Enter updated movie ID: ").upper().strip()
            movie_listing = lookup_entry(
                "Cinema/Database/movie_listings.txt", entry_id=update_details)
            if not movie_listing:
                print("Invalid input: this movie ID does not exist.")
                tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_showtime()
                else:
                    main_cinema_manager()
        case 2:
            update_details = input(
                "Enter updated auditorium ID: ").upper().strip()
            auditorium_info = lookup_entry(
                "Cinema/Database/auditorium_info.txt", entry_id=update_details)
            if not auditorium_info:
                print("Invalid input: this auditorium ID does not exist.")
                tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_showtime()
                else:
                    main_cinema_manager()
        case 3:
            update_details = validate_date(
                "Enter updated date (enter in the format DD-MM-YYYY): ")
        case 4:
            update_details = validate_time(
                "Enter updated start time (enter in the format HHMM): ")
        case 5:
            update_details = validate_time(
                "Enter updated end time (enter in the format HHMM): ")
        case _:
            print("Invalid option")
            detail_selection = validate_int(
                "Select detail (enter number 1-5): ")

    update_entry("Cinema/Database/movie_showtimes.txt",
                 showtime_id, detail_selection, update_details)
    notification = f'Listing for {showtime_id} updated.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Update another movie showtime [Y/N]: ") == "Y"
    if another:
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
    movie_showtime = lookup_entry(
        "Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
    if not movie_showtime:
        print(color_error_message("Invalid input: this showtime ID does not exist."))
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            remove_showtime()
        else:
            main_cinema_manager()
    remove_entry("Cinema/Database/movie_showtimes.txt", showtime_id)
    notification = f'Listing for {showtime_id} removed.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Remove another movie showtime [Y/N]: ") == "Y"
    if another:
        clear_terminal()
        remove_showtime()
    else:
        main_cinema_manager()


def view_discount():
    """
    Displays all discount policies in a formatted table.

    Returns:
        None
    """
    view_all_entries("Cinema/Database/discount_policies.txt")
    while True:
        done = validate_yes_no("Return to cinema manager menu [Y/N]: ")
        if done == "Y":
            main_cinema_manager()
            break


def add_discount():
    """
    Collects discount details from user input and adds a new duscount policy entry.

    Returns:
        None
    """
    discount_id_no = id_counter("discount")
    discount_id = f'D{discount_id_no:02}'

    while True:
        discount_name = input("Enter discount name: ")
        if discount_name:
            break
        print(color_error_message(
            "Invalid input: discount policy must have discount name."))

    discount_type_options = ["fixed", "percentage"]
    for index, field in enumerate(discount_type_options[0: 2], start=1):
        print(f'[{index}] {field}', end="   ")
    print()
    discount_type_selection = validate_int(
        "Select discount type (enter number 1-2): ")
    match discount_type_selection:
        case 1:
            discount_type = discount_type_options[0]
            discount_amount = validate_float(
                "Enter discount amount (enter as a 2 decimal float): ")
            discount_rate = None
        case 2:
            discount_type = discount_type_options[1]
            discount_amount = None
            discount_rate = validate_float(
                "Enter discount rate (enter as a 2 decimal float): ")
        case _:
            print(color_error_message("Invalid option."))
            discount_type_selection = validate_int(
                "Select discount type (enter number 1-2): ")
    discount_policies = input("Enter discount policies: ")

    discount_policy = [discount_id, discount_name, discount_type,
                       f'{discount_amount:.2f}' if discount_amount is not None else "", f'{discount_rate:.2f}' if discount_rate is not None else "", discount_policies]
    add_entry("Cinema/Database/discount_policies.txt", discount_policy)
    notification = f'Discount {discount_id} created.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Add another discount policy [Y/N]: ") == "Y"
    if another:
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
    for index, field in enumerate(details[1: 6], start=1):
        print(f'[{index}] {field}')

    detail_selection = validate_int("Select detail (enter number 1-5): ")

    match detail_selection:
        case 1:
            while True:
                discount_name = input("Enter discount name: ")
                if discount_name:
                    break
                print(color_error_message(
                    "Invalid input: discount policy must have discount name."))
        case 2:
            update_details = []
            if discount_policy[2] == "fixed":
                discount_type = "percentage"
                update_details[0] = discount_type
                update_details[1] = validate_float(
                    "Enter updated discount amount (enter as a 2 decimal float): ")
                update_details[2] = None
            elif discount_policy[2] == "percentage":
                discount_type = "fixed"
                update_details[0] = discount_type
                update_details[1] = None
                update_details[2] = validate_float(
                    "Enter updated discount rate (enter as a 2 decimal float): ")
        case 3:
            if discount_policy[2] != "fixed":
                print(color_error_message(
                    "Invalid selection: discount amount cannot be edited for percentage discounts."))
                tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_discount()
                else:
                    main_cinema_manager()
            else:
                update_details = validate_float(
                    "Enter updated discount amount (enter as a 2 decimal float): ")
        case 4:
            if discount_policy[2] != "percentage":
                print(color_error_message(
                    "Invalid selection: discount rate cannot be edited for fixed discounts."))
                tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_discount()
                else:
                    main_cinema_manager()
            else:
                update_details = validate_float(
                    "Enter updated discount rate (enter as a 2 decimal float): ")
        case 5:
            update_details = input(
                "Enter updated discount policies: ")
        case _:
            print(color_error_message("Invalid option."))
            detail_selection = validate_int(
                "Select detail (enter number 1-5): ")

    if isinstance(update_details, list):
        update_entry("Cinema/Database/discount_policies.txt",
                     discount_id, 2, update_details[0])
        update_entry("Cinema/Database/discount_policies.txt",
                     discount_id, 3, update_details[1])
        update_entry("Cinema/Database/discount_policies.txt",
                     discount_id, 4, update_details[2])
    else:
        update_entry("Cinema/Database/discount_policies.txt",
                     discount_id, detail_selection, update_details)
    notification = f'Listing for {discount_id} updated.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Update another discount policy [Y/N]: ") == "Y"
    if another:
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
    discount_policy = lookup_entry(
        "Cinema/Database/discount_policies.txt", entry_id=discount_id)
    if not discount_policy:
        print(color_error_message("Invalid input: this discount ID does not exist."))
        tryagain = validate_yes_no("Try again [Y/N]: ") == "Y"
        if tryagain:
            clear_terminal()
            remove_movie_listing()
        else:
            main_cinema_manager()
    remove_entry("Cinema/Database/discount_policies.txt", discount_id)
    notification = f'Listing for {discount_id} removed.'
    print("-" * len(notification))
    print(color_completion_message(notification))
    print("\n")
    another = validate_yes_no("Remove another discount policy [Y/N]: ") == "Y"
    if another:
        clear_terminal()
        remove_discount()
    else:
        main_cinema_manager()


def view_booking_reports():
    """
    Displays booking entries, optionally filtered by movie ID, in a formatted table.

    Returns:
        None
    """
    def format_row(row, widths):
        return "   ".join(item.strip().ljust(width) for item, width in zip(row, widths))

    specific_movie = validate_yes_no(
        "Do you want to view the report for a specific movie? [Y/N] ") == "Y"
    entries = []
    with open("Cinema/Database/movie_bookings.txt", "r") as f:
        header = f.readline().strip().upper().split(",")

    if specific_movie:
        movie_id = input("Enter movie ID: ").upper().strip()
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for showtime_line in f:
                showtime_entry = [i.strip() for i in showtime_line.split(",")]
                if showtime_entry[1] == movie_id:
                    with open("Cinema/Database/movie_bookings.txt", "r") as g:
                        for booking_line in g:
                            entry = [i.strip()
                                     for i in booking_line.split(",")]
                            if entry[1] == showtime_entry[0]:
                                entries.append(entry)

    else:
        with open("Cinema/Database/movie_bookings.txt", "r") as f:
            next(f)
            entries = [[i.strip() for i in line.strip().split(",")]
                       for line in f.readlines()]

    all_rows = [header] + entries
    col_widths = [max(len(i.strip()) for i in col)
                  for col in zip(*all_rows)]
    print(format_row(header, col_widths))
    print("-" * sum(col_widths) + "-" * (3 * (len(col_widths) - 1)))
    if not entries:
        print("No entries found.")
        main_cinema_manager()
    for entry in entries:
        print(format_row(entry, col_widths))
    done = validate_yes_no("Return to cinema manager menu [Y/N]: ") == "Y"
    while True:
        done = validate_yes_no("Return to cinema manager menu [Y/N]: ")
        if done == "Y":
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
            showtime_id = booking[1]
            tickets = [int(i.strip()) for i in booking[4].split("|")]

            movie_showtime = lookup_entry(
                "Cinema/Database/movie_showtimes.txt", entry_id=showtime_id)
            normal_total_revenue += round((tickets[0]
                                          * float(movie_showtime[6])), 2)
            discounted_total_revenue += round((
                tickets[1] * float(movie_showtime[7])), 2)

    total_revenue = normal_total_revenue + discounted_total_revenue
    print(
        f'Revenue from normal tickets: {normal_total_revenue:.2f}\nRevenue from discounted tickets: {discounted_total_revenue:.2f}\nTotal revenue: {total_revenue}')
    done = validate_yes_no("Return to cinema manager menu [Y/N]: ") == "Y"
    while True:
        done = validate_yes_no("Return to cinema manager menu [Y/N]: ")
        if done == "Y":
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
               "Add discount", "Update discount", "Remove discount", "View booking report", "View revenue summary", "Exit cinema manager role"]

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
        13: view_booking_reports,
        14: view_revenue_summary,
        15: main
    }

    while True:
        action_choice = validate_int("Select action (enter number 1-15): ")
        if action_choice in action_functions:
            break
        print("Invalid input: please enter a number between 1 and 15.")
    confirmed = validate_yes_no(
        f'Do you want to {actions[action_choice - 1].lower()} [Y/N]: ') == "Y"
    if confirmed:
        clear_terminal()
        action_functions[action_choice]()
    else:
        clear_terminal()
        main_cinema_manager()


# MAIN MENU
def main():
    """
    Displays the main menu and dispatches to role-specific interfaces.

    Returns:
        None
    """
    clear_terminal()
    print("==== MAIN MENU ====\n\nAvailable role:\n------------------")
    roles = ["Ticketing Clerk", "Cinema Manager", "Technician", "Customer"]

    for index, role in enumerate(roles, start=1):
        print(f'[{index}] {role}')
    print("------------------")

    role_functions = {
        # 1: main_ticketing_clerk,
        2: main_cinema_manager,
        # 3: main_technician,
        # 4: main_customer,
    }

    while True:
        role_choice = validate_int("Select role (enter number 1-4): ")
        if role_choice in role_functions:
            break
        print("Invalid input: please enter a number between 1 and 4.")
    confirmed = validate_yes_no(
        f'Confirm role {roles[role_choice - 1].lower()} [Y/N]: ') == "Y"
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
