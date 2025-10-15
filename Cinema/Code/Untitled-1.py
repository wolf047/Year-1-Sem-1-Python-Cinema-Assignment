def load_issues(filename="Cinema/Database/technician_issues.txt"):
    issues = {}
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
            print("LOAD:", issues)

load_issues()