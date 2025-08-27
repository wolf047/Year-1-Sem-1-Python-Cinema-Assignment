# Cinema Manager
# - Add, update, or remove movie listings.
# - Create and manage showtime schedules(movie, auditorium, time).
# - Set ticket prices and apply discount policies.
# - View overall booking reports and revenue summaries.

def lint_entries(value):
    if isinstance(value, list):
        value = "|".join(value)
    value = str(value)
    return f'"{value}"' if "," in value or " " in value else value


def add_entries(filename, entry_details):
    with open(filename, "a") as f:
        formatted_entry = []
        for item in entry_details:
            formatted_item = lint_entries(item)
            formatted_entry.append(formatted_item)
        f.write(", ".join(formatted_entry) + "\n")


def update_entries(filename, entry_id, position, entry_details):
    with open(filename, "r") as f:
        entries = f.readlines()
        updated_entries = []
        for entry in entries:
            entry = [i.strip() for i in entry.strip().split(",")]
            if entry[0] == entry_id:
                entry[position] = lint_entries(entry_details)
                updated_entries.append(", ".join(entry) + "\n")
            else:
                updated_entries.append(", ".join(entry) + "\n")
    with open(filename, "w") as f:
        f.writelines(updated_entries)

def remove_entries(filename, entry_id):
    with open(filename, "r") as f:
        entries = f.readlines()
        updated_entries = []
        for entry in entries:
            entry = [i.strip() for i in entry.strip().split(",")]
            if entry[0] != entry_id:
                updated_entries.append(", ".join(entry) + "\n")
    with open(filename, "w") as f:
        f.writelines(updated_entries)


def id_counter(location, counted):
    filename = f'{location}/{counted}_id_counter.txt'
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            id_no = int(content) if content else 1
    except FileNotFoundError:
        id_no = 1

    with open(filename, "w") as f:
        f.write(str(id_no + 1))

    return id_no


def add_movie_listing():
    movie_id_no = id_counter("Cinema/Database/", "movie")
    movie_id = f'M{movie_id_no:04}'

    movie_name = input("Enter movie name: ")
    release_date = input("Enter release date: ")
    running_time = input("Enter running time: ")
    genre = [genre.strip() for genre in input(
        "Enter genres (enter comma-delimited list): ").split(",")]

    # ----------CLASSIFICATION -----------
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
            print("Invalid option")

# ---------- CLASSIFICATION END -------------

    spoken_language = input("Enter spoken language (full form): ")
    subtitle_language = [language.strip() for language in input(
        "Enter subtitle languages (full form, enter comma-delimited list): ").split(",")]
    director = input("Enter director name: ")
    casts = [cast.strip() for cast in input(
        "Enter cast names (enter comma-delimited list): ").split(",")]
    description = input("Enter description: ")

    listing = [movie_id, movie_name, release_date, running_time, genre,
               classification, spoken_language, subtitle_language, director, casts, description]

    add_entries("Cinema/Database/movie_listing.txt", listing)
    print(f'Listing for {movie_id} created.')


def update_movie_listing():
    movie_id_edit = input("Enter ID of movie to be edited: ")

    with open("Cinema/Database/movie_listing.txt", "r") as f:
        details = [detail.strip() for detail in f.readline().split(",")]

        for line in f:
            entry = [i.strip() for i in line.split(",")]

            if entry[0] == movie_id_edit:
                for index, field in enumerate(details[1: 11], start=1):
                    print(f'[{index}] {field}')

                detail_selection = int(
                    input("Select detail (enter number 1-10): "))
                valid_selection = True

                match detail_selection:
                    case 1:
                        update_details = input("Enter updated movie name: ")
                    case 2:
                        update_details = input("Enter updated release date: ")
                    case 3:
                        update_details = input("Enter updated running time: ")
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
                                print("Invalid option")
                        update_details = classification
                    case 6:
                        update_details = input(
                            "Enter updated spoken language (full form): ")
                    case 7:
                        update_details = [language.strip() for language in input(
                            "Enter updated subtitle languages (full form, enter comma-delimited list): ").split(",")]
                    case 8:
                        update_details = input("Enter updated director name: ")
                    case 9:
                        update_details = [cast.strip() for cast in input(
                            "Enter updated cast names (enter comma-delimited list): ").split(",")]
                    case 10:
                        update_details = input("Enter updated description: ")
                    case _:
                        print("Invalid option")
                        valid_selection = False
                if valid_selection:
                    update_entries("Cinema/Database/movie_listing.txt",
                                   movie_id_edit, detail_selection, update_details)
                    print(f'Listing for {movie_id_edit} updated.')


def remove_movie_listing():
    movie_id_remove = input("Enter ID of movie to be removed: ")
    remove_entries("Cinema/Database/movie_listing.txt", movie_id_remove)
    print(f'Listing for {movie_id_remove} removed.')


def create_showtime():
    showtime_id_no = id_counter("Cinema/Database/", "showtime")
    showtime_id = f'M{showtime_id_no:05}'

    movie_id = input("Enter movie ID: ")
    auditorium_id = input("Enter auditorium ID: ")
    date = input("Enter date: ")
    start_time = input("Enter start time: ")
    end_time = input("Enter end time: ")

    showtime = [showtime_id, movie_id,
                auditorium_id, date, start_time, end_time]

    add_entries("Cinema/Database/movie_showtimes.txt", showtime)
    print(f'Showtime {showtime_id} for {movie_id} created.')


def update_showtime():
    showtime_id_edit = input("Enter ID of showtime to be edited: ")

    with open("Cinema/Database/movie_showtime.txt", "r") as f:
        details = [detail.strip() for detail in f.readline().split(",")]

        for line in f:
            entry = [i.strip() for i in line.split(",")]

            if entry[0] == showtime_id_edit:
                for index, field in enumerate(details[1: 6], start=1):
                    print(f'[{index}] {field}')

                detail_selection = int(
                    input("Select detail (enter number 1-5): "))
                valid_selection = True

                match detail_selection:
                    case 1:
                        update_details = input("Enter updated movie ID: ")
                    case 2:
                        update_details = input("Enter updated auditorium ID: ")
                    case 3:
                        update_details = input("Enter updated date: ")
                    case 4:
                        update_details = input("Enter updated start time: ")
                    case 5:
                        update_details = input("Enter updated end time: ")
                    case _:
                        print("Invalid option")
                        valid_selection = False
                if valid_selection:
                    update_entries("Cinema/Database/movie_showtimes.txt",
                                   showtime_id_edit, detail_selection, update_details)
                    print(f'Listing for {showtime_id_edit} updated.')


def remove_showtime():
    showtime_id_remove = input("Enter ID of showtime to be removed: ")
    remove_entries("Cinema/Database/movie_showtimes.txt", showtime_id_remove)
    print(f'Listing for {showtime_id_remove} removed.')


def set_ticket_price():
    def set_adult_price():
        pass

    def set_discounted_price():
        pass


def view_booking_reports():
    pass


def view_revenue_summary():
    pass
