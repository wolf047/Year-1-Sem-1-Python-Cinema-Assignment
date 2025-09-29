def load_movies(filename=r"Cinema/Database/movie_listings.txt"):
    movies = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = [p.strip().strip('"') for p in line.split(",")]
                # protect against malformed lines
                if len(parts) < 11:
                    continue
                movie = {
                    "movie_id": parts[0],
                    "movie_name": parts[1],
                    "release_date": parts[2],
                    "running_time": parts[3],
                    "genre": parts[4],
                    "classification": parts[5],
                    "spoken_language": parts[6],
                    "subtitle_language": parts[7],
                    "director": parts[8],
                    "casts": parts[9],
                    "description": parts[10]
                }
                movies.append(movie)
    except FileNotFoundError:
        print("⚠️ movie_listing.txt not found! Please put it in Cinema\\Database\\movie_listing.txt or adjust the path.")
    return movies


def display_movies(movies):
    if not movies:
        print("⚠️ No movies available.")
        return

    print("\n🎬 --- Movie Listings --- 🎬")
    for m in movies:
        print(f"""
ID: {m['movie_id']}
Name: {m['movie_name']}
Release Date: {m['release_date']}
Running Time: {m['running_time']} min
Genre: {m['genre']}
Classification: {m['classification']}
Language: {m['spoken_language']} (Subtitles: {m['subtitle_language']})
Director: {m['director']}
Casts: {m['casts']}
Description: {m['description']}
""")
    print("------------------------------------------------------")


# ================== ISSUES (robust, deduped) ==================
ISSUES_FILE = "issues.txt"
AUDITORIUMS = [f"Auditorium {i}" for i in range(1, 9)]
EQUIPMENT_LIST = ["Projector", "Sound", "Air Conditioner"]


def load_issues(filename=ISSUES_FILE):
    """
    Load issues.txt into a dict keyed by (auditorium, equipment) -> status.
    Last occurrence in file wins (but usually file will be written by save_issues,
    so each pair appears once).
    """
    issues = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # split by '|' into at most 3 parts
                parts = [p.strip() for p in line.split("|", 2)]
                if len(parts) < 3:
                    continue
                aud, equip, status = parts[0], parts[1], parts[2]
                issues[(aud, equip)] = status
    except FileNotFoundError:
        # no file yet -> return empty dict
        pass
    return issues


def save_issues(issues, filename=ISSUES_FILE):
    """
    Save the issues dict to file (one canonical line per pair).
    """
    with open(filename, "w", encoding="utf-8") as f:
        # sort for stable ordering (optional)
        for (aud, equip), status in sorted(issues.items()):
            f.write(f"{aud} | {equip} | {status}\n")


# ----- action: report new issue (set Under Maintenance) -----
def report_issue():
    # Auditorium selection
    print("\nSelect Auditorium:")
    for i, a in enumerate(AUDITORIUMS, 1):
        print(f"{i}. {a}")
    choice = input("Enter choice (1-8): ")
    try:
        auditorium = AUDITORIUMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    # Equipment selection
    print("\nSelect Equipment:")
    for i, e in enumerate(EQUIPMENT_LIST, 1):
        print(f"{i}. {e}")
    choice = input("Enter choice (1-3): ")
    try:
        equipment = EQUIPMENT_LIST[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    # Load, update, save (this prevents duplicate lines)
    issues = load_issues()
    issues[(auditorium, equipment)] = "Under Maintenance"
    save_issues(issues)
    print(f"✅ Issue reported successfully: {auditorium} - {equipment} (Under Maintenance)")


# ----- view-only: show current equipment status for a chosen auditorium -----
def confirm_readiness():
    # (kept the old function name since it's option 3 in your menu)
    print("\nSelect Auditorium to view status:")
    for i, a in enumerate(AUDITORIUMS, 1):
        print(f"{i}. {a}")
    choice = input("Enter choice (1-8): ")
    try:
        auditorium = AUDITORIUMS[int(choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Returning to menu.")
        return

    issues = load_issues()  # dict
    print(f"\n📋 Current equipment status for {auditorium}:")
    found_any = False
    # show all equipment types with status (default "No record")
    for equip in EQUIPMENT_LIST:
        status = issues.get((auditorium, equip), None)
        if status is None:
            print(f"   {equip}: READY ")
        else:
            print(f"   {equip}: {status}")
            found_any = True

    if not found_any:
        print("   (No recorded statuses yet for this auditorium.)")


# ----- resolve: set a specific equipment to Resolved -----
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
        if issues[key] == "Under Maintenance":
            issues[key] = "Resolved"
            save_issues(issues)
            print(f"✅ Issue resolved: {auditorium} - {equipment}")
        elif issues[key] == "Resolved":
            print(f"ℹ️ Equipment already marked Resolved: {auditorium} - {equipment}")
        else:
            # if it was "OK" or other status, still update if you want:
            issues[key] = "Resolved"
            save_issues(issues)
            print(f"✅ Status updated to Resolved for {auditorium} - {equipment}")
    else:
        print("⚠️ No record found for that auditorium/equipment. Nothing to resolve.")

def reset_all_equipment():
    # Auditorium and equipment setup
    auditoriums = [f"Auditorium {i}" for i in range(1, 9)]
    equipment_list = ["Projector", "Sound", "Air Conditioner"]

    with open("issues.txt", "w", encoding="utf-8") as f:
        for auditorium in auditoriums:
            for equipment in equipment_list:
                f.write(f"{auditorium} | {equipment} | READY\n")

    print("🔄 All equipment has been reset to READY.")

# ================== MAIN MENU ==================
if __name__ == "__main__":
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
            confirm_readiness()   # view-only now
        elif choice == "4":
            mark_resolved()
        elif choice == "5":
            reset_all_equipment()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("!! Invalid Choice, Please Use 1 2 3 ... Format !!")