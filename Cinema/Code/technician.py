# # TODO: 
# # put your data into a txt file, only code here in py file. Use "with open(...) as f:..." to read, write, append to txt file. For screenings, use movie_showtimes.txt

import json

SCREENINGS_FILE = "movie_listing.txt"
EQUIPMENT_FILE = "equipment_status.txt"
ISSUES_FILE = "technical_issues.txt"

def load_data(filename, default_data):
    try:
        with open(filename, "r") as f:
            data= json.load(f)
            return data if data else default_data
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

screenings = load_data(SCREENINGS_FILE, [
    {"Movie": "How to Train Your Dragon", "Time": "30-08-2025 20:00", "Auditorium": "Hall 1"},
    {"Movie": "Movie 2", "Time": "30-08-2025 21:00", "Auditorium": "Hall 2"},
])

equipment_status = load_data(EQUIPMENT_FILE, {
    "Hall 1": {"Projector": "Ready", "Sound": "Ready", "Air Conditioner": "Ready"},
    "Hall 2": {"Projector": "Ready", "Sound": "Ready", "Air Conditioner": "Ready"}
})

technical_issues = load_data(ISSUES_FILE, [])

def view_schedules():
    print("\n--- Upcoming Movie Screening Schedule ---")
    if not screenings:
        print("No screening available.\n")
        return
    for s in screenings:
        print(f"Movie: {s['Movie']}, Time: {s['Time']}, Auditorium: {s['Auditorium']}")
    print("------------------------------------------\n")


def report_issue():
    try:
        # numbered list of halls
        halls = list(equipment_status.keys())
        for i, h in enumerate(halls, 1):
            print(f"{i}. {h}")
        hall_choice = int(input("Choose a hall: "))
        hall = halls[hall_choice - 1]

        # numbered list of equipment
        equipment_list = list(equipment_status[hall].keys())
        for i, eq in enumerate(equipment_list, 1):
            print(f"{i}. {eq}")
        eq_choice = int(input("Choose equipment: "))
        equipment = equipment_list[eq_choice - 1]

        description = input("Describe the issue: ")

        # update data
        technical_issues.append({"Hall": hall, "Equipment": equipment, "Description": description})
        equipment_status[hall][equipment] = "Under Maintenance"

        # save to files
        save_data(ISSUES_FILE, technical_issues)
        save_data(EQUIPMENT_FILE, equipment_status)

        print(f"Issue reported for {equipment} in {hall}. Status set to 'Under Maintenance'.\n")

    except (ValueError, IndexError):
        print("Invalid choice. Try again.\n")


def confirm_readiness():
    halls = list(equipment_status.keys())
    for i, h in enumerate(halls, 1):
        print(f"{i}. {h}")
    hall_choice = int(input("Choose a hall: "))
    hall = halls[hall_choice - 1]

    print(f"\nEquipment Status for {hall}:")
    for eq, status in equipment_status[hall].items():
        print(f"{eq}: {status}")
    print()


def mark_equipment():
    try:
        halls = list(equipment_status.keys())
        for i, h in enumerate(halls, 1):
            print(f"{i}. {h}")
        hall_choice = int(input("Choose a hall: "))
        hall = halls[hall_choice - 1]

        equipment_list = list(equipment_status[hall].keys())
        for i, eq in enumerate(equipment_list, 1):
            print(f"{i}. {eq}")
        eq_choice = int(input("Choose equipment: "))
        equipment = equipment_list[eq_choice - 1]

        statuses = ["Ready", "Under Maintenance", "Resolved"]
        for i, st in enumerate(statuses, 1):
            print(f"{i}. {st}")
        status_choice = int(input("Choose new status: "))
        new_status = statuses[status_choice - 1]

        equipment_status[hall][equipment] = new_status
        save_data(EQUIPMENT_FILE, equipment_status)

        print(f"Equipment '{equipment}' in {hall} updated to '{new_status}'.\n")

    except (ValueError, IndexError):
        print("Invalid choice. Try again.\n")


def main():
    while True:
        print("=== Technician Management Menu ===")
        print("1. View Upcoming Screenings")
        print("2. Report Technical Issue")
        print("3. Confirm Equipment Readiness")
        print("4. Mark Equipment Status")
        print("5. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            view_schedules()
        elif choice == "2":
            report_issue()
        elif choice == "3":
            confirm_readiness()
        elif choice == "4":
            mark_equipment()
        elif choice == "5":
            print("Exiting Technician System. Goodbye!")
            break
        else:
            print("Invalid choice. Try again!\n")


if __name__ == "__main__":
    main()