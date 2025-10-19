# --- Use relative paths anchored to the script folder ---
import os

try:
    SCRIPT_DIR = os.path.dirname(__file__)       
except NameError:                                  
    SCRIPT_DIR = os.getcwd()

# Make the script folder the working directory so relative paths are stable
if os.getcwd() != SCRIPT_DIR:
    os.chdir(SCRIPT_DIR)

BASE = os.path.join("Database")                    # relative
os.makedirs(BASE, exist_ok=True)

# Relative file paths (no absolute components)
MOVIE_FILE        = os.path.join(BASE, "movie_listings.txt")
SHOW_FILE         = os.path.join(BASE, "movie_showtimes.txt")
CUSTOMER_FILE     = os.path.join(BASE, "customer.txt")
BOOKING_FILE      = os.path.join(BASE, "movie_bookings.txt")
AUD_SITTING_FILE  = os.path.join(BASE, "auditorium_sitting.txt")
DISCOUNT_FILE     = os.path.join(BASE, "discount_policies.txt")



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

#  GO BACK HELPERS
EXIT_HINT = " (Enter 0 to return to menu)"      # message shown at each prompt

def read_int_or_menu(msg):                      # safe number input with 0 to exit
    while True:
        t = safe_input(msg + EXIT_HINT + ": ")  # show message + exit hint
        if t == "0":                            # user typed 0 → go back to menu
            return None
        if t.isdigit():                         # must be digits only
            return int(t)                       # return as integer
        print("Please enter digits only.")      # re-ask if invalid

def input_or_menu(msg):                         # text input with 0 to exit
    t = safe_input(msg + EXIT_HINT + ": ")      # add (Enter 0 to return)
    if t == "0":                                # allow immediate exit
        return None
    return t.strip()                            # remove extra spaces

# PHONE VALIDATION 
def is_valid_msisdn_with_60(text):              # check phone format
    return text.isdigit() and text.startswith("60") and len(text) > 2
    # must be digits, start with 60, and longer than 2 chars (e.g. 60123456789)




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
def read_all_lines(filename):                                                     # read all lines from a file (safe)
    try:                                                                          # ← protect file open/read
        f = open(filename, "r", encoding="utf-8")                                 # open the file for Reading text
        raw = f.readlines()                                                       # read all lines (each ends with "\n")
        f.close()                                                                 # close the file (good habit)
    except FileNotFoundError:                                                     # file is missing
        print(f"[Warning] Missing file: {filename}. (Returning empty list.)")     # friendly message
        return []                                                                 # keep app running
    except PermissionError:                                                       # no OS permission
        print(f"[Error] No permission to read: {filename}.")                      # explain
        return []                                                                 # keep app running
    except OSError as e:                                                          # other disk/OS errors
        print(f"[Error] Could not read {filename}: {e}")                          # explain
        return []                                                                 # keep app running

    out = []                                                                       # we'll store cleaned lines here
    for ln in raw:                                                                 # go through each raw line
        out.append(ln.rstrip("\n"))                                                # remove the trailing newline only
    return out                                                                     # return the cleaned list

def append_line(filename, one_line):                                              # add exactly one line to end (safe)
    try:                                                                          # ← protect file open/write
        f = open(filename, "a", encoding="utf-8")                                 # open for Appending text
        f.write(one_line + "\n")                                                  # write the text and a newline
        f.close()                                                                 # close the file
    except PermissionError:                                                       # OS forbids writing here
        print(f"[Error] No permission to write: {filename}. Data not saved.")     # explain
    except OSError as e:                                                          # other disk/OS errors
        print(f"[Error] Could not append to {filename}: {e}. Data not saved.")    # explain

def write_all_lines(filename, lines):                                             # replace whole file (safe)
    try:                                                                          # ← protect file open/write
        f = open(filename, "w", encoding="utf-8")                                 # open for Writing text (clears file)
        for ln in lines:                                                          # go through each line we want to save
            f.write(ln + "\n")                                                    # write it and add a newline
        f.close()                                                                 # close the file
    except PermissionError:                                                       # OS forbids writing here
        print(f"[Error] No permission to write: {filename}. Changes not saved.")  # explain
    except OSError as e:                                                          # other disk/OS errors
        print(f"[Error] Could not write {filename}: {e}. Changes not saved.")     # explain

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
def load_movies():                                                        # read movies we care about (id + name) via safe helper
    lines = read_all_lines(MOVIE_FILE)                                    # safely read all lines ([] on error)
    movies = []                                                           # start an empty list
    for i, line in enumerate(lines):                                      # go line by line with index
        if i == 0:                                                        # index 0 is the header row
            continue                                                      # skip header
        parts = split_csv_line(line)                                      # split row into fields
        if len(parts) >= 2:                                               # need at least movie_id and movie_name
            movies.append({"movie_id": parts[0], "movie_name": parts[1]}) # keep the 2 fields we use
    return movies                                                         # return list (maybe empty)


