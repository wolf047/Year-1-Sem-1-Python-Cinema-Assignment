

from datetime import datetime


TICKET_PRICE = 15.00
STUDENT_DISCOUNT = 0.20


MOVIES_FILE = "Cinema/Database/movie_listings.txt"
BOOKINGS_FILE = "Cinema/Database/movie_bookings.txt"



def setup():
    """Create sample data files"""
    try:
        # Create movies file
        open(MOVIES_FILE, 'a').close()
        with open(MOVIES_FILE, 'r') as f:
            if not f.read():
                with open(MOVIES_FILE, 'w') as f:
                    f.write("M01,Avengers,Hall A,2025-10-08,10:00\n")
                    f.write("M02,Frozen,Hall B,2025-10-08,14:00\n")
                    f.write("M03,Spider-Man,Hall A,2025-10-08,18:00\n")

        # Create bookings file
        open(BOOKINGS_FILE, 'a').close()
    except:
        pass



def view_movies():
    """Show all movies"""
    print("\n" + "=" * 60)
    print("AVAILABLE MOVIES")
    print("=" * 60)
    print(f"{'ID':<6} {'Title':<15} {'Hall':<10} {'Date':<12} {'Time'}")
    print("-" * 60)

    with open(MOVIES_FILE, 'r') as f:
        for line in f:
            m = line.strip().split(',')
            print(f"{m[0]:<6} {m[1]:<15} {m[2]:<10} {m[3]:<12} {m[4]}")


def view_bookings():
    """Show all bookings"""
    print("\n" + "=" * 70)
    print("ALL BOOKINGS")
    print("=" * 70)
    print(f"{'ID':<8} {'Name':<15} {'Movie':<8} {'Seats':<8} {'Price':<10} {'Status'}")
    print("-" * 70)

    with open(BOOKINGS_FILE, 'r') as f:
        lines = f.readlines()
        if not lines:
            print("No bookings found.")
            return
        for line in lines:
            b = line.strip().split(',')
            print(f"{b[0]:<8} {b[1]:<15} {b[2]:<8} {b[3]:<8} RM{b[4]:<8} {b[5]}")



