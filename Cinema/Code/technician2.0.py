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
            break
        else:
            print("!! Invalid Choice, Please Use 1 2 3 ... Format !!")


main_technician()