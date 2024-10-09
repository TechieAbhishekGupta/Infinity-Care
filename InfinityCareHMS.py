from sys import exit

import mysql.connector as sql


def main():
    """The main entry point for the program,
    Main function to interact with the hospital management system and to control the program flow, coordinating connection, login, and menu flow.
    """

    print("\n************************************************")
    print("    INFINITY CARE HOSPITAL MANAGEMENT SYSTEM")
    print("************************************************\n")

    while True:
        print("1. LOGIN")
        print("2. EXIT")

        try:
            login_choice = int(input("\nENTER YOUR CHOICE (1-2): "))

            if login_choice == 1:
                if handle_login():
                    db_connection, my_cursor = connect_to_database()

                    handle_welcome_menu(db_connection, my_cursor)

            elif login_choice == 2:
                print("\nExiting login window...\n")
                break

            else:
                print("\nInvalid choice. Please enter 1 for LOGIN or 2 for EXIT.\n")

        except ValueError:
            print("\nInvalid input. Please enter a valid number.\n")


def handle_login():
    """
    Performs user login for authorized access to the system.

    Returns:
        True if login is successful, False otherwise.
    """
    while True:
        UserName = input("\nEnter User Name: ")
        Password = input("Enter the Password: ")

        if UserName == "queen_Khushi" and Password == "queen#0258#":
            print("\nLogin Successful!\n")
            return True
        else:
            print("\nWrong UserName & Password !\n")
            print("Try Again...\n")
            return False


def connect_to_database():
    """
    Establishes a connection to the Infinity Care Hospital Management System database.

    Returns: A tuple containing the established database connection and cursor object.
        connection (mysql.connector.connection): Database connection object.
        cursor (mysql.connector.cursor): Database cursor object.
    """
    try:
        connection = sql.connect(
            host="localhost",
            database="infinity_care_hms_db",
            user="root",
            password="queen#0258#",
        )
        cursor = connection.cursor()

        if connection.is_connected():
            print("\nDataBase Connected Successfully...")
            return connection, cursor

    except sql.Error as error:
        print(f"\nDatabase connection failed: {error}")
        exit()


