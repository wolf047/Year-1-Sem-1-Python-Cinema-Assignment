import os

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
