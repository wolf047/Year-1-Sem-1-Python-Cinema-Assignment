def main_cinema_manager():
    print("=== Cinema Manager Main Page ===\n")
    actions = ["Add movie listing", "Update movie listing", "Remove movie listing", "Add showtime", "Update showtime", "Remove showtime",
               "Add discount", "Update discount", "Remove discount", "View booking report", "View revenue summary"]

    # ADD IF GOT MOVIE LISTING, SHOWTIME, DISCOUNT
    for index, action in enumerate(actions, start=1):
        print(f'[{index}] {action}')

    action_choice = int(input("Select action (enter number 1-11): "))

    match action_choice:
        case 1:
            print(actions[0].upper())
            add_movie_listing()
        case 2:
            print(actions[1].upper())
            update_movie_listing()
        case 3:
            print(actions[2].upper())
            remove_movie_listing()
        case 4:
            print(actions[3].upper())
            add_showtime()
        case 5:
            print(actions[4].upper())
            update_showtime()
        case 6:
            print(actions[5].upper())
            remove_showtime()
        case 7:
            print(actions[6].upper())
            add_discount()
        case 8:
            print(actions[7].upper())
            update_discount()
        case 9:
            print(actions[8].upper())
            remove_discount()
        case 10:
            print(actions[9].upper())
            view_booking_reports()
        case 11:
            print(actions[10].upper())
            view_revenue_summary()


# One-time usage: to generate seat IDs and their respective details
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
#                         seat = [seat_id, auditorium_id, f'{i:02}', f'{j:02}']
#                         g.write(", ".join(seat) + "\n")


def clean_yes_no(prompt):
    while True:
        value = input(prompt).upper().strip()
        if value in ("Y", "N"):
            return value
        print("Invalid input: please enter 'Y' or 'N' only.")


def clean_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())
            return value
        except:
            print("Invalid input: please enter integers only.")

def clean_float(prompt):
    while True:
        try:
            value = round(float(input(prompt).strip()), 2)
            return value
        except:
            print("Invalid input: please enter integers only.")


def lint_entries(value):
    if isinstance(value, list):
        value = "|".join(value)
    value = str(value)
    return f'"{value}"' if "," in value or " " in value else value


def add_entry(filename, entry_details):
    with open(filename, "r") as f:
        next(f)
        second_line = f.readline()
        single_line = second_line == ""
    with open(filename, "a") as f:
        if single_line:
            f.write("\n")
        formatted_entry = []
        for item in entry_details:
            formatted_item = lint_entries(item)
            formatted_entry.append(formatted_item)
        f.write(", ".join(formatted_entry) + "\n")


def update_entry(filename, entry_id, position, entry_detail):
    with open(filename, "r") as f:
        entries = f.readlines()
        updated_entries = []
        for entry in entries:
            entry = [i.strip() for i in entry.strip().split(",")]
            if entry[0] == entry_id:
                entry[position] = lint_entries(entry_detail)
                updated_entries.append(", ".join(entry) + "\n")
            else:
                updated_entries.append(", ".join(entry) + "\n")
    with open(filename, "w") as f:
        f.writelines(updated_entries)


def remove_entry(filename, entry_id):
    with open(filename, "r") as f:
        entries = f.readlines()
        updated_entries = []
        for entry in entries:
            entry = [i.strip() for i in entry.strip().split(",")]
            if entry[0] != entry_id:
                updated_entries.append(", ".join(entry) + "\n")
    with open(filename, "w") as f:
        f.writelines(updated_entries)


def lookup_entry(filename, id_index, target_id, header=0):
    with open(filename, "r") as f:
        if header:
            details = [detail.strip() for detail in f.readline().split(",")]
        for line in f:
            entry = [i.strip() for i in line.split(",")]
            if entry[id_index] == target_id:
                if header:
                    return details
                return entry
    return None


def id_counter(location, counted):
    filename = f'{location}/COUNTER_{counted}_id.txt'
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            id_no = int(content) if content else 1
    except FileNotFoundError:
        id_no = 1

    with open(filename, "w") as f:
        f.write(str(id_no + 1))

    return id_no