def book_ticket():
    """Book a new ticket"""
    print("\n" + "=" * 50)
    print("BOOK TICKET")
    print("=" * 50)


    view_movies()


    movie_id = input("\nMovie ID: ").strip().upper()
    name = input("Customer Name: ").strip()
    seat = input("Seat (e.g., A1): ").strip().upper()
    is_student = input("Student? (Y/N): ").strip().upper()


    if not movie_id or not name or not seat:
        print("Error: All fields required!")
        return


    price = TICKET_PRICE
    if is_student == 'Y':
        price = price * (1 - STUDENT_DISCOUNT)


    print(f"\nCustomer: {name}")
    print(f"Movie: {movie_id}")
    print(f"Seat: {seat}")
    print(f"Price: RM{price:.2f}")


    confirm = input("\nConfirm? (Y/N): ").strip().upper()
    if confirm != 'Y':
        print("Cancelled.")
        return


    try:
        with open(BOOKINGS_FILE, 'r') as f:
            lines = f.readlines()
            if lines:
                last_id = int(lines[-1].split(',')[0][1:])
                booking_id = f"B{last_id + 1:03d}"
            else:
                booking_id = "B001"
    except:
        booking_id = "B001"

    # Save booking
    with open(BOOKINGS_FILE, 'a') as f:
        f.write(f"{booking_id},{name},{movie_id},{seat},{price:.2f},Active\n")


    print("\n" + "=" * 40)
    print("RECEIPT")
    print("=" * 40)
    print(f"Booking ID: {booking_id}")
    print(f"Customer: {name}")
    print(f"Movie: {movie_id}")
    print(f"Seat: {seat}")
    print(f"Price: RM{price:.2f}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 40)
    print("Thank you!")



def cancel_booking():
    """Cancel a booking"""
    print("\n" + "=" * 50)
    print("CANCEL BOOKING")
    print("=" * 50)


    view_bookings()


    booking_id = input("\nBooking ID to cancel: ").strip().upper()
    if not booking_id:
        print("Error: Booking ID required!")
        return


    with open(BOOKINGS_FILE, 'r') as f:
        bookings = f.readlines()


    found = False
    for i, line in enumerate(bookings):
        b = line.strip().split(',')
        if b[0] == booking_id:
            if b[5] == "Cancelled":
                print("Already cancelled!")
                return

            print(f"\nCustomer: {b[1]}")
            print(f"Movie: {b[2]}")
            print(f"Seat: {b[3]}")

            confirm = input("\nConfirm cancel? (Y/N): ").strip().upper()
            if confirm != 'Y':
                print("Aborted.")
                return

            b[5] = "Cancelled"
            bookings[i] = ','.join(b) + '\n'
            found = True
            break

    if not found:
        print("Booking not found!")
        return


    with open(BOOKINGS_FILE, 'w') as f:
        f.writelines(bookings)

    print(f"\nBooking {booking_id} cancelled!")



def modify_booking():
    """Modify customer name"""
    print("\n" + "=" * 50)
    print("MODIFY BOOKING")
    print("=" * 50)


    view_bookings()


    booking_id = input("\nBooking ID: ").strip().upper()
    if not booking_id:
        print("Error: Booking ID required!")
        return

    with open(BOOKINGS_FILE, 'r') as f:
        bookings = f.readlines()

    found = False
    for i, line in enumerate(bookings):
        b = line.strip().split(',')
        if b[0] == booking_id:
            if b[5] == "Cancelled":
                print("Cannot modify cancelled booking!")
                return

            print(f"\nCurrent name: {b[1]}")
            new_name = input("New name: ").strip()

            if not new_name:
                print("Name cannot be empty!")
                return

            b[1] = new_name
            bookings[i] = ','.join(b) + '\n'
            found = True
            break

    if not found:
        print("Booking not found!")
        return

    with open(BOOKINGS_FILE, 'w') as f:
        f.writelines(bookings)

    print(f"\nBooking {booking_id} updated!")

def process_payment():
    """Process payment"""
    print("\n" + "=" * 50)
    print("PROCESS PAYMENT")
    print("=" * 50)

    view_bookings()

    booking_id = input("\nBooking ID: ").strip().upper()
    if not booking_id:
        print("Error: Booking ID required!")
        return

    with open(BOOKINGS_FILE, 'r') as f:
        for line in f:
            b = line.strip().split(',')
            if b[0] == booking_id:
                if b[5] == "Cancelled":
                    print("Cannot pay for cancelled booking!")
                    return

                print(f"\nCustomer: {b[1]}")
                print(f"Amount: RM{b[4]}")
                print("\nPayment: 1.Cash 2.Card 3.E-Wallet")

                method = input("Select: ").strip()
                if method not in ['1', '2', '3']:
                    print("Invalid method!")
                    return

                methods = {'1': 'Cash', '2': 'Card', '3': 'E-Wallet'}

                print("\n" + "=" * 40)
                print("PAYMENT RECEIPT")
                print("=" * 40)
                print(f"Booking: {b[0]}")
                print(f"Customer: {b[1]}")
                print(f"Amount: RM{b[4]}")
                print(f"Method: {methods[method]}")
                print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                print("=" * 40)
                print("Payment successful!")
                return

        print("Booking not found!")


def main():
    """Main program"""
    setup()

    print("*" * 50)
    print(" CINEMA TICKETING SYSTEM")
    print("*" * 50)

    while True:
        print("\n" + "=" * 50)
        print("MENU")
        print("=" * 50)
        print("1. View Movies")
        print("2. Book Ticket")
        print("3. View Bookings")
        print("4. Cancel Booking")
        print("5. Modify Booking")
        print("6. Process Payment")
        print("7. Exit")

        choice = input("\nChoice (1-7): ").strip()

        if choice == '1':
            view_movies()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            view_bookings()
        elif choice == '4':
            cancel_booking()
        elif choice == '5':
            modify_booking()
        elif choice == '6':
            process_payment()
        elif choice == '7':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice!")

        input("\nPress Enter...")


if __name__ == "__main__":
    main()