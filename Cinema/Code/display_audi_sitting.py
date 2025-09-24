with open("Cinema\Database\movie_showtimes.txt", "r") as f:
    if header:
        details = [detail.strip() for detail in f.readline().split(",")]
        return details
    for line in f:
        entry = [i.strip() for i in line.split(",")]
        if entry[0] == "ST001":
            return entry

auditorium_id = entry[2]

with open("Cinema/Database/auditorium_sitting.txt", "r") as g:
    entries = g.readlines()
    for line in entries:
        if line == auditorium_id:
            while line != "":
                sitting = 
