

# FILE PATHS (plain strings)
BASE =  "Cinema/Database"
MOVIE_FILE    = BASE + r"/movie_listings.txt"      # where movie rows are stored
SHOW_FILE     = BASE + r"/movie_showtimes.txt"     # where showtime rows are stored
CUSTOMER_FILE = BASE + r"/customers.txt"      # where customer rows are stored
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
            print("Goodbye!")                                            # goodbye text
            break                                                         # leave the loop and end program
        else:
            print("Invalid choice. Try again.")                          # anything else -> error then loop

                                                            # start the program
