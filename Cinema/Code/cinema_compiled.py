from datetime import datetime, timedelta
import time
import os

#------------------------- TICKETING CLERK --------------------------------------------------
# File names - Change these if your files have different names
MOVIE_FILE = "Cinema/Database/movie_listings.txt"
SHOWTIME_FILE = "Cinema/Database/movie_showtimes.txt"
BOOKING_FILE = "movie_bookings.txt"
AUDITORIUM_FILE = "auditorium_info.txt"


def view_movies():
    """Show all movies"""
    print("\n========== AVAILABLE MOVIES ==========")

    try:
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
    except FileNotFoundError:
        print(f"ERROR: {MOVIE_FILE} not found!")
    except Exception as e:
        print(f"ERROR: Could not read movies")


def view_auditoriums():
    """Show all auditoriums"""
    print("\n========== AUDITORIUMS ==========")

    try:
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
    except FileNotFoundError:
        print(f"ERROR: {AUDITORIUM_FILE} not found!")
    except Exception as e:
        print(f"ERROR: Could not read auditoriums")


def view_showtimes():
    """Show all showtimes"""
    print("\n========== MOVIE SHOWTIMES ==========")

    try:
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
    except FileNotFoundError:
        print(f"ERROR: {SHOWTIME_FILE} not found!")
    except Exception as e:
        print(f"ERROR: Could not read showtimes")


def view_bookings():
    """Show all bookings"""
    print("\n========== ALL BOOKINGS ==========")

    try:
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
    except FileNotFoundError:
        print(f"ERROR: {BOOKING_FILE} not found!")
    except Exception as e:
        print(f"ERROR: Could not read bookings")


