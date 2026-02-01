import sqlite3

# create exceptions
class UserAlreadyExists(Exception):
    pass
class DuplicateEmail(Exception):
    pass
class UserNotFound(Exception):
    pass
class InvalidCredentials(Exception):
    pass

# Database connection
class Database:
    connection = sqlite3.connect("DAS.db")
    cursor = connection.cursor()

    # Create User Table
    cursor.execute("""CREATE TABLE IF NOT EXISTS usertable (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,phone TEXT, address TEXT,password TEXT NOT NULL)""")

    # Create Login Table
    cursor.execute("""CREATE TABLE IF NOT EXISTS logintable ( email TEXT PRIMARY KEY, password TEXT NOT NULL)""")
    connection.commit()
    connection.close()

# database connection function
def get_connection():
    return sqlite3.connect("DAS.db")

# register function
def register():
    connection = get_connection()
    cursor = connection.cursor()
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    address = input("Enter Address: ")
    password = input("Enter Password: ")
    cursor.execute("SELECT email FROM usertable WHERE email = ?",(email,))
    if cursor.fetchone():
        connection.close()
        raise DuplicateEmail("Email already exists")

    cursor.execute("""INSERT INTO usertable(name,email,phone,address,password) VALUES(?,?,?,?,?)
                    """,(name, email, phone, address, password))

    cursor.execute("INSERT INTO logintable(email,password) VALUES(?,?)",(email, password))
    connection.commit()
    connection.close()
    print(" Registration successful")

# login function
def login():
    connection = get_connection()
    cursor = connection.cursor()
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    cursor.execute("SELECT password FROM logintable WHERE email = ?",(email,))
    data = cursor.fetchone()
    connection.close()
    if not data:
        raise UserNotFound("User not found")
    if data[0] != password:
        raise InvalidCredentials("Invalid email or password")
    print("Login successfully")

# search function
def search():
    connection = get_connection()
    cursor = connection.cursor()
    email = input("Enter Email to search: ")
    cursor.execute(" SELECT name,email,phone,address  FROM usertable WHERE email = ? ", (email,))
    user = cursor.fetchone()
    connection.close()
    if not user:
        raise UserNotFound("User does not exist")
    print("\n   User Details   ")
    print("Name   :", user[0])
    print("Email  :", user[1])
    print("Phone  :", user[2])
    print("Address:", user[3])

# Exit function
def exit_program():
    print("Exit program successfully")

# Main method
if __name__  == "__main__":
    while True:
        print("\n    Dynamic Authentication System    ")
        print("1.Register")
        print("2.Login")
        print("3.Search User")
        print("4.Exit")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                register()
            elif choice == "2":
                login()
            elif choice == "3":
                search()
            elif choice == "4":
                exit_program()
                break
            else:
                print(" Invalid choice")
        except Exception as e:
            print(" Error:",e)

