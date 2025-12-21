import sys
from app import *
from werkzeug.security import generate_password_hash, check_password_hash

try:
    add_user = sys.argv[1]
except IndexError:
    add_user = "blahblahblahblah"

if add_user == "add_user":
    print("Ticket System: Add user")
    print("-----------------------")
    username = str(input("Name: "))
    password = str(input("Password: "))
    repassword = input("Re-enter password:  ")
    if password != repassword:
        print("-----------------------------------------")
        print("It looks like your passwords don't match.")
        print("Please try running this program again.")
    with app.app_context():
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            print("ERROR: A user with that name already exists. Please try again.")
            exit(   )
        a = User(username=username, password=generate_password_hash(password))
        db.session.add(a)
        db.session.commit()
    exit()

print("Ticket System: Welcome to scripts.py!")
print("-------------------------------------")
print("")
print("This is a program with scripts for the program.")
print("To add a user, in the terminal, run:")
print("python scripts.py add_user")
print("-------------------------------------")
print("Goodbye!")