def book_ticket():
    """Book a new ticket"""
    print("\n========== BOOK TICKET ==========")

    view_movies()
    view_auditoriums()
    view_showtimes()

    # Get booking info with validation for each field
    while True:
        try:
            print("\nEnter details:")

            # Get and validate Movie ID
            while True:
                movie_id = input("Movie ID: ").strip()
                if not movie_id:
                    print("ERROR: Movie ID required!")
                    continue

                try:
                    file = open(MOVIE_FILE, 'r')
                    lines = file.readlines()
                    file.close()

                    valid_movie = False
                    for i in range(1, len(lines)):
                        if lines[i].strip() == "":
                            continue
                        parts = lines[i].split(',')
                        if parts[0].strip() == movie_id:
                            valid_movie = True
                            break

                    if not valid_movie:
                        print(f"ERROR: Movie {movie_id} not found! Try again.")
                        continue
                    break

                except FileNotFoundError:
                    print(f"ERROR: {MOVIE_FILE} not found!")
                    return

            # Get and validate Auditorium ID
            while True:
                auditorium_id = input("Auditorium ID: ").strip()
                if not auditorium_id:
                    print("ERROR: Auditorium ID required!")
                    continue

                try:
                    file = open(AUDITORIUM_FILE, 'r')
                    lines = file.readlines()
                    file.close()

                    valid_auditorium = False
                    for i in range(1, len(lines)):
                        if lines[i].strip() == "":
                            continue
                        parts = lines[i].split(',')
                        if parts[0].strip() == auditorium_id:
                            valid_auditorium = True
                            break

                    if not valid_auditorium:
                        print(f"ERROR: Auditorium {auditorium_id} not found! Try again.")
                        continue
                    break

                except FileNotFoundError:
                    print(f"ERROR: {AUDITORIUM_FILE} not found!")
                    return

            # Get and validate Showtime ID
            while True:
                showtime_id = input("Showtime ID: ").strip()
                if not showtime_id:
                    print("ERROR: Showtime ID required!")
                    continue

                try:
                    file = open(SHOWTIME_FILE, 'r')
                    lines = file.readlines()
                    file.close()

                    valid_showtime = False
                    for i in range(1, len(lines)):
                        if lines[i].strip() == "":
                            continue
                        parts = lines[i].split(',')
                        if parts[0].strip() == showtime_id:
                            valid_showtime = True
                            break

                    if not valid_showtime:
                        print(f"ERROR: Showtime {showtime_id} not found! Try again.")
                        continue
                    break

                except FileNotFoundError:
                    print(f"ERROR: {SHOWTIME_FILE} not found!")
                    return

            # Get Customer ID
            while True:
                customer_id = input("Customer ID: ").strip()
                if not customer_id:
                    print("ERROR: Customer ID required!")
                    continue
                break

            # Get and validate Seats
            while True:
                seats = input("Seats (A1 or A1|A2): ").strip()
                if not seats:
                    print("ERROR: Seats required!")
                    continue
                break

            # Get and validate Tickets
            while True:
                tickets = input("Tickets (normal|discount like 1|0): ").strip()
                if not tickets:
                    print("ERROR: Tickets required!")
                    continue

                if "|" not in tickets:
                    print("ERROR: Tickets must be like 1|0 or 2|1. Try again.")
                    continue

                ticket_parts = tickets.split('|')
                if len(ticket_parts) != 2:
                    print("ERROR: Tickets must have 2 numbers (normal|discount). Try again.")
                    continue

                try:
                    normal = int(ticket_parts[0])
                    discount = int(ticket_parts[1])
                    break
                except ValueError:
                    print("ERROR: Tickets must be numbers! Try again.")
                    continue

            # Count seats
            if "|" in seats:
                seat_list = seats.split('|')
                total_seats = len(seat_list)
            else:
                seat_list = [seats]
                total_seats = 1

            total_tickets = normal + discount

            # Check seats = tickets
            if total_seats != total_tickets:
                print(f"\nERROR: {total_seats} seats but {total_tickets} tickets!")
                print("Please enter booking details again.\n")
                continue

            # Check for duplicate seats
            try:
                file = open(BOOKING_FILE, 'r')
                lines = file.readlines()
                file.close()

                seat_taken = False
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
                                seat_taken = True
                                break

                        if seat_taken:
                            break

                if seat_taken:
                    retry = input("Try again? (Y/N): ").strip().upper()
                    if retry != "Y":
                        return
                    continue

            except FileNotFoundError:
                pass

            # Get price from showtime file
            try:
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
                        normal_price = float(parts[6].strip())
                        discounted_price_str = parts[7].strip()

                        if discounted_price_str != "" and float(discounted_price_str) > 0:
                            discount_price = float(discounted_price_str)
                        else:
                            discount_price = normal_price
                        break

                if normal_price is None:
                    print(f"\nERROR: Showtime {showtime_id} not found!")
                    retry = input("Try again? (Y/N): ").strip().upper()
                    if retry != "Y":
                        return
                    continue

            except (ValueError, IndexError):
                print("\nERROR: Invalid price data in showtime file!")
                return

            total_price = (normal * normal_price) + (discount * discount_price)

            # Generate booking ID
            try:
                file = open(BOOKING_FILE, 'r')
                lines = file.readlines()
                file.close()
                booking_count = len(lines) - 1
            except FileNotFoundError:
                booking_count = 0

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

            confirm = input("\nConfirm? (Y/N): ").strip().upper()
            if confirm != "Y":
                print("Cancelled.")
                return

            # Save booking
            try:
                file = open(BOOKING_FILE, 'a')
                file.write(
                    f"{booking_id}, {movie_id}, {showtime_id}, {customer_id}, {seats}, {tickets}, {total_price:.2f}, {auditorium_id}\n")
                file.close()

                print("\n✓ Booking successful!")
                print(f"Booking ID: {booking_id}")
                return

            except Exception as e:
                print(f"\nERROR: Could not save booking!")
                return

        except Exception as e:
            print(f"\nERROR: Something went wrong!")
            retry = input("Try again? (Y/N): ").strip().upper()
            if retry != "Y":
                return


def cancel_booking():
    """Cancel a booking"""
    print("\n========== CANCEL BOOKING ==========")

    view_bookings()

    while True:
        try:
            booking_id = input("\nBooking ID to cancel (or 0 to exit): ").strip()

            if booking_id == "0":
                return

            if not booking_id:
                print("ERROR: Enter booking ID!")
                continue

            # Read all bookings
            try:
                file = open(BOOKING_FILE, 'r')
                lines = file.readlines()
                file.close()
            except FileNotFoundError:
                print("ERROR: No bookings file found!")
                return

            found = False
            new_lines = [lines[0]]

            for i in range(1, len(lines)):
                if lines[i].strip() == "":
                    continue

                parts = lines[i].split(',')
                if parts[0].strip() == booking_id:
                    found = True
                    print(f"\nFound: {lines[i].strip()}")

                    confirm = input("Cancel? (Y/N): ").strip().upper()
                    if confirm == "Y":
                        print(f"\n✓ Booking {booking_id} cancelled!")
                    else:
                        new_lines.append(lines[i])
                        print("Not cancelled.")
                else:
                    new_lines.append(lines[i])

            if not found:
                print(f"ERROR: Booking {booking_id} not found!")
                retry = input("Try again? (Y/N): ").strip().upper()
                if retry != "Y":
                    return
                continue

            # Save updated bookings
            try:
                file = open(BOOKING_FILE, 'w')
                file.writelines(new_lines)
                file.close()
                return
            except Exception as e:
                print("ERROR: Could not save changes!")
                return

        except Exception as e:
            print("ERROR: Something went wrong!")
            retry = input("Try again? (Y/N): ").strip().upper()
            if retry != "Y":
                return


