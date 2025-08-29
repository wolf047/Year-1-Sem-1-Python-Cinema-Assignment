screenings = [
    {"Movie": "Movie 1", "Time": "30-08-2025 20:00", "Auditorium": "hall 1"},
     {"Movie": "Movie 2", "Time": "30-08-2025 21:00", "Auditorium": "hall 2"},
]

equipment_status = {"Hall 1": {"Projector": "Ready", "Sound": "Ready","Air Conditioner": "Ready"},
                    "Hall 2": {"Projector": "Ready", "Sound": "Ready","Air Conditioner": "Ready"}
}

technical_issues = []

def view_schedules():
    print("n--- Upcoming Movie Screening Schedule ---")
    for s in screenings:
        print(f"Movie: {s['Movie']},Time: {s['Time']}, Audoitorium: {s['Auditorium']}")
    
    print("------------------------------------------\n")

def report_issue():
    try:
        hall = input('Enter Auditorium (Hall 1/Hall 2/Hall 3)')
        if hall not in equipment_status[hall]:
            raise ValueError("Invalid Equipment Type! ")
        
        issue = input("Enter Issue (Projector/Sound/Air Conditioner): ")
        if issue not in equipment_status[hall]:
            raise ValueError("Invalid equipment Type!")
        
        description = input("Describe the issue: ")
        technical_issues.append({"hall": hall, "equipment": issue, "description": description})
        equipment_status[hall][issue] = "Under Maintanence"
        print(f"Issue reported for {issue} in {hall}. Status set to 'Under Maintanence.\n")
    except ValueError as e:
        print(f"Error: {e}\n")
    except Exception:
        print("Unexpected Error occured while reporting issue!\n")

def comfirm_readiness():
    hall = input("Enter Auditorium to Comfirm Readiness: ")
    if hall not in equipment_status:
        print("invalid hall name!\n")
        return
    
    print(f"\nEquipment Status for {hall}: ")
    for eq, status in equipment_status[hall].items():
        print(f"{eq}: {status}")
    print()


def mark_equipment():
    try:
        hall = input("Enter Auditorium (Hall 1/Hall 2): ")
        if hall not in equipment_status:
            raise ValueError("Invalid auditorium!")

        equipment = input("Enter Equipment (Projector/Sound/Air Conditioner): ")
        if equipment not in equipment_status[hall]:
            raise ValueError("Invalid equipment!")

        new_status = input("Enter New Status (Ready/Under Maintenance/Resolved): ")
        if new_status not in ["Ready", "Under Maintenance", "Resolved"]:
            raise ValueError("Invalid status!")

        equipment_status[hall][equipment] = new_status
        print(f"Equipment '{equipment}' in {hall} updated to '{new_status}'.\n")

    except ValueError as e:
        print(f"Error: {e}\n")
    except Exception:
        print("Unexpected error occurred while updating equipment!\n")


# Main Menu
def main():
    while True:
        print("=== Technician Management Menu ===")
        print("1. View Upcoming Screenings")
        print("2. Report Technical Issue")
        print("3. Confirm Equipment Readiness")
        print("4. Mark Equipment Status")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_schedules()
        elif choice == "2":
            report_issue()
        elif choice == "3":
            comfirm_readiness()
        elif choice == "4":
            mark_equipment()
        elif choice == "5":
            print("Exiting Technician System. Goodbye!")
            break
        else:
            print("Invalid choice. Try again!\n")


if __name__ == "__main__":
    main()