# Year-1-Sem-1-Python-Cinema-Assignment

## User roles

#### Ticketing Clerk
- Book tickets for walk-in customers.
- Cancel or modify existing bookings.
- View seating availability and screening details.
- Process payments and generate receipts.

#### Cinema Manager
- Add, update, or remove movie listings.
- Create and manage showtime schedules (movie, auditorium, time).
- Set ticket prices and apply discount policies.
- View overall booking reports and revenue summaries.

#### Technician
- View upcoming movie screening schedules.
- Report technical issues (projector, sound, air conditioner) by the auditorium.
- Confirm readiness of screening equipment.
- Mark equipment as under maintenance or resolved.

#### Customer
- Register and update personal account details.
- View currently showing and upcoming movies.
- Book or cancel tickets for available shows.
- Access booking history and seat information.


## Setting up

### 1. Download Git
Link: https://git-scm.com/

### 2. Setting up user account
in VS Code terminal, run:
    git --version

    git config --global user.name "username" (GitHub username)

    git config --global user.email "email" (GitHub email account)

### 3. Clone remote repository onto local machine
open Command Palette and type "Git: Clone" then paste:
    https://github.com/wolf047/Year-1-Sem-1-Python-Cinema-Assignment.git
then choose a folder to save the repository in

### 4. Common commands
- git checkout -b <branch_name> (create branch and switch to it)
- git checkout <branch_name> (switch branches)
- git add <filenames> (add files to be committed; use . to add all, or list names separated by comma) 
- git commit (save work locally; add description)
- git push <remote> <branch> (usually git push origin main, or git push origin <branch_name>; uploads your committed edits)
- git pull <remote> <branch> (usually git push origin main; downloads remote copy to your local location)
-- git merge <branch_to_be_merged> (merge specified branch to the branch that you are currently in)

#### Beginning:
    git checkout -b something

#### After completing your work:
    git add something
    git commit
    git push origin something

#### To download others' work:
    git pull origin main