def main_ticketing_clerk():
    """Main program"""
    print("=" * 50)
    print("   CINEMA TICKETING SYSTEM")
    print("=" * 50)

    while True:
        try:
            print("\n========== MENU ==========")
            print("1. View Movies")
            print("2. View Auditoriums")
            print("3. View Showtimes")
            print("4. Book Ticket")
            print("5. View Bookings")
            print("6. Cancel Booking")
            print("7. Exit")
            print("=" * 27)

            choice = input("\nChoice (1-7): ").strip()

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
                break
            else:
                print("ERROR: Choose 1-7")

            input("\nPress Enter...")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print("\nERROR: Something went wrong!")
            input("Press Enter to continue...")


#------------------------- CINEMA MANAGER --------------------------------------------------
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
        colored_message (str): The error message wrapped with red color and reset codes.
    """
    colored_message = RED + message + RESET
    return colored_message


def color_completion_message(message):
    """
    Wraps a string with ANSI escape codes to display it in green.

    Args:
        message (str): The completion message to be colorized.

    Returns:
        colored_message (str): The completion message wrapped with green color and reset codes.
    """
    colored_message = GREEN + message + RESET
    return colored_message


def color_confirmation_message(message):
    """
    Wraps a string with ANSI escape codes to display it in blue.

    Args:
        message (str): The confirmation message to be colorized.

    Returns:
        colored_message (str): The confirmation message wrapped with blue color and reset codes.
    """
    colored_message = BLUE + message + RESET
    return colored_message


def clear_terminal():
    """Clears the terminal screen.

    Returns:
        None
    """
    if os.name == "nt":
        _ = os.system("cls")
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
        list: A list of the fields that makes up the line.
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
            list: A list containing the auditorium ID of the selected auditorium, the end time, the normal price based on the auditorium, and the discounted price based on the normal price and the existing discount ID if the movie is eligible for discount.
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




#------------------------- TECHNICIAN  --------------------------------------------------
def load_movies(filename=r"Cinema/Database/movie_listings.txt"):
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

        formatted = m["movie_data"].replace(",", "\n")

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


# ================== ISSUES ==================
ISSUES_FILE = r"Cinema/Database/technician_issues.txt"

# ensure path & file exist
import os
os.makedirs(os.path.dirname(ISSUES_FILE), exist_ok=True)
if not os.path.exists(ISSUES_FILE):
    with open(ISSUES_FILE, "w", encoding="utf-8") as f:
        f.write("auditorium_id, equipment, status, estimated_repair_date, estimated_repaired_date\n")

AUDITORIUMS = [f"AUD0{i}" for i in range(1, 9)]
EQUIPMENT_LIST = ["Projector", "Audio", "Air Conditioning"]


def load_issues(filename=ISSUES_FILE):
    issues = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip() or line.startswith("auditorium_id"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 5:
                    continue
                aud, equip, status, est_repair, est_done = parts
                issues[(aud, equip)] = {
                    "status": status,
                    "est_repair": est_repair,
                    "est_done": est_done
                }
    except FileNotFoundError:
        pass
    return issues



def save_issues(issues, filename=ISSUES_FILE):
    print("Saving")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("auditorium_id, equipment, status, estimated_repair_date, estimated_repaired_date\n")
        for x, data in sorted(issues.items()):
            f.write(f"{x[0]}, {x[1]}, {data['status']}, {data['est_repair']}, {data['est_done']}\n")


def report_issue():
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

    # -------- input section --------
    print("\n🛠 Enter estimated repair start date (DD-MM-YYYY):")
    date = input("   Date: ").strip()
    print("🕐 Enter start time (e.g. 08:00AM or 08:00 AM):")
    time = input("   Time: ").strip()
    print("⏱ Enter estimated time needed (e.g. 2h 30m):")
    duration = input("   Duration: ").strip()

    # -------- validation --------
    if "-" not in date or len(date.split("-")) != 3:
        print("⚠️ Invalid date format (use DD-MM-YYYY).")
        return
    if not any(x in time.upper() for x in ["AM", "PM"]):
        print("⚠️ Invalid time format (must include AM/PM).")
        return

# -------- calculate end time --------
    try:
        from datetime import datetime, timedelta

        # --- Validate and parse date ---
        # Accepts both 10-1-2006 and 10-01-2006
        try:
            date_obj = datetime.strptime(date.strip(), "%d-%m-%Y")
        except ValueError:
            print("⚠️ Invalid date format or non-existent date (e.g. 30-2-2000).")
            return

        # --- Validate and parse time ---
        # Normalize time input (handle 8:00am / 08:00AM / 8:00 pm)
        time = time.strip().upper().replace(" ", "")
        if not any(x in time for x in ["AM", "PM"]):
            print("⚠️ Please include AM or PM in time (e.g. 8:00AM).")
            return

        # Try to parse using 12-hour format
        try:
            time_obj = datetime.strptime(time, "%I:%M%p")
        except ValueError:
            print("⚠️ Invalid time format. Use something like 8:00AM or 08:00PM.")
            return

        # Combine date and time into one datetime object
        start_dt = datetime.combine(date_obj.date(), time_obj.time())

        # --- Parse duration ---
        duration = duration.lower().strip()
        hrs = 0
        mins = 0
        if "h" in duration:
            hrs_part = duration.split("h")[0].strip()
            hrs = int(hrs_part) if hrs_part.isdigit() else 0
        if "m" in duration:
            after_h = duration.split("h")[-1]
            mins_part = after_h.replace("m", "").strip()
            mins = int(mins_part) if mins_part.isdigit() else 0

        # --- Calculate end time ---
        end_dt = start_dt + timedelta(hours=hrs, minutes=mins)

        # Display in 12-hour format with AM/PM
        end_time = end_dt.strftime("%I:%M%p").lstrip("0")
        print(f"✅ End time: {end_time}")

    except Exception as e:
        print("⚠️ Invalid time, date, or duration format.")
        return

    # -------- save data --------
    issues = load_issues()
    issues[(auditorium, equipment)] = {
        "status": "Under Maintenance",
        "est_repair": f"{date} {time}",
        "est_done": f"{date} {end_time}"
    }
    save_issues(issues)

    print(f"✅ Issue reported successfully: {auditorium} - {equipment}")
    print(f"   Estimated completion: {date} {end_time}")

def confirm_readiness():
    print("\nSelect Auditorium to view status:")
    for i, a in enumerate(AUDITORIUMS, 1):
        print(f"{i}. {a}")
    choice = input("Enter choice (1-8): ")
    try:
        auditorium = AUDITORIUMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    issues = load_issues()
    print(f"\n📋 Current equipment status for {auditorium}:")
    found_any = False
    for equip in EQUIPMENT_LIST:
        data = issues.get((auditorium, equip))
        if data:
            print(f"   {equip}: {data['status']}")
            if data['status'] == "Under Maintenance":
                print(f"      Estimated Repair Start: {data['est_repair']}")
                print(f"      Estimated Repair Completion: {data['est_done']}")
            found_any = True
        else:
            print(f"   {equip}: READY")

    if not found_any:
        print("   (No recorded statuses yet for this auditorium.)")


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
        if issues[key]["status"] == "Under Maintenance":
            issues[key]["status"] = "READY"
            save_issues(issues)
            print(f"✅ Issue resolved: {auditorium} - {equipment}")
        elif issues[key]["status"] == "READY":
            print(f"ℹ️ Equipment already marked READY: {auditorium} - {equipment}")
        else:
            issues[key]["status"] = "READY"
            save_issues(issues)
            print(f"✅ Status updated to READY for {auditorium} - {equipment}")
    else:
        print("⚠️ No record found for that auditorium/equipment. Nothing to resolve.")


def reset_all_equipment():
    with open(ISSUES_FILE, "w", encoding="utf-8") as f:
        f.write("auditorium_id, equipment, status, estimated_repair_date, estimated_repaired_date\n")
        for i in range(1, 9):
            for e in EQUIPMENT_LIST:
                f.write(f"AUD{i}, {e}, READY, , \n")
    print("🔄 All equipment has been reset to READY.")


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
            movies = load_movies()
            display_movies(movies)
        elif choice == "2":
            report_issue()
        elif choice == "3":
            confirm_readiness()
        elif choice == "4":
            mark_resolved()
        elif choice == "5":
            reset_all_equipment()
        elif choice == "6":
            print("👋 Goodbye!")
            main()
            break
        else:
            print("!! Invalid Choice, Please Use 1 2 3 ... Format !!")





#------------------------- CUSTOMER --------------------------------------------------
try:
    SCRIPT_DIR = os.path.dirname(__file__)
except NameError:
    SCRIPT_DIR = os.getcwd()

if os.getcwd() != SCRIPT_DIR:
    os.chdir(SCRIPT_DIR)

BASE = os.path.join("Database")
os.makedirs(BASE, exist_ok=True)

MOVIE_FILE       = os.path.join(BASE, "movie_listings.txt")
SHOW_FILE        = os.path.join(BASE, "movie_showtimes.txt")
CUSTOMER_FILE    = os.path.join(BASE, "customer.txt")
BOOKING_FILE     = os.path.join(BASE, "movie_bookings.txt")
AUD_SITTING_FILE = os.path.join(BASE, "auditorium_sitting.txt")
DISCOUNT_FILE    = os.path.join(BASE, "discount_policies.txt")


def safe_input(msg):
    text = input(msg)
    return text.strip()

def read_int(msg):
    while True:
        t = safe_input(msg)
        if t.isdigit():
            return int(t)
        print("Please enter digits only.")

EXIT_HINT = " (Enter 0 to return to menu)"

def read_int_or_menu(msg):
    while True:
        t = safe_input(msg + EXIT_HINT + ": ")
        if t == "0":
            return None
        if t.isdigit():
            return int(t)
        print("Please enter digits only.")

def input_or_menu(msg):
    t = safe_input(msg + EXIT_HINT + ": ")
    if t == "0":
        return None
    return t.strip()

def is_valid_msisdn_with_60(text):
    return text.isdigit() and text.startswith("60") and len(text) > 2


def split_csv_line(line):
    parts = line.split(",")
    out = []
    for p in parts:
        out.append(p.strip().strip('"'))
    return out

def join_csv(items):
    texts = []
    for it in items:
        texts.append(str(it))
    return ", ".join(texts)


def read_all_lines(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        raw = f.readlines()
        f.close()
    except FileNotFoundError:
        print(f"[Warning] Missing file: {filename}. (Returning empty list.)")
        return []
    except PermissionError:
        print(f"[Error] No permission to read: {filename}.")
        return []
    except OSError as e:
        print(f"[Error] Could not read {filename}: {e}")
        return []

    out = []
    for ln in raw:
        out.append(ln.rstrip("\n"))
    return out

def append_line(filename, one_line):
    try:
        f = open(filename, "a", encoding="utf-8")
        f.write(one_line + "\n")
        f.close()
    except PermissionError:
        print(f"[Error] No permission to write: {filename}. Data not saved.")
    except OSError as e:
        print(f"[Error] Could not append to {filename}: {e}. Data not saved.")

def write_all_lines(filename, lines):
    try:
        f = open(filename, "w", encoding="utf-8")
        for ln in lines:
            f.write(ln + "\n")
        f.close()
    except PermissionError:
        print(f"[Error] No permission to write: {filename}. Changes not saved.")
    except OSError as e:
        print(f"[Error] Could not write {filename}: {e}. Changes not saved.")


def pad4(n):
    s = str(n)
    while len(s) < 4:
        s = "0" + s
    return s

def next_id_by_count(filename, prefix):
    lines = read_all_lines(filename)
    if len(lines) == 0:
        count = 0
    else:
        count = len(lines) - 1
    next_number = count + 1
    return prefix + pad4(next_number)


def load_movies():
    lines = read_all_lines(MOVIE_FILE)
    movies = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        parts = split_csv_line(line)
        if len(parts) >= 2:
            movies.append({"movie_id": parts[0], "movie_name": parts[1]})
    return movies

def load_showtimes():
    lines = read_all_lines(SHOW_FILE)
    shows = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        parts = split_csv_line(line)
        if len(parts) >= 9:
            shows.append({
                "showtime_id":      parts[0],
                "movie_id":         parts[1],
                "auditorium":       parts[2],
                "date":             parts[3],
                "start_time":       parts[4],
                "end_time":         parts[5],
                "normal_price":     parts[6],
                "discounted_price": parts[7],
                "discount_id":      parts[8],
            })
    return shows

def load_discounts():
    lines = read_all_lines(DISCOUNT_FILE)
    discs = {}
    for i, line in enumerate(lines):
        if i == 0:
            continue
        parts = split_csv_line(line)
        if len(parts) >= 2:
            disc_id = parts[0]
            name    = parts[1]
            policy  = ", ".join(parts[2:]).strip()
            discs[disc_id] = {"name": name, "policy": policy}
    return discs


def load_auditorium_seats():
    seats_by_aud = {}
    lines = read_all_lines(AUD_SITTING_FILE)
    current_aud = None
    for line in lines:
        txt = line.strip()
        if txt == "":
            continue
        if txt.startswith("AUD"):
            current_aud = txt
            if current_aud not in seats_by_aud:
                seats_by_aud[current_aud] = []
            continue
        pieces = txt.split()
        for token in pieces:
            if ":" in token:
                seat_id = token.split(":")[0]
                seat_id = seat_id.strip()
                if current_aud is not None and seat_id != "":
                    seats_by_aud[current_aud].append(seat_id)
    return seats_by_aud

def pad2(n):
    s = str(n)
    if len(s) < 2:
        s = "0" + s
    return s

def seat_row_col(seat_id):
    letters = ""
    digits = ""
    for ch in seat_id:
        if ch.isalpha():
            letters += ch
        else:
            digits += ch
    col = 0
    if digits != "":
        col = int(digits)
    return letters, col

def print_seat_map(aud_id, taken_seats, seats_by_aud):
    if aud_id not in seats_by_aud:
        print("No seating layout found for", aud_id)
        return

    valid = seats_by_aud[aud_id]
    row_to_cols = {}
    max_col = 0

    for seat in valid:
        r, c = seat_row_col(seat)
        if r not in row_to_cols:
            row_to_cols[r] = []
        if c not in row_to_cols[r]:
            row_to_cols[r].append(c)
        if c > max_col:
            max_col = c

    rows = []
    for r in row_to_cols:
        rows.append(r)
    rows.sort()
    for r in rows:
        row_to_cols[r].sort()

    print("Legend: [ ] = available   [X] = taken")
    header = "    "
    for c in range(1, max_col + 1):
        header = header + " " + pad2(c) + " "
    print(header)

    for r in rows:
        line = r + " :"
        existing = row_to_cols[r]
        for c in range(1, max_col + 1):
            seat_code = r + pad2(c)
            if c in existing:
                if seat_code in taken_seats:
                    line = line + " [X]"
                else:
                    line = line + " [ ]"
            else:
                line = line + "    "
        print(line)
    print()


def find_row_by_id(filename, id_index, target_id):
    lines = read_all_lines(filename)
    for i in range(1, len(lines)):
        parts = split_csv_line(lines[i])
        if len(parts) > id_index and parts[id_index] == target_id:
            return parts
    return None

def get_auditorium_for_showtime(showtime_id):
    row = find_row_by_id(SHOW_FILE, 0, showtime_id)
    if row is None or len(row) < 3:
        return None
    return row[2]


def ask_existing_showtime_id_for_movie(movie_id):
    shows = load_showtimes()
    any_printed = False

    for s in shows:
        if s["movie_id"] == movie_id:
            if not any_printed:
                print("\n=== Showtimes for", movie_id, "===\n")
            any_printed = True
            print(" " + s["showtime_id"], "|", s["date"],
                  s["start_time"] + "-" + s["end_time"], "| Aud:", s["auditorium"])
            print()

    if not any_printed:
        print("No showtimes for that movie.\n")

    while True:
        sid = input_or_menu("Enter Showtime ID (e.g. ST0001)")
        if sid is None: return None
        row = find_row_by_id(SHOW_FILE, 0, sid)
        if row is not None and len(row) > 1 and row[1] == movie_id:
            print()
            return sid
        print("Invalid showtime for that movie. Try again.\n")


def ask_existing_customer_login():
    while True:
        cid = input_or_menu("Customer ID (e.g. C0001)")
        if cid is None: return None
        pwd = input_or_menu("Password")
        if pwd is None: return None

        lines = read_all_lines(CUSTOMER_FILE)
        for i in range(1, len(lines)):
            parts = split_csv_line(lines[i])
            if len(parts) >= 5 and parts[0] == cid and parts[4] == pwd:
                return cid
        print("ID or password incorrect. Try again.")

def ask_existing_movie_id():
    movies = load_movies()
    if len(movies) == 0:
        print("No movies found in", MOVIE_FILE)
    else:
        print("=== Movies ===")
        for m in movies:
            print(m["movie_id"] + " - " + m["movie_name"])

    while True:
        mid = input_or_menu("Enter Movie ID (e.g. M001)")
        if mid is None: return None
        if find_row_by_id(MOVIE_FILE, 0, mid):
            return mid
        print("Invalid Movie ID. Try again.")


def register_customer():
    cust_id = next_id_by_count(CUSTOMER_FILE, "C")

    name = input_or_menu("Name")
    if name is None: return

    while True:
        phone = input_or_menu("Phone (must start with 60)")
        if phone is None: return
        if is_valid_msisdn_with_60(phone): break
        print("Phone must start with '60' and contain digits only.")

    email = input_or_menu("Email")
    if email is None: return
    while "@" not in email:
        print("Email must contain '@'.")
        email = input_or_menu("Email")
        if email is None: return

    while True:
        pwd1 = input_or_menu("Create password")
        if pwd1 is None: return
        pwd2 = input_or_menu("Confirm password")
        if pwd2 is None: return
        if pwd1 != "" and pwd1 == pwd2: break
        print("Passwords do not match. Try again.")

    new_row = join_csv([cust_id, name, phone, email, pwd1])
    append_line(CUSTOMER_FILE, new_row)
    print("Registered! Your customer ID is:", cust_id)


def update_my_details():
    lines = read_all_lines(CUSTOMER_FILE)
    if len(lines) <= 1:
        print("No customers yet.")
        return

    cid = ask_existing_customer_login()

    idx = -1
    cur = None
    for i in range(1, len(lines)):
        parts = split_csv_line(lines[i])
        if parts[0] == cid:
            idx = i
            cur = parts
            break
    if idx == -1:
        print("Unexpected: customer not found.")
        return

    print("Leave blank to keep current value in [brackets].")
    new_name  = safe_input("Name  [" + cur[1] + "]: ") or cur[1]
    new_phone = safe_input("Phone [" + cur[2] + "]: ") or cur[2]
    new_email = safe_input("Email [" + cur[3] + "]: ") or cur[3]

    if not new_phone.isdigit():
        print("Phone must be digits only. Keeping old.")
        new_phone = cur[2]
    if "@" not in new_email:
        print("Email must contain '@'. Keeping old.")
        new_email = cur[3]

    change = safe_input("Change password? (Y/N): ").strip().upper()
    if change == "Y":
        while True:
            p1 = safe_input("New password: ")
            p2 = safe_input("Confirm new password: ")
            if p1 != "" and p1 == p2:
                new_pass = p1
                break
            print("Passwords do not match or are empty. Try again.")
    else:
        new_pass = cur[4]

    lines[idx] = join_csv([cid, new_name, new_phone, new_email, new_pass])
    write_all_lines(CUSTOMER_FILE, lines)
    print("Details updated.")


def view_all_movie_showtimes():
    movies = load_movies()
    shows  = load_showtimes()
    discs  = load_discounts()

    if len(movies) == 0 or len(shows) == 0:
        print("No movies or showtimes to display.")
        return

    name_of = {}
    for m in movies:
        name_of[m["movie_id"]] = m["movie_name"]

    print("=== All Movie Showtimes ===")
    n = 1
    for s in shows:
        title = name_of.get(s["movie_id"], "(title not found)")
        print(str(n) + ". Movie:", title)
        print("   date:", s["date"])
        print("   time:", s["start_time"])
        print("   venue:", s["auditorium"])

        if s["normal_price"] != "":
            print("   normal price: RM", s["normal_price"])
        if s["discounted_price"] != "" and s["discount_id"] != "":
            did = s["discount_id"]
            rule = discs.get(did, None)
            print("   discounted price: RM", s["discounted_price"])
            if rule is not None:
                print("   discount:", did, "-", rule["name"])
                print("   who qualifies: 10% off for students, kids, senior citizens, and OKU.")
        print()
        n = n + 1


def seats_taken_for_show(showtime_id):
    lines = read_all_lines(BOOKING_FILE)
    taken = []
    for i in range(1, len(lines)):
        parts = split_csv_line(lines[i])
        if len(parts) >= 4 and parts[1] == showtime_id:
            seats_text = parts[3]
            pieces = seats_text.split("|")
            for s in pieces:
                seat = s.strip()
                if seat != "":
                    taken.append(seat)
    return taken


def book_tickets():
    cid = ask_existing_customer_login()
    if cid is None:
        return

    mid = ask_existing_movie_id()
    if mid is None:
        return

    sid = ask_existing_showtime_id_for_movie(mid)
    if sid is None:
        return

    aud_id = get_auditorium_for_showtime(sid)
    seats_map = load_auditorium_seats()
    taken = seats_taken_for_show(sid)
    valid_seats = seats_map.get(aud_id, [])

    print("\n=== Seat Map ===\n")
    print_seat_map(aud_id, taken, seats_map)
    print("This show is in", aud_id + ". Seats will be checked against that auditorium.\n")

    while True:
        raw = input_or_menu("Seats (e.g. A01|A02)")
        if raw is None:
            return

        pieces = raw.split("|")
        chosen = [p.strip() for p in pieces if p.strip() != ""]
        if len(chosen) == 0:
            print("Enter at least one seat.\n")
            continue

        bad = [s for s in chosen if s not in valid_seats]
        if len(bad) > 0:
            print("These seats are not valid for", aud_id + ":", ", ".join(bad))
            print("Please choose seats that exist in", aud_id + ".\n")
            continue

        conflict = False
        for s in chosen:
            if s in taken:
                print("Seat", s, "already taken. Pick others.")
                conflict = True
        if conflict:
            print("")
            continue

        break

    shows = load_showtimes()
    discs = load_discounts()
    the_show = next((s for s in shows if s["showtime_id"] == sid), None)

    print("")
    if the_show:
        if the_show["normal_price"]:
            print("Normal price per ticket: RM", the_show["normal_price"])
        if the_show["discounted_price"] and the_show["discount_id"]:
            did = the_show["discount_id"]
            print("Discounted price per ticket: RM", the_show["discounted_price"])
            if did in discs:
                print("Who qualifies: 10% off for students, kids, senior citizens, and OKU.")
        else:
            print("No discount set for this showtime.")
    print("")

    normal = read_int_or_menu("Normal tickets")
    if normal is None:
        return
    disc = 0
    if the_show and the_show["discounted_price"] and the_show["discount_id"]:
        disc = read_int("Discounted tickets (if you qualify; enter 0 if none): ")

    bid = next_id_by_count(BOOKING_FILE, "B")
    tickets_text = str(normal) + "|" + str(disc)
    new_row = join_csv([bid, sid, cid, "|".join(chosen), tickets_text])
    append_line(BOOKING_FILE, new_row)

    print("\nBooked! Your Booking ID is:", bid, "\n")


def cancel_ticket():
    lines = read_all_lines(BOOKING_FILE)
    cid = ask_existing_customer_login()
    if cid is None:
        return

    my_ids = []
    print("=== Your Bookings ===")
    for i in range(1, len(lines)):
        parts = split_csv_line(lines[i])
        if len(parts) >= 3 and parts[2] == cid:
            my_ids.append(parts[0])
            print("Booking:", parts[0], "| Show:", parts[1], "| Seats:", parts[3])

    if len(my_ids) == 0:
        print("You have no bookings.")
        return

    while True:
        bid = input_or_menu("Enter Booking ID to cancel")
        if bid is None:
            return
        if bid in my_ids:
            break
        print("That booking doesn't belong to you. Try again.")

    new_lines = [lines[0]]
    for i in range(1, len(lines)):
        parts = split_csv_line(lines[i])
        if parts[0] != bid:
            new_lines.append(lines[i])
    write_all_lines(BOOKING_FILE, new_lines)

    print("Booking", bid, "cancelled.")


def view_booking_history():
    lines = read_all_lines(BOOKING_FILE)
    cid = ask_existing_customer_login()
    if cid is None:
        return
    any_printed = False
    print("=== Booking History for", cid, "===")

    for i in range(1, len(lines)):
        parts = split_csv_line(lines[i])
        if len(parts) >= 3 and parts[2] == cid:
            any_printed = True
            print("Booking ID:", parts[0])
            print(" Show ID:", parts[1])
            print(" Seats:", parts[3])
            print(" Tickets (normal|discount):", parts[4])
            print("-" * 30)
    if not any_printed:
        print("No bookings found.")


def main_customer():
    while True:
        print("\n=== CUSTOMER MENU ===")
        print("[1] Register / Create account")
        print("[2] Update my account details")
        print("[3] View all movie showtimes (Movie/Date/Time/Venue)")
        print("[4] Book tickets")
        print("[5] Cancel my ticket")
        print("[6] View my booking history")
        print("[0] Exit")
        choice = read_int("Enter your choice: ")

        if choice == 1:   register_customer()
        elif choice == 2: update_my_details()
        elif choice == 3: view_all_movie_showtimes()
        elif choice == 4: book_tickets()
        elif choice == 5: cancel_ticket()
        elif choice == 6: view_booking_history()
        elif choice == 0:
            print("Goodbye!")
            main()
            break
        else:
            print("Invalid choice. Try again.")





#------------------------- MAIN MENU --------------------------------------------------
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

    
    