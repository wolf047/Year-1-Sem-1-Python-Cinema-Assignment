from datetime import datetime

# File names - Change these if your files have different names
MOVIE_FILE = "movie_listings.txt"
SHOWTIME_FILE = "movie_showtimes.txt"
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


def main():
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