def load_showtimes():                                                     # read showtimes + prices + discount id (safe)
    lines = read_all_lines(SHOW_FILE)                                     # safely read all lines
    shows = []                                                            # will collect showtime dicts here
    for i, line in enumerate(lines):                                      # walk through file
        if i == 0:                                                        # header?
            continue                                                      # skip it
        parts = split_csv_line(line)                                      # split row into columns
        if len(parts) >= 9:                                               # ensure all 9 columns exist
            shows.append({                                                # build one showtime record
                "showtime_id":      parts[0],                             # e.g. ST0001
                "movie_id":         parts[1],                             # e.g. M001
                "auditorium":       parts[2],                             # e.g. AUD01
                "date":             parts[3],                             # e.g. 12-10-2025
                "start_time":       parts[4],                             # e.g. 0900
                "end_time":         parts[5],                             # e.g. 1150
                "normal_price":     parts[6],                             # e.g. 24.00 (string)
                "discounted_price": parts[7],                             # e.g. 21.60 (string or "")
                "discount_id":      parts[8],                             # e.g. D02 (string or "")
            })
    return shows                                                          # return list (maybe empty)


def load_discounts():                                                     # read discount rules (safe)
    lines = read_all_lines(DISCOUNT_FILE)                                 # safely read all lines
    discs = {}                                                            # will be {"D02":{"name":..., "policy":...}, ...}
    for i, line in enumerate(lines):                                      # go through file
        if i == 0:                                                        # header row?
            continue                                                      # skip it
        parts = split_csv_line(line)                                      # split by comma (policy may have commas)
        if len(parts) >= 2:                                               # need at least id + name
            disc_id = parts[0]                                            # e.g. "D02"
            name    = parts[1]                                            # e.g. "Students/kids/seniors/OKU"
            policy  = ", ".join(parts[2:]).strip()                        # join the rest back → full sentence policy
            discs[disc_id] = {"name": name, "policy": policy}             # store in dictionary
    return discs                                                          # return dict (maybe empty)



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

def pad2(n):                          # make 1 -> "01", 12 -> "12"
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

    # Sort rows alphabetically, each row's columns numerically
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
def ask_existing_showtime_id_for_movie(movie_id):                 # showtime selector
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
        sid = input_or_menu("Enter Showtime ID (e.g. ST0001)")    # allow 0 to exit
        if sid is None: return None
        row = find_row_by_id(SHOW_FILE, 0, sid)
        if row is not None and len(row) > 1 and row[1] == movie_id:
            print()
            return sid
        print("Invalid showtime for that movie. Try again.\n")


def ask_existing_customer_login():                                # login check with exit
    while True:
        cid = input_or_menu("Customer ID (e.g. C0001)")           
        if cid is None: return None                               # back to menu
        pwd = input_or_menu("Password")
        if pwd is None: return None

        lines = read_all_lines(CUSTOMER_FILE)
        for i in range(1, len(lines)):
            parts = split_csv_line(lines[i])
            if len(parts) >= 5 and parts[0] == cid and parts[4] == pwd:
                return cid                                        # login success
        print("ID or password incorrect. Try again.")

def ask_existing_movie_id():                                      # select movie safely
    movies = load_movies()
    if len(movies) == 0:
        print("No movies found in", MOVIE_FILE)
    else:
        print("=== Movies ===")
        for m in movies:
            print(m["movie_id"] + " - " + m["movie_name"])

    while True:
        mid = input_or_menu("Enter Movie ID (e.g. M001)")         # ask with 0 to exit
        if mid is None: return None                               # back to menu
        if find_row_by_id(MOVIE_FILE, 0, mid):
            return mid
        print("Invalid Movie ID. Try again.")

# Register + Update personal details 
def register_customer():                                          # add new customer
    cust_id = next_id_by_count(CUSTOMER_FILE, "C")                # auto-generate id (e.g. C0001)

    name = input_or_menu("Name")                                  # ask name (0 to exit)
    if name is None: return                                       # exit early

    while True:
        phone = input_or_menu("Phone (must start with 60)")       # ask phone number
        if phone is None: return                                  # exit early
        if is_valid_msisdn_with_60(phone): break                  # valid → stop loop
        print("Phone must start with '60' and contain digits only.") # show rule

    email = input_or_menu("Email")                                # ask email
    if email is None: return
    while "@" not in email:                                       # ensure @ in email
        print("Email must contain '@'.")                          
        email = input_or_menu("Email")
        if email is None: return

    while True:                                                   # password loop
        pwd1 = input_or_menu("Create password")
        if pwd1 is None: return
        pwd2 = input_or_menu("Confirm password")
        if pwd2 is None: return
        if pwd1 != "" and pwd1 == pwd2: break                     # must match
        print("Passwords do not match. Try again.")

    new_row = join_csv([cust_id, name, phone, email, pwd1])       # combine data
    append_line(CUSTOMER_FILE, new_row)                           # save to file
    print("Registered! Your customer ID is:", cust_id)            # confirmation


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
def book_ticket():                                                     # TASK: guide user through selecting a show and booking seats
    # LOGIN (with exit)
    cid = ask_existing_customer_login()                                # ask for ID+password; returns None if user entered 0 at any prompt
    if cid is None:                                                    # user chose to exit
        return                                                         # go back to main menu

    # PICK MOVIE (with exit)
    mid = ask_existing_movie_id()                                      # shows all movies and asks for a valid Movie ID
    if mid is None:                                                    # user chose to exit
        return

    # PICK SHOWTIME (with exit)
    sid = ask_existing_showtime_id_for_movie(mid)                      # lists showtimes for that movie and asks for a valid Showtime ID
    if sid is None:                                                    # user chose to exit
        return

    # LOAD CONTEXT NEEDED FOR SEAT VALIDATION + DISPLAY
    aud_id = get_auditorium_for_showtime(sid)                          # which auditorium this showtime uses (e.g., AUD01)
    seats_map = load_auditorium_seats()                                # dict: { "AUD01": ["A01","A02",...], ... }
    taken = seats_taken_for_show(sid)                                   # list of seats already booked for this showtime
    valid_seats = seats_map.get(aud_id, [])                             # list of seats that physically exist in this auditorium

    # SHOW VISUAL SEAT MAP
    print("\n=== Seat Map ===\n")
    print_seat_map(aud_id, taken, seats_map)                            # draws a grid: [ ] free, [X] taken 
    print("This show is in", aud_id + ". Seats will be checked against that auditorium.\n")

    # ASK USER FOR SEAT CODES (A01|A02|...) — allow exit; ensure they exist + not taken
    while True:
        raw = input_or_menu("Seats (e.g. A01|A02)")                     # user can type 0 to exit
        if raw is None:                                                 # user exited
            return

        # CLEAN + DEDUP INPUT: split by '|' and strip spaces → ["A01","A02",...]
        pieces = raw.split("|")
        chosen = [p.strip() for p in pieces if p.strip() != ""]         # ignore blanks like " |  "
        if len(chosen) == 0:                                            # must choose at least one seat
            print("Enter at least one seat.\n")
            continue

        # VALIDATION 1: typed seats must physically exist in this auditorium layout
        bad = [s for s in chosen if s not in valid_seats]
        if len(bad) > 0:
            print("These seats are not valid for", aud_id + ":", ", ".join(bad))
            print("Please choose seats that exist in", aud_id + ".\n")
            continue                                                    # re-ask

        # VALIDATION 2: none of the chosen seats can be already taken for this showtime
        conflict = False
        for s in chosen:
            if s in taken:
                print("Seat", s, "already taken. Pick others.")
                conflict = True
        if conflict:
            print("")                                                   # spacing
            continue                                                    # re-ask

        # if we reach here: all seats are valid and free → stop loop
        break

    #  PRICE INFO (so user knows the cost before confirming ticket counts)
    shows = load_showtimes()                                            # all showtime dicts
    discs = load_discounts()                                            # discount policies (id -> {name, policy})
    the_show = next((s for s in shows if s["showtime_id"] == sid), None)  # find this specific showtime dict or None

    print("")                                                           # spacing before price block
    if the_show:
        # print normal price if present (strings from file; print as-is)
        if the_show["normal_price"]:
            print("Normal price per ticket: RM", the_show["normal_price"])
        # print discount info only if both discounted_price and discount_id are set
        if the_show["discounted_price"] and the_show["discount_id"]:
            did = the_show["discount_id"]
            print("Discounted price per ticket: RM", the_show["discounted_price"])
            # OPTIONAL: display who qualifies (from discount file if available)
            if did in discs:
                # You already show a friendly, simplified policy line:
                print("Who qualifies: 10% off for students, kids, senior citizens, and OKU.")
        else:
            print("No discount set for this showtime.")
    print("")                                                           # spacing after price block

    # TICKET COUNTS (with exit)
    normal = read_int_or_menu("Normal tickets")                         # returns int or None if user typed 0
    if normal is None:
        return
    disc = 0                                                            # default
    # only ask for discounted tickets if the showtime actually has a discount
    if the_show and the_show["discounted_price"] and the_show["discount_id"]:
        disc = read_int("Discounted tickets (if you qualify; enter 0 if none): ")

    # SAVE BOOKING ROW
    bid = next_id_by_count(BOOKING_FILE, "B")                           # e.g., "B0007" based on number of rows
    tickets_text = str(normal) + "|" + str(disc)                        # "normal|discount", e.g. "2|1"
    new_row = join_csv([bid, sid, cid, "|".join(chosen), tickets_text]) # build CSV-like line in file order
    append_line(BOOKING_FILE, new_row)                                  # append to movie_bookings.txt

    # DONE
    print("\nBooked! Your Booking ID is:", bid, "\n")                   # final confirmation to user


def cancel_ticket():                                                     # TASK: let a logged-in user delete one of their bookings
    # READ FILE + LOGIN
    lines = read_all_lines(BOOKING_FILE)                                 # list of text lines (header + rows)
    cid = ask_existing_customer_login()                                  # ask ID+password (0 to exit)
    if cid is None:                                                      # user chose to exit
        return

    # SHOW ONLY *THIS USER’S* BOOKINGS + COLLECT THEIR BOOKING IDS
    my_ids = []                                                          # will hold booking IDs that belong to this user
    print("=== Your Bookings ===")                                       # simple heading
    for i in range(1, len(lines)):                                       # start from 1 to skip header line at index 0
        parts = split_csv_line(lines[i])                                 # convert row text -> list of fields
        # expected CSV order for bookings: [booking_id, showtime_id, customer_id, seats_text, tickets_text]
        if len(parts) >= 3 and parts[2] == cid:                          # ensure row has customer_id and it matches me
            my_ids.append(parts[0])                                      # remember the booking_id for validation later
            # small user-friendly summary of the row
            print("Booking:", parts[0], "| Show:", parts[1], "| Seats:", parts[3])

    # IF THE USER HAS NOTHING TO CANCEL, STOP EARLY
    if len(my_ids) == 0:
        print("You have no bookings.")                                   # nothing to cancel for this user
        return

    # ASK WHICH BOOKING TO CANCEL (with exit)
    while True:
        bid = input_or_menu("Enter Booking ID to cancel")                # allow typing 0 to go back
        if bid is None:                                                  # user chose to exit
            return
        if bid in my_ids:                                                # must belong to this user
            break                                                        # good → proceed to deletion
        print("That booking doesn't belong to you. Try again.")          # keep asking until valid

    # REWRITE FILE WITHOUT THE CHOSEN BOOKING
    new_lines = [lines[0]]                                               # keep the header unchanged
    for i in range(1, len(lines)):                                       # for each data row
        parts = split_csv_line(lines[i])                                 # split row into fields
        if parts[0] != bid:                                              # keep any row that is NOT the one we’re cancelling
            new_lines.append(lines[i])                                   # copy it forward
    write_all_lines(BOOKING_FILE, new_lines)                             # overwrite file safely with rows we kept

    # DONE
    print("Booking", bid, "cancelled.")                                  # confirmation to the user

# Booking history / Seat info
def view_booking_history():                                              # print all bookings for a given customer
    lines = read_all_lines(BOOKING_FILE)                                 # read all bookings
    cid = ask_existing_customer_login()                                  # ask whose history
    if cid is None:
        return
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



# MENU 
def main_customer():                                                      # main menu loop
    while True:                                                          # keep showing options until user exits
        print("\n=== CUSTOMER MENU ===")                                 # a blank line then the title
        print("[1] Register / Create account")                           # option 1
        print("[2] Update my account details")                           # option 2
        print("[3] View all movie showtimes (Movie/Date/Time/Venue)")    # option 3
        print("[4] Book tickets")                                        # option 4
        print("[5] Cancel my ticket")                                    # option 5
        print("[6] View my booking history")                             # option 6
        print("[0] Exit")                                                # option 0 to exit
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

