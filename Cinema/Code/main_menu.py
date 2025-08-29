# from ticketing_clerk import *
# from cinema_manager import *
# from technician import *
# from customer import *

def generate_seat_ids():
    rows = "ABCDEFGHIJKLMN"
    with open("Cinema/Database/auditorium_info.txt","r") as f:
        next(f)
        for line in f:
            entry = [i.strip() for i in line.strip().split(",")]
            auditorium_id = entry[0]
            for i in range(int(entry[3]) + 1):
                row = rows[i]
                for j in range(1, (int(entry[4]) + 1)):
                    column = j
                    seat_id = f'SEAT-{row}{column:02}' 
                    with open("Cinema/Database/auditorium_sitting.txt", "a") as g:
                        seat = [seat_id, auditorium_id, f'{i:02}', f'{j:02}']
                        g.write(", ".join(seat) + "\n")

generate_seat_ids()