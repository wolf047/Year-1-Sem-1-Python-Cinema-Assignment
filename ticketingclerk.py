from datetime import datetime

# File names - Change these if your files have different names
MOVIE_FILE = "movie_listings.txt"
SHOWTIME_FILE = "movie_showtimes.txt"
BOOKING_FILE = "movie_bookings.txt"
AUDITORIUM_FILE = "auditorium_info.txt"


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


def main():
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
            break
        else:
            print("ERROR: Choose 1-7")

        input("\nPress Enter...")


if __name__ == "__main__":
    main()