def add_movie_listing():  #DONE
    movie_id_no = id_counter("Cinema/Database/", "movie")
    movie_id = f'M{movie_id_no:04}'
    movie_name = input("Enter movie name: ")
    release_date = input("Enter release date: ").strip()
    running_time = clean_int("Enter running time: ")
    genre = [genre.strip() for genre in input(
        "Enter genres (enter comma-delimited list): ").split(",")]

    classification_options = ["U", "P12", "13", "16", "18+", "18SG", "18SX"]
    for index, field in enumerate(classification_options, start=1):
        print(f'[{index}] {field}')
    classification_selection = int(
        input("Select classification (enter number 1-7): "))
    match classification_selection:
        case 1:
            classification = classification_options[0]
        case 2:
            classification = classification_options[1]
        case 3:
            classification = classification_options[2]
        case 4:
            classification = classification_options[3]
        case 5:
            classification = classification_options[4]
        case 6:
            classification = classification_options[5]
        case 7:
            classification = classification_options[6]
        case _:
            print("Invalid option.")
            classification_selection = int(
                input("Select classification (enter number 1-7): "))
    spoken_language = input("Enter spoken language (full form): ")
    subtitle_language = [language.strip() for language in input(
        "Enter subtitle languages (full form, enter comma-delimited list): ").split(",")]
    directors = [director.strip() for director in input(
        "Enter director names (enter comma-delimited list): ").split(",")]
    casts = [cast.strip() for cast in input(
        "Enter cast names (enter comma-delimited list): ").split(",")]
    description = input("Enter description: ")
    eligibility_for_discount = clean_yes_no("Select eligibility for discount (Y/N): ")

    listing = [movie_id, movie_name, release_date, running_time, genre,
               classification, spoken_language, subtitle_language, directors, casts, description, eligibility_for_discount]
    add_entry("Cinema/Database/movie_listing.txt", listing)
    print(f'Listing for {movie_id} created.')


def update_movie_listing(): #DONE
    movie_id_edit = input("Enter ID of movie to be edited: ")

    details = lookup_entry("Cinema/Database/movie_listing.txt", 0, movie_id_edit, 1)

    if not details:
        print("Invalid input: this movie ID does not exist.")
        return

    for index, field in enumerate(details[1: 12], start=1):
        print(f'[{index}] {field}')

    detail_selection = clean_int("Select detail (enter number 1-10): ")

    match detail_selection:
        case 1:
            update_details = input("Enter updated movie name: ")
        case 2:
            update_details = input("Enter updated release date: ")
        case 3:
            update_details = clean_int("Enter updated running time: ")
        case 4:
            update_details = [genre.strip() for genre in input(
                "Enter updated genres (enter comma-delimited list): ").split(",")]
        case 5:
            classification_options = [
                "U", "P12", "13", "16", "18+", "18SG", "18SX"]
            for index, field in enumerate(classification_options, start=1):
                print(f'[{index}] {field}')
            classification_selection = int(
                input("Select updated classification (enter number 1-7): "))
            match classification_selection:
                case 1:
                    classification = classification_options[0]
                case 2:
                    classification = classification_options[1]
                case 3:
                    classification = classification_options[2]
                case 4:
                    classification = classification_options[3]
                case 5:
                    classification = classification_options[4]
                case 6:
                    classification = classification_options[5]
                case 7:
                    classification = classification_options[6]
                case _:
                    print("Invalid option.")
                    classification_selection = int(
                        input("Select updated classification (enter number 1-7): "))
            update_details = classification
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
            update_details = clean_yes_no(
                "Select updated eligibility for discount (Y/N): ")
        case _:
            print("Invalid option")
            detail_selection = clean_int(
                "Select detail (enter number 1-10): ")
            
    update_entry("Cinema/Database/movie_listing.txt",
                movie_id_edit, detail_selection, update_details)
    print(f'Listing for {movie_id_edit} updated.')


def remove_movie_listing():
    movie_id_remove = input("Enter ID of movie to be removed: ")
    movie_listing = lookup_entry(
        "Cinema/Database/movie_listing.txt", 0, movie_id_remove)
    if not movie_listing:
        print("Invalid input: this movie ID does not exist.")
        return
    remove_entry("Cinema/Database/movie_listing.txt", movie_id_remove)
    print(f'Listing for {movie_id_remove} removed.')


def add_showtime():
    showtime_id_no = id_counter("Cinema/Database/", "showtime")
    showtime_id = f'ST{showtime_id_no:05}'
    movie_id = input("Enter movie ID: ")
    auditorium_id = input("Enter auditorium ID: ")
    date = input("Enter date: ")
    start_time = input("Enter start time: ")
    end_time = input("Enter end time: ")

    normal_price = 0
    discounted_price = None

    auditorium_info = lookup_entry("Cinema/Database/auditorium_info.txt", 0, auditorium_id)
    if not auditorium_info:
        print("Invalid input: this auditorium ID does not exist.")
        return
    normal_price = round(float(auditorium_info[5]), 2)

    movie_listing = lookup_entry("Cinema/Database/movie_listing.txt", 0, movie_id)
    if not movie_listing:
        print("Invalid input: this movie ID does not exist.")
        return
    if movie_listing[11] == "Y":
        discount_id = input("Enter discount ID: ")
        discount_policy = lookup_entry("Cinema/Database/discount_policies.txt", 0, discount_id)
        if not discount_policy:
            print("Invalid input: this discount ID does not exist.")
            return
        discounted_price = calculate_discount(discount_id, normal_price)
    
    showtime = [showtime_id, movie_id,
                auditorium_id, date, start_time, end_time,  f'{normal_price:.2f}', f'{discounted_price:.2f}' if discounted_price is not None else ""]
    add_entry("Cinema/Database/movie_showtimes.txt", showtime)
    print(f'Showtime {showtime_id} for {movie_id} created.')


