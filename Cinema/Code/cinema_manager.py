from datetime import datetime, timedelta
import time
import os

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

AUDITORIUM_OPTIONS = ["AUD01", "AUD02", "AUD03", "AUD04", "AUD05", "AUD06", "AUD07", "AUD08"]
CLASSIFICATION_OPTIONS = ["U", "P12", "13", "16", "18+", "18SG", "18SX"]
BUFFER = timedelta(minutes=15)
TIME_NOW = datetime.now()

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
    try:
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
    except FileNotFoundError:
        print(color_error_message(f'Error: {filename} file not found.'))
        return


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
    try:
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
    except FileNotFoundError:
        print(color_error_message(f'Error: {filename} file not found.'))
        return


def remove_entry(filename, entry_id):
    """
    Removes a specific entry within a text file.

    Args:
        filename (str): Path to the file containing the entry.
        entry_id (str): ID of the entry to be removed.

    Returns:
        None
    """
    try: 
        with open(filename, "r") as f:
            entries = f.readlines()
            updated_entries = []
            for entry in entries:
                entry = [i.strip() for i in entry.split(",")]
                if entry[0] != entry_id:
                    updated_entries.append(", ".join(entry) + "\n")
        with open(filename, "w") as f:
            f.writelines(updated_entries)
    except FileNotFoundError:
        print(color_error_message(f'Error: {filename} file not found.'))
        return


def view_all_entries(filename):
    """
    Displays all entries from a text file.

    Args:
        filename (str): Path to the file containing the entries.

    Returns:
        None
    """
    try:
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
    except FileNotFoundError:
        print(color_error_message(f'Error: {filename} file not found.'))
        return None


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
    try: 
        with open(filename, "r") as f:
            if header:
                details = [detail.strip() for detail in f.readline().split(",")]
                return details
            for line in f:
                entry = [i.strip() for i in split_line(line)]
                if entry[0] == entry_id:
                    return entry
        return None
    except FileNotFoundError:
        print(color_error_message(f'Error: {filename} file not found.'))
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

    Reads the current ID value from a text file specific to the item type, increments it, writes the updated value back to the file, and returns the original ID. 
    
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
        if item_counted == "movie":
            with open("Cinema/Database/movie_listings.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 1:
                    prev_id_no = int(lines[-1][1:4])
                    id_no = prev_id_no + 1
                else:
                    id_no = 1
        elif item_counted == "showtime":
            with open("Cinema/Database/movie_showtimes.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 1:
                    prev_id_no = int(lines[-1][2:6])
                    id_no = prev_id_no + 1
                else:
                    id_no = 1
        elif item_counted == "discount":
            with open("Cinema/Database/discount_policies.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 1:
                    prev_id_no = int(lines[-1][1:3])
                    id_no = prev_id_no + 1
                else:
                    id_no = 1
        else:
            return
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

    while True:
        date = validate_date("Enter date (DD-MM-YYYY): ")
        parsed_date = datetime.strptime(date, "%d-%m-%Y")
        if parsed_date > TIME_NOW:
            break
        print(color_error_message("Invalid input: showtime date should not be before today."))
       
    duration = timedelta(minutes=int(movie_listing[3]))
    start_time = validate_time("Enter start time (HHMM): ")
    parsed_start_time = datetime.strptime(start_time, "%H%M")
    parsed_end_time = round_time(parsed_start_time + duration)
    end_time = datetime.strftime(parsed_end_time, "%H%M")
    same_day_showtimes = []
    same_time_showtimes = []
    try:
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for line in f:
                entry = [i.strip() for i in line.split(",")]
                if entry[3] == date:
                    same_day_showtimes.append(entry)
    except FileNotFoundError:
        print(color_error_message(f'Error: "Cinema/Database/movie_showtimes.txt" file not found.'))
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
                 
    auditoriums_under_maintenance = []
    try:
        with open("Cinema/Database/technician_issues.txt", "r") as f:
            for line in f:
                entry = [i.strip() for i in line.split(",")]
                print(entry)
                if entry[2] == "Under Maintenance":   
                    est_repair = entry[4]
                    est_repair_date_time = [i.strip() for i in est_repair.split(" ")]
                    est_repaired_date = est_repair_date_time[0]
                    est_repaired_time = est_repair_date_time[1]
                    parsed_est_repaired_date = datetime.strptime(est_repaired_date, "%d-%m-%Y")
                    parsed_est_repaired_time = datetime.strptime(est_repaired_time, "%I:%M%p")
                    if parsed_est_repaired_date == parsed_date and parsed_est_repaired_time > parsed_end_time:
                        auditoriums_under_maintenance.append(entry)
                    elif parsed_est_repaired_date > parsed_date:
                        auditoriums_under_maintenance.append(entry)
    except FileNotFoundError:
        print(color_error_message(f'Error: "Cinema/Database/technician_issues.txt" file not found.'))
    for maintenance in auditoriums_under_maintenance:
        unavailable_auditorium_id = maintenance[0]
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
        try:
            with open("Cinema/Database/movie_showtimes.txt", "r") as f:
                for line in f:
                    entry = [i.strip() for i in line.split(",")]
                    if entry[3] == date:
                        same_day_showtimes.append(entry)
        except FileNotFoundError:
            print(color_error_message(f'Error: "Cinema/Database/movie_showtimes.txt" file not found.'))
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
                
        #Remove under maintenance audis
        auditoriums_under_maintenance = []
        try:
            with open("Cinema/Database/technician_issues.txt", "r") as f:
                for line in f:
                    entry = [i.strip() for i in line.split(",")]
                    print(entry)
                    if entry[2] == "Under Maintenance":   
                        est_repair = entry[4]
                        est_repair_date_time = [i.strip() for i in est_repair.split(" ")]
                        est_repaired_date = est_repair_date_time[0]
                        est_repaired_time = est_repair_date_time[1]
                        parsed_est_repaired_date = datetime.strptime(est_repaired_date, "%d-%m-%Y")
                        parsed_est_repaired_time = datetime.strptime(est_repaired_time, "%I:%M%p")
                        if parsed_est_repaired_date == parsed_date and parsed_est_repaired_time > parsed_end_time:
                            auditoriums_under_maintenance.append(entry)
                        elif parsed_est_repaired_date > parsed_date:
                            auditoriums_under_maintenance.append(entry)
        except FileNotFoundError:
            print(color_error_message(f'Error: "Cinema/Database/technician_issues.txt" file not found.'))
        for maintenance in auditoriums_under_maintenance:
            unavailable_auditorium_id = maintenance[0]
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

    date = movie_showtime[3]
    parsed_date = datetime.strptime(date, "%d-%m-%Y")
    if parsed_date < TIME_NOW:
        print(color_error_message("Invalid input: past showtimes cannot be updated."))
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
            start_time = movie_showtime[4]
            update_details = check_auditorium_availability(date, start_time, showtime_id)
        case 3:
            while True:
                date = validate_date("Enter updated date (DD-MM-YYYY): ")
                parsed_date = datetime.strptime(date, "%d-%m-%Y")
                if parsed_date > TIME_NOW:
                    break
                print(color_error_message("Invalid input: showtime date should not be before today."))
            start_time = movie_showtime[4]
            update_details = check_auditorium_availability(date, start_time, showtime_id)
        case 4:
            start_time = validate_time("Enter updated start time (HHMM): ")
            update_details = check_auditorium_availability(date, start_time, showtime_id)
        case 5:
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
            else:
                print(color_error_message("Error: current discount type is neither fixed nor percentage."))
                tryagain = validate_yes_no("Try again? [Y/N]: ") == "Y"
                if tryagain:
                    clear_terminal()
                    update_discount()
                else:
                    main_cinema_manager()
            update_details = [discount_type, f'{discount_amount:.2f}' if discount_amount is not None else "", f'{discount_rate:.2f}' if discount_rate is not None else ""]
        case 3:
            if discount_policy[2] != "fixed":
                print(color_error_message("Invalid option: discount amount cannot be edited for percentage discounts."))
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
                print(color_error_message("Invalid option: discount rate cannot be edited for fixed discounts."))
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
            
        try:
            with open("Cinema/Database/movie_showtimes.txt", "r") as f:
                for line in f:
                    showtime = [i.strip() for i in line.split(",")]
                    if len(showtime) == 9:
                        if showtime[8] == discount_id:
                            normal_price = showtime[6]
                            discounted_price = calculate_discount(discount_id, normal_price)
                            update_entry("Cinema/Database/movie_showtimes.txt", showtime[0], 7, discounted_price)
        except FileNotFoundError:
            print(color_error_message(f'Error: "Cinema/Database/movie_showtimes.txt" file not found.'))
        
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
    try:
        with open("Cinema/Database/movie_bookings.txt", "r") as f:
            header = f.readline().upper()
    except FileNotFoundError:
        print(color_error_message(f'Error: "Cinema/Database/movie_bookings.txt" file not found.'))
        
    header = [i.strip() for i in header.split(",")]
    header.insert(1, "MOVIE_NAME")
    header.insert(2, "DATE")
    header.insert(3, "START_TIME")
    header = ", ".join(header)

    if specific_movie:
        movie_id = input("Enter movie ID: ").upper().strip()
        try:
            with open("Cinema/Database/movie_showtimes.txt", "r") as f:
                for showtime_line in f:
                    showtime_entry = [i.strip() for i in showtime_line.split(",")]
                    if showtime_entry[1] == movie_id:
                        try:
                            with open("Cinema/Database/movie_bookings.txt", "r") as g:
                                for booking_line in g:
                                    entry = [i.strip() for i in booking_line.split(",")]
                                    if entry[1] == showtime_entry[0]:
                                        entries.append(", ".join(entry) + "\n")
                        except FileNotFoundError:
                            print(color_error_message(f'Error: "Cinema/Database/movie_bookings.txt" file not found.'))
        except FileNotFoundError:
            print(color_error_message(f'Error: "Cinema/Database/movie_showtimes.txt" file not found.'))

    else:
        try:
            with open("Cinema/Database/movie_bookings.txt", "r") as f:
                next(f)
                entries = f.readlines()
        except FileNotFoundError:
            print(color_error_message(f'Error: "Cinema/Database/movie_bookings.txt" file not found.'))
            
    booking_info = []
    
    for booking in entries:
        booking = [i.strip() for i in booking.split(",")]
        showtime_id = booking[1]
        try:
            with open("Cinema/Database/movie_showtimes.txt", "r") as f:
                for showtime_line in f:
                    showtime_entry = [i.strip() for i in showtime_line.split(",")]
                    if showtime_entry[0] == showtime_id:
                        movie_id = showtime_entry[1]
                        try:
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
                        except FileNotFoundError:
                            print(color_error_message(f'Error: "Cinema/Database/movie_listings.txt" file not found.'))
        except FileNotFoundError:
            print(color_error_message(f'Error: "Cinema/Database/movie_showtimes.txt" file not found.'))
                    
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
    try:
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
    except FileNotFoundError:
        print(color_error_message(f'Error: "Cinema/Database/movie_bookings.txt" file not found.'))

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


# MAIN MENU
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
    clear_terminal()
    starting_message = "STARTING PROGRAM..."
    for char in starting_message:
        print(char, end="", flush=True)
        time.sleep(0.1)
    main()
