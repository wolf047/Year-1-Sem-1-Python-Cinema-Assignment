

# FILE PATHS (plain strings)
BASE =  r"C:\Users\shann\Desktop\Comp-Science(AI)\Int-Python-programming\Assignment\Cinema\Database"
MOVIE_FILE    = BASE + r"/movie_listings.txt"      # where movie rows are stored
SHOW_FILE     = BASE + r"/movie_showtimes.txt"     # where showtime rows are stored
CUSTOMER_FILE = BASE + r"/customer.txt"      # where customer rows are stored
BOOKING_FILE  = BASE + r"/movie_bookings.txt"      # where booking rows are stored
AUD_SITTING_FILE = BASE + r"/auditorium_sitting.txt"  # where auditorium seating layouts are stored
DISCOUNT_FILE = BASE + r"/discount_policies.txt"  # where discount policies are stored


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

def load_showtimes():                                                    # read showtimes + prices + discount id
    shows = []                                                           # start with an empty list
    f = open(SHOW_FILE, "r", encoding="utf-8")                           # open the showtimes file for reading
    first = True                                                         # skip-header flag
    for line in f:                                                       # read line by line
        if first:                                                        # first row is the header text
            first = False                                                # mark it as consumed
            continue                                                     # skip the header
        parts = split_csv_line(line)                                     # split row into columns (by comma)
        if len(parts) >= 9:                                              # make sure we have all 9 columns
            show = {                                                     # build a dictionary for one showtime
                "showtime_id":      parts[0],                            # e.g. ST0001
                "movie_id":         parts[1],                            # e.g. M001
                "auditorium":       parts[2],                            # e.g. AUD01
                "date":             parts[3],                            # e.g. 12-10-2025
                "start_time":       parts[4],                            # e.g. 0900
                "end_time":         parts[5],                            # e.g. 1150
                "normal_price":     parts[6],                            # e.g. 24.00 (text—we print it as-is)
                "discounted_price": parts[7],                            # e.g. 21.60 (may be empty)
                "discount_id":      parts[8]                             # e.g. D02 (may be empty)
            }
            shows.append(show)
    f.close()                                                            # close the file
    return shows                                                         # return list (maybe empty)  


def load_discounts():                                      # read discount rules into a dict
    discs = {}                                             # e.g. {"D02": {"name": "...", "policy": "..."}}
    f = open(DISCOUNT_FILE, "r", encoding="utf-8")         # open the discount file to read text
    first = True                                           # flag to skip header
    for line in f:                                         # go line-by-line
        if first:                                          # first line is the header row
            first = False                                  # mark header as consumed
            continue                                       # skip it
        parts = split_csv_line(line)                       # split by comma (simple split you already have)
        # We expect: [discount_id, name, policy...]  (policy may contain commas)
        if len(parts) >= 2:                                # need at least id + name
            disc_id = parts[0]                             # e.g. "D02"
            name    = parts[1]                             # e.g. "Students/kids/seniors/OKU"
            # IMPORTANT: join everything from index 2 to the end to rebuild the full policy, keeping commas
            policy  = ", ".join(parts[2:]).strip()         # e.g. "10% off for students, kids, senior citizens, and OKU."
            discs[disc_id] = {"name": name, "policy": policy}  # store in a dictionary
    f.close()                                              # close file
    return discs                                           # give back the dictionary






def load_auditorium_seats():                                   # read the seating map for every auditorium
    seats_by_aud = {}                                          # will store something like {"AUD01": ["A01","A02",...], ...}
    lines = read_all_lines(AUD_SITTING_FILE)                   # read every line from auditorium_sitting.txt
    current_aud = None                                         # we'll remember which auditorium we're currently reading
    for line in lines:                                         # go through the file line by line
        txt = line.strip()                                     # remove spaces on both ends
        if txt == "":                                          # skip empty lines (they separate auditoriums)
            continue
        if txt.startswith("AUD"):                              # lines like "AUD01", "AUD02" mark a new auditorium
            current_aud = txt                                  # remember this auditorium id
            if current_aud not in seats_by_aud:                # if it's not already a key in our dict
                seats_by_aud[current_aud] = []                 # create an empty list for its seat IDs
            continue                                           # move to next line
        # seat lines have tokens like  A01:[O]  B10:[O]  etc, separated by spaces
        pieces = txt.split()                                   # split by spaces (many will just be seat tokens)
        for token in pieces:                                   # check each piece
            if ":" in token:                                   # seat tokens contain a colon, like "A01:[O]"
                seat_id = token.split(":")[0]                  # take only the part before ":" → "A01"
                seat_id = seat_id.strip()                      # trim just in case
                if current_aud is not None and seat_id != "":  # only keep if we know which auditorium we're in
                    seats_by_aud[current_aud].append(seat_id)  # add seat to that auditorium's list
    return seats_by_aud                                        # give back the full dictionary

def pad2(n):                          # make 1 -> "01", 9 -> "09", 12 -> "12"
    s = str(n)                        # turn number into string
    if len(s) < 2:                    # if shorter than 2 characters
        s = "0" + s                   # put a "0" in front (prefix)
    return s                          # give back the 2-digit string

def seat_row_col(seat_id):            # split "B09" into ("B", 9)
    letters = ""                      # will collect A/B/C...
    digits = ""                       # will collect 01/02/...
    for ch in seat_id:                # look at each character
        if ch.isalpha():              # A..Z?
            letters += ch             # add to the row letters
        else:                         # not a letter → assume digit
            digits += ch              # add to the number string
    col = 0
    if digits != "":                  # if we found digits
        col = int(digits)             # convert digits to an integer
    return letters, col               # return ("B", 9) for "B09"

def print_seat_map(aud_id, taken_seats, seats_by_aud):
    # If we don't have a layout for this auditorium, say so
    if aud_id not in seats_by_aud:
        print("No seating layout found for", aud_id)
        return

    valid = seats_by_aud[aud_id]      # all seat codes that exist in this room
    row_to_cols = {}                  # will map "A" -> [1,2,3,...]
    max_col = 0

    # Build row -> columns and remember largest column number
    for seat in valid:
        r, c = seat_row_col(seat)     # e.g. "A05" -> ("A", 5)
        if r not in row_to_cols:
            row_to_cols[r] = []
        if c not in row_to_cols[r]:
            row_to_cols[r].append(c)
        if c > max_col:
            max_col = c

    # Sort rows alphabetically; each row's columns numerically
    rows = []
    for r in row_to_cols:
        rows.append(r)
    rows.sort()
    for r in rows:
        row_to_cols[r].sort()

    # Legend + column header
    print("Legend: [ ] = available   [X] = taken")
    header = "    "                   # 4 spaces to align under row labels
    for c in range(1, max_col + 1):
        header = header + " " + pad2(c) + " "
    print(header)

    # One line per row, marking each seat spot
    for r in rows:
        line = r + " :"               # row label, e.g. "A :"
        existing = row_to_cols[r]     # which seat numbers exist in this row
        for c in range(1, max_col + 1):
            seat_code = r + pad2(c)   # build code like "A05"
            if c in existing:         # seat physically exists here?
                if seat_code in taken_seats:
                    line = line + " [X]"   # already booked
                else:
                    line = line + " [ ]"   # free
            else:
                line = line + "    "       # gap (keeps columns aligned)
        print(line)
    print()                          # blank line after the map

                                                      

# LOOKUPS 
def find_row_by_id(filename, id_index, target_id):                       # find a row where a specific column equals target_id
    lines = read_all_lines(filename)                                     # read all lines
    for i in range(1, len(lines)):                                       # loop from 1 to skip header at index 0
        parts = split_csv_line(lines[i])                                 # split the row into fields
        if len(parts) > id_index and parts[id_index] == target_id:       # check we have that column and it matches
            return parts                                                 # return the fields list for that row
    return None                                                          # if not found, return None

def get_auditorium_for_showtime(showtime_id):                  # find which auditorium a given showtime uses
    row = find_row_by_id(SHOW_FILE, 0, showtime_id)            # look for the row whose column-0 == showtime_id
    if row is None or len(row) < 3:                            # if not found or malformed
        return None                                            # we can't tell the auditorium
    return row[2]                                              # column-2 is auditorium_id (e.g., "AUD01")


# VALIDATED PROMPTS (keep asking until correct) 

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
        lines = read_all_lines(CUSTOMER_FILE)                           # read all customer rows
        for i in range(1, len(lines)):                                  # skip header
            parts = split_csv_line(lines[i])                            # split into list
            # expected order: [id, name, phone, email, password]
            if len(parts) >= 5 and parts[0] == cid and parts[4] == pwd:
                return cid                                              # success
        print("ID or password is incorrect. Try again.")

def ask_existing_movie_id():                                             # ask user for a real movie id
    movies = load_movies()                                               # read movies for display (list of dicts)
    if len(movies) == 0:                                                 # if there are no data rows
        print("No movies found in", MOVIE_FILE)                          # tell the user to put some data
    else:
        print("=== Movies ===")                                          # heading
        for m in movies:                                                 # show lines like "M0001 - Interstellar"
            print(m["movie_id"] + " - " + m["movie_name"])

    while True:                                                          # keep asking until valid
        mid = safe_input("Enter Movie ID (e.g. M001): ")                # ask for a movie id (as typed text)
        # look for a row in MOVIE_FILE where column 0 equals the typed id
        if find_row_by_id(MOVIE_FILE, 0, mid):                           # True => id exists in file
            return mid                                                   # valid -> return it to the caller
        print("Invalid Movie ID. Try again.")                            # otherwise loop again


# Register + Update personal details 
def register_customer():  # add a new row to customers.txt
    cust_id = next_id_by_count(CUSTOMER_FILE, "C")  # build next id like "C0001"
    name  = safe_input("Name: ")
    phone = safe_input("Phone (digits only, include 60): ")
    while not phone.isdigit():
        print("Phone must be digits only.")
        phone = safe_input("Phone (digits only): ")
    email = safe_input("Email: ")
    while "@" not in email:
        print("Email must contain '@'.")
        email = safe_input("Email: ")

    while True:
        pwd1 = safe_input("Create password: ")
        pwd2 = safe_input("Confirm password: ")
        if pwd1 != "" and pwd1 == pwd2:
            break
        print("Passwords do not match or are empty. Try again!")

    new_row = join_csv([cust_id, name, phone, email, pwd1])              # build a CSV-like line
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
def view_all_movie_showtimes():                      # show all showtimes (with prices + discount info)
    movies = load_movies()                           # list of {"movie_id","movie_name"}
    shows  = load_showtimes()                        # list of showtime dicts (now includes prices + discount_id)
    discs  = load_discounts()                        # dictionary of discount rules, by discount_id

    if len(movies) == 0 or len(shows) == 0:          # if either file has no data rows
        print("No movies or showtimes to display.")
        return

    # build a quick map from movie_id -> movie_name for printing titles
    name_of = {}
    for m in movies:
        name_of[m["movie_id"]] = m["movie_name"]

    print("=== All Movie Showtimes ===")
    n = 1
    for s in shows:
        title = name_of.get(s["movie_id"], "(title not found)")
        print(str(n) + ". Movie:", title)            # numbered movie title line
        print("   date:", s["date"])                 # show date (as text from file)
        print("   time:", s["start_time"])           # show start time
        print("   venue:", s["auditorium"])          # auditorium id

        # --- NEW: prices ---
        if s["normal_price"] != "":                  # print normal price if present
            print("   normal price: RM", s["normal_price"])
        if s["discounted_price"] != "" and s["discount_id"] != "":  # only if the file has a discount filled in
            did = s["discount_id"]                                   # e.g. D02
            rule = discs.get(did, None)                               # look up rule text by id
            print("   discounted price: RM", s["discounted_price"])   # show discounted price
            if rule is not None:
                # show the rule name + policy to guide the user
                print("   discount:", did, "-", rule["name"])
                print("   who qualifies: 10% off for students, kids, senior citizens, and OKU.")
        print()                                      # blank line between entries
        n = n + 1


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
def book_ticket():
    cid = ask_existing_customer_login()           # cid = Customer ID string (e.g., "C0003") returned after a valid ID+password login
    mid = ask_existing_movie_id()                 # mid = Movie ID string the user chose (e.g., "M0002")
    sid = ask_existing_showtime_id_for_movie(mid) # sid = Showtime ID string (e.g., "ST0007") chosen from showtimes that belong to that movie

    # Figure out auditorium + load seating map ONCE
    aud_id = get_auditorium_for_showtime(sid)     # aud_id = which auditorium this showtime uses (e.g., "AUD01")
    seats_map = load_auditorium_seats()           # seats_map = dict like {"AUD01":[seat codes...], "AUD02":[...]} read from auditorium_sitting.txt
    taken = seats_taken_for_show(sid)             # taken = list of seat codes already booked for this specific showtime (e.g., ["A04","B10"])
    valid_seats = seats_map.get(aud_id, [])       # valid_seats = list of seats that physically exist in this auditorium; [] if aud_id missing

    print("\n=== Seat Map ===\n")                 
    print_seat_map(aud_id, taken, seats_map)      # Draws a grid: shows each seat as [ ] (free) or [X] (taken) using the room layout in seats_map

    print("This show is in", aud_id + ". Seats will be checked against that auditorium.\n")  # Inform the user which room they’re picking seats in

    # choose seats (remove duplicates, must exist here, not already taken)
    while True:                                    # Loop until the user provides a valid seat selection
        raw = safe_input("Seats (e.g. A01|A02): ") # raw = exact text the user typed, like "A01|A02| B03"
        pieces = raw.split("|")                    # pieces = ["A01", "A02", " B03"] (split on '|')
        chosen = []                                # chosen = cleaned list of unique seats we'll accept
        for p in pieces:                           # go through each typed piece
            s = p.strip()                          # s = remove spaces → "B03" instead of " B03"
            if s != "" and s not in chosen:        # ignore empties and duplicates
                chosen.append(s)                   # keep this seat code

        if len(chosen) == 0:                       # must pick at least one seat
            print("Enter at least one seat.\n")
            continue                               # ask again

        # seats must exist in this auditorium
        bad = [s for s in chosen if s not in valid_seats]  # bad = any seat codes that are NOT in this room’s layout
        if len(bad) > 0:                                   # if the user typed seats that don't exist here
            print("These seats are not valid for", aud_id + ":", ", ".join(bad))
            print("Please choose seats that exist in", aud_id + ".\n")
            continue                                       # ask again

        # seats must not already be taken
        conflict = False                          # conflict flag: assume no clashes first
        for s in chosen:                          # check each seat the user wants
            if s in taken:                        # if someone has already booked it in this showtime
                print("Seat", s, "already taken. Pick others.")
                conflict = True                   # mark a problem so we can re-prompt
        if conflict:                              # any seat was taken?
            print("")                             # small blank line for spacing
            continue                              # re-ask for seats

        # normalize to "A01|A02|B03"
        seats_text = ""                           # build the text we will save to the file
        for i in range(len(chosen)):              # walk through chosen seats in order
            seats_text = chosen[i] if i == 0 else seats_text + "|" + chosen[i]  # add '|' between items
        break                                     # we have a valid selection; exit the seat-picking loop

    # price summary + discount policy
    shows = load_showtimes()                      # shows = list of all showtime dicts (includes prices + discount_id)
    discs = load_discounts()                      # discs = dict of discount rules by id, e.g., {"D02": {"name": "...", "policy": "..."}}
    the_show = None                               # will hold the dict for THIS showtime
    for s in shows:                               # find the showtime dict that matches sid
        if s["showtime_id"] == sid:
            the_show = s
            break

    print("")                                     # spacing before price info
    if the_show is not None:                      # safety: only show prices if we successfully found the show
        if the_show["normal_price"] != "":        # print normal price if present
            print("Normal price per ticket: RM", the_show["normal_price"])
        if the_show["discounted_price"] != "" and the_show["discount_id"] != "":  # only if discounted info is set
            did = the_show["discount_id"]         # did = discount id, e.g., "D02"
            print("Discounted price per ticket: RM", the_show["discounted_price"])
            if did in discs:                      # if we have a policy entry for this discount id
                print("Discount:", did, "-", discs[did]["name"])   # short label/name
                print("Who qualifies: 10% off for students, kids, senior citizens, and OKU.")      # full sentence policy text from file
        else:
            print("No discount set for this showtime.")            # nothing special for this show
    print("")                                     # extra spacing before ticket counts

    normal = read_int("Normal tickets: ")         # normal = integer count of regular tickets
    disc = 0                                      # default: 0 discounted tickets
    if the_show is not None and the_show["discounted_price"] != "" and the_show["discount_id"] != "":
        disc = read_int("Discounted tickets (if you qualify): ")   # disc = integer count of discounted tickets

    bid = next_id_by_count(BOOKING_FILE, "B")     # bid = new Booking ID (e.g., "B0007") based on number of rows in booking file
    tickets_text = str(normal) + "|" + str(disc)  # tickets_text = "normal|discount" (e.g., "2|1")
    new_row = join_csv([bid, sid, cid, seats_text, tickets_text])  # build CSV-like line in the required column order
    append_line(BOOKING_FILE, new_row)            # append that line to movie_bookings.txt (adds a newline automatically)

    print("\nBooked! Your Booking ID is:", bid, "\n")  # final confirmation to the user


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



# MENU (only the 4 tasks)
def main_customer():                                                      # main menu loop
    while True:                                                          # keep showing options until user exits
        print("\n=== CUSTOMER MENU ===")                                 # a blank line then the title
        print("[1] Register / Create account")                           # option 1
        print("[2] Update my account details")                           # option 2
        print("[3] View all movie showtimes (Movie/Date/Time/Venue)")    # option 3
        print("[4] Book tickets")                                        # option 4
        print("[5] Cancel my ticket")                                    # option 5
        print("[6] View my booking history")                             # option 6
        print("[0] Exit")                                                # option 0   <-- REMOVED the old [7] line
        choice = read_int("Enter your choice: ")                         # read a number safely

        if choice == 1:   register_customer()                            # run register
        elif choice == 2: update_my_details()                            # run update
        elif choice == 3: view_all_movie_showtimes()                     # run view current/upcoming
        elif choice == 4: book_ticket()                                  # run book
        elif choice == 5: cancel_ticket()                                # run cancel
        elif choice == 6: view_booking_history()                         # run history
        elif choice == 0:                                                 # exit
            print("Goodbye!")                                            # goodbye text
            main()
            break                                                        # leave the loop and end program
        else:
            print("Invalid choice. Try again.")                          # anything else -> errors then loop


if __name__ == "__main__":                                               # this is True when we press Run on this file
    main_customer()                                                               # start the program