def update_showtime():
    showtime_id_edit = input("Enter ID of showtime to be edited: ")

    details = lookup_entry("Cinema/Database/movie_showtime.txt", 0, showtime_id_edit, 1)
    
    if not details:
        print("Invalid input: this showtime ID does not exist.")
        return
    
    for index, field in enumerate(details[1: 6], start=1):
        print(f'[{index}] {field}')

    detail_selection = clean_int("Select detail (enter number 1-5): ")

    match detail_selection:
        case 1:
            update_details = input("Enter updated movie ID: ")
        case 2:
            update_details = input("Enter updated auditorium ID: ")
            auditorium_info = lookup_entry("Cinema/Database/auditorium_info.txt", 0, update_details)
            if not auditorium_info:
                print("Invalid input: this auditorium ID does not exist.")
                update_details = input("Enter updated auditorium ID: ")
        case 3:
            update_details = input("Enter updated date: ")
        case 4:
            update_details = input("Enter updated start time: ")
        case 5:
            update_details = input("Enter updated end time: ")
        case _:
            print("Invalid option")
            detail_selection = clean_int("Select detail (enter number 1-5): ")
  
    update_entry("Cinema/Database/movie_showtimes.txt",
                    showtime_id_edit, detail_selection, update_details)
    print(f'Listing for {showtime_id_edit} updated.')


def remove_showtime():
    showtime_id_remove = input("Enter ID of showtime to be removed: ")
    movie_showtime = lookup_entry("Cinema/Database/movie_showtime.txt", 0, showtime_id_remove)
    if not movie_showtime:
        print("Invalid input: this showtime ID does not exist.")
        return
    remove_entry("Cinema/Database/movie_showtimes.txt", showtime_id_remove)
    print(f'Listing for {showtime_id_remove} removed.')


def add_discount():
    discount_id_no = id_counter("Cinema/Database/", "discount")
    discount_id = f'D{discount_id_no:02}'
    discount_name = input("Enter discount name: ")
    discount_type_options = ["fixed", "percentage"]
    for index, field in enumerate(discount_type_options[0: 2], start=1):
        print(f'[{index}] {field}')
    discount_type_selection = clean_int("Select discount type (enter number 1-2): ")
    match discount_type_selection:
        case 1:
            discount_type = discount_type_options[0]
            discount_amount = clean_float("Enter discount amount: ")
            discount_rate = None
        case 2:
            discount_type = discount_type_options[1]
            discount_amount = None
            discount_rate = clean_float("Enter discount rate: ")
        case _:
            print("Invalid option.")
            discount_type_selection = clean_int(
                "Select discount type (enter number 1-2): ")
    discount_policies = input("Enter discount policies: ")

    discount = [discount_id, discount_name, discount_type,
                f'{discount_amount:.2f}' if discount_amount is not None else "", f'{discount_rate:.2f}' if discount_rate is not None else "", discount_policies]
    add_entry("Cinema/Database/discount_policies.txt", discount)
    print(f'Discount {discount_id} created.')