def handle_welcome_menu(db_connection, my_cursor):
    """
    Presents the main system menu and handles user interaction with its options.

    Args:
        db_connection: The established database connection.
        my_cursor: The active database cursor object.
    """

    print("\n - WELCOME TO INFINITY CARE HOSPITAL -")
    print("---------------------------------------\n")
    print("1. Registering Patient Detail")
    print("2. Registering Doctor Details")
    print("3. Registering Worker Details")
    print("4. All Patient Details")
    print("5. All Doctor Details")
    print("6. All Worker details")
    print("7. Patient Detail")
    print("8. Doctor Detail")
    print("9. Worker Detail")
    print("10. Exit")

    while True:
        try:
            choice = int(input("\nENTER YOUR CHOICE (1-10): "))

            # Get patient details and insert into database
            if choice == 1:
                print("Registering Patient Details")
                patient_name = input("\nEnter Patient Name: ")
                patient_age = int(input("Enter Age: "))
                patient_problems = input("Enter the Problem/Disease: ")
                patient_phono = int(input("Enter Phone number: "))

                insert_record(
                    "patient_details",
                    [
                        "patient_Name",
                        "patient_Age",
                        "patient_Disease",
                        "patient_PhoneNo",
                    ],
                    (
                        patient_name,
                        str(patient_age),
                        patient_problems,
                        str(patient_phono),
                    ),
                    my_cursor,
                    db_connection,
                )

            # Get doctor details and insert into database
            elif choice == 2:
                print("Registering Doctor Details")
                doctor_name = input("\nEnter Doctor Name: ")
                doctor_age = int(input("Enter Doctor Age: "))
                doctor_specialist = input("Enter Doctor Specialization: ")
                doctor_phono = int(input("Enter Doctor Phone number: "))

                insert_record(
                    "doctor_details ",
                    [
                        "doctor_Name",
                        "doctor_Age",
                        "doctor_Specialist",
                        "doctor_PhoneNo",
                    ],
                    (
                        doctor_name,
                        str(doctor_age),
                        doctor_specialist,
                        str(doctor_phono),
                    ),
                    my_cursor,
                    db_connection,
                )

            # Get worker details and insert into database
            elif choice == 3:
                print("Registering Worker Details")
                worker_name = input("\nEnter Worker Name: ")
                worker_age = int(input("Enter Age: "))
                worker_work_name = input("Enter type of work: ")
                worker_phono = int(input("Enter Phone number: "))

                insert_record(
                    "worker_details",
                    [
                        "worker_Name",
                        "worker_Age",
                        "worker_Work_Name",
                        "worker_PhoneNo",
                    ],
                    (
                        worker_name,
                        str(worker_age),
                        worker_work_name,
                        str(worker_phono),
                    ),
                    my_cursor,
                    db_connection,
                )

            # Display all patient details
            elif choice == 4:
                print("Displaying All Patient Details")
                display_records("patient_details", my_cursor)

            # Display all doctor details
            elif choice == 5:
                print("Displaying All Doctor Details")
                display_records("doctor_details", my_cursor)

            # Display all worker details
            elif choice == 6:
                print("Displaying All Worker Details")
                display_records("worker_details", my_cursor)

            # Search for a specific patient record
            elif choice == 7:
                print("Searching for Patient Detail")
                # Get patient name input
                patient_Name = input("Enter Name of Patient: ")
                search_record(
                    "patient_details", "patient_Name", patient_Name, my_cursor
                )

            # Search for a specific doctor record
            elif choice == 8:
                print("Searching for Doctor Detail")
                # Get doctor name input
                doctor_Name = input("Enter Name of Doctor: ")
                search_record("doctor_details", "doctor_Name", doctor_Name, my_cursor)

            # Search for a specific worker record
            elif choice == 9:
                print("Searching for Worker Detail")
                # Get worker name input
                worker_Name = input("Enter Name of Worker: ")
                search_record("worker_details", "worker_Name", worker_Name, my_cursor)

            # Close database connection and exit
            elif choice == 10:
                print("Exiting welcome window...")
                close_database_connection(my_cursor, db_connection)
                break  # Exit the loop

            else:
                print("Invalid choice. Please enter a number between 1 and 10.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def insert_record(table_name, columns, values, cursor, connection):
    """
    Insert a record into the specified table.

    Args:
        table_name (str): Name of the table to insert the record into.
        columns (list): List of column names.
        values (tuple): Tuple of values to be inserted into the corresponding columns.
        cursor (mysql.connector.cursor): Database cursor object.
        connection (mysql.connector.connection): Database connection object.
    """
    try:
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))})"

        cursor.execute(query, values)

        connection.commit()

        print(f"\nRecord inserted successfully into {table_name} table.")

        print(f"{cursor.rowcount} tuple was inserted. ID: {cursor.lastrowid}")

    except sql.Error as error:
        print(f"Parameterized query failed: {error}")


def display_records(table_name, cursor):
    """
    Display all records from the specified table.

    Args:
        table_name (str): Name of the table to fetch records from.
        cursor (mysql.connector.cursor): Database cursor object.
    """
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        print(record)


def search_record(table_name, search_column, search_value, cursor):
    """
    Search for records in the specified table based on a given column and value.

    Args:
        table_name (str): Name of the table to search records in.
        search_column (str): Column to search for the specified value.
        search_value (str): Value to search for in the specified column.
        cursor (mysql.connector.cursor): Database cursor object.
    """
    query = f"SELECT * FROM {table_name} WHERE {search_column} LIKE %s"
    cursor.execute(query, ("%" + search_value + "%",))
    records = cursor.fetchall()
    if records:
        for record in records:
            print(record)

    else:
        print(f"No {search_column} found with that {table_name}.")


def close_database_connection(cursor, connection):
    """
    Close the cursor and database connection.

    Args:
        cursor (mysql.connector.cursor): Database cursor object.
        connection (mysql.connector.connection): Database connection object.
    """
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed.\n")


if __name__ == "__main__":
    main()