def update_discount():
    discount_id_edit = input("Enter ID of discount to be edited: ")

    details = lookup_entry("Cinema/Database/discount_policies.txt", 0, discount_id_edit, 1)
    if not details:
        print("Invalid input: this discount ID does not exist.")
        return
    
    for index, field in enumerate(details[1: 6], start=1):
        print(f'[{index}] {field}')

    detail_selection = clean_int("Select detail (enter number 1-5): ")

    match detail_selection:
        case 1:
            update_details = input("Enter updated discount name: ")
        case 2:
            discount_type_options = ["fixed", "percentage"]
            for index, field in enumerate(discount_type_options[0: 2], start=1):
                print(f'[{index}] {field}')

            discount_type_selection = clean_int("Select updated discount type (enter number 1-2): ")

            match discount_type_selection:
                case 1:
                    update_details = []
                    update_details[0] = discount_type_options[0]
                    update_details[1] = clean_float("Enter updated discount amount: ")
                    update_details[2] = None
                case 2:
                    update_details = []
                    update_details[0] = discount_type_options[1]
                    update_details[1] = None
                    update_details[2] = clean_float(
                        "Enter updated discount rate: ")
                case _:
                    print("Invalid option.")
                    discount_type_selection = clean_int(
                        "Select discount type (enter number 1-2): ")
        case 3:
            update_details = input(
                "Enter updated discount policies: ")
        case _:
            print("Invalid option.")
            detail_selection = clean_int("Select detail (enter number 1-5): ")

    if isinstance(update_details, list):
        update_entry("Cinema/Database/discount_policies.txt",
                        discount_id_edit, 2, update_details[0])
        update_entry("Cinema/Database/discount_policies.txt",
                        discount_id_edit, 3, update_details[1])
        update_entry("Cinema/Database/discount_policies.txt",
                        discount_id_edit, 4, update_details[2])
    else:
        update_entry("Cinema/Database/discount_policies.txt",
                        discount_id_edit, detail_selection, update_details)
    print(f'Listing for {discount_id_edit} updated.')


def remove_discount():
    discount_id_remove = input("Enter ID of discount to be removed: ")
    discount_policy = lookup_entry(
        "Cinema/Database/discount_policies.txt", 0, movie_id_remove)
    if not discount_policy:
        print("Invalid input: this discount ID does not exist.")
        return
    remove_entry("Cinema/Database/discount_policies.txt", discount_id_remove)
    print(f'Listing for {discount_id_remove} removed.')


def calculate_discount(discount_id, normal_price):
    with open("Cinema/Database/discount_policies.txt", "r") as f:
        for line in f:
            entry = [i.strip() for i in line.split(",")]
            discounted_price = None
            if entry[0] == discount_id:
                if entry[2] == "fixed":
                    discounted_price = normal_price - int(entry[3])
                elif entry[2] == "percentage":
                    discounted_price = normal_price * (1 - int(entry[3]))
                return discounted_price


def view_booking_reports():
    specific_movie = input(
        "Do you want to view the report for a specific movie? [Y/N] ") == "Y"

# Validation:
# choice = input("Enter 1 for specific movie, 0 for all movies: ").strip()
# while choice not in ("0", "1"):
#     print("Invalid input. Please enter 0 or 1.")
#     choice = input("Enter 1 for specific movie, 0 for all movies: ").strip()
# specific_movie = choice == "1"

    booking = []
    if specific_movie:
        movie_id_report = input("Enter movie ID: ")
        with open("Cinema/Database/movie_bookings.txt", "r") as f:
            print(f.readline().upper(), end="")
        with open("Cinema/Database/movie_showtimes.txt", "r") as f:
            for showtime_line in f:
                showtime_entry = [i.strip() for i in showtime_line.split(",")]
                with open("Cinema/Database/movie_bookings.txt", "r") as g:
                    for booking_line in g:
                        booking_entry = [i.strip()
                                         for i in booking_line.split(",")]
                        if booking_entry[1] == showtime_entry[0]:
                            if showtime_entry[1] == movie_id_report:
                                booking.append(booking_entry)
    else:
        with open("Cinema/Database/movie_bookings.txt", "r") as f:
            print(f.readline().upper(), end="")
            for line in f:
                entry = [i.strip() for i in line.split(",")]
                booking.append(entry)

    for entry in booking:
        for item in entry[:-1]:
            print(item + ", ", end="")
        print(entry[-1])


def view_revenue_summary():
    normal_total_revenue = 0
    discounted_total_revenue = 0
    with open("Cinema/Database/movie_bookings.txt", "r") as f:
        next(f)
        for line in f:
            booking = [i.strip() for i in line.split(",")]
            showtime_id = booking[1]
            tickets = [int(i.strip()) for i in booking[4].split("|")]

            with open("Cinema/Database/movie_showtimes.txt", "r") as f:
                for line in f:
                    showtime = [i.strip() for i in showtime.split(",")]
                    if showtime[0] == showtime_id:
                        movie_id = showtime[1]

                        with open("Cinema/Database/movie_listing.txt", "r") as f:
                            for line in f:
                                listing = [i.strip()
                                           for i in listing.split(",")]
                                if listing[0] == movie_id:
                                    normal_total_revenue += tickets[0] * \
                                        listing[11]
                                    discounted_total_revenue += tickets[1] * \
                                        listing[12]
                    else:
                        print("Invalid something")  # ERROR MESSAGEEEEEEE

    total_revenue = normal_total_revenue + discounted_total_revenue
    print(
        f'Revenue from normal tickets: {normal_total_revenue}\nRevenue from discounted tickets: {discounted_total_revenue}\nTotal revenue: {total_revenue}')
