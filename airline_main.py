import bcrypt
from AirAsiaCsvIO import CsvToDB, CsvToDBWithEncryption, DbToCSV
from AirAsia import AirAsiaDatabase
from datetime import date, datetime

class Customer(AirAsiaDatabase): #This class contains all the CRUD methods for the Customer table
    #This will be the method for adding
    def add_customer_info(self, first_name, last_name, dob, citizenship, email, username, password): #These are the possible values that can be added for each customer profile
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            super().get_cursor.execute("""
            INSERT INTO Customer (first_name, last_name, dob, citizenship, email, username, password) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (first_name, last_name, dob, citizenship, email, username, hashed_password))
            super().get_connection.commit()
            print(f"The customer {first_name} {last_name} was added to the database")
        except Exception as e:
            print("There was an error adding in this new customer")
            print("The specific error adding the customer was:", e)

    #This method will update customer information based on the provided username
    def update_customer_info(self, first_name, last_name, dob, citizenship, email, username):
        try:
            super().get_cursor.execute("""UPDATE Customer SET first_name = ?, last_name = ?, dob = ?, citizenship = ?, email = ? WHERE username = ?;
            """, (first_name, last_name, dob, citizenship, email, username))
            super().get_connection.commit()
            print(f"The customer information for customer {username} was successfully updated") #Every method will include a successful print statement since its easier to tell if it worked or not with one
            return True
        except Exception as e: #All the exceptions will follow the same general format as the add method
            print("There was an error updating the customer information")
            print("The specific error updating the customer was:", e)
            return False

    #This method deletes the customer based off of the provided username
    def delete_customer(self, username):
        try:
            super().get_cursor.execute("""DELETE FROM Customer WHERE username =?;
            """, (username,))
            super().get_connection.commit()
            print(f"The customer {username} was successfully deleted from the database")
        except Exception as e:
            print("There was an error deleting the customer entry")
            print("The specific error was:", e)

    #This method will retrieve customer information by customer_id
    def retrieve_customer_information(self, username = None):
        try:
            if username is not None:
                retval = super().get_cursor.execute("""SELECT first_name, last_name, dob, citizenship, email FROM Customer WHERE username = ?
                """, (username,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute("""SELECT first_name, last_name, dob, citizenship, email FROM Customer""").fetchall()
        except Exception as e:
            print("There was an error retrieving customer information")
            print("The specific error retrieving customer information:", e)

    def getAllCustomers(self):
        # returns customer details based on an username.
        try:
            print('inside')
            sql = "SELECT * FROM Customer ;"
            super().get_cursor.execute(sql)
            result = super().get_cursor.fetchall()
            print(result)
            return result
        except Exception as e:
            print("Error in getCustomer block:", e)

    def verifyCustomerAuthentication(self, username, password):
        try:
            print(f"Verifying authentication for username: {username}")
            sql = "SELECT * FROM Customer WHERE username = ?;"
            super().get_cursor.execute(sql, (username,))
            user_data = super().get_cursor.fetchone()
            print(user_data)
            if not user_data:
                print("User not found")
                return False

            stored_hash_hex = user_data[7] # Store the hexadecimal hash string
            print("Stored hash (hex) found for user:", stored_hash_hex)
            # Convert the stored hash to bytes if it's not already
            if isinstance(stored_hash_hex, str):
                stored_hash_hex = stored_hash_hex.encode('utf-8')
            result = bcrypt.checkpw(password.encode('utf-8'), stored_hash_hex)
            print(f"Authentication result: {result}")
            return result

        except Exception as e:
            print(f"Error in authentication: {e}")
        return False        

class Airport(AirAsiaDatabase): #This class will contain all the CRUD methods for airports
    #The method to add and create new airport entries
    def add_airport(self, airport_code, airport_name, city, country):
        try:
            super().get_cursor.execute(
                """INSERT INTO Airport (airport_code, airport_name, city, country) VALUES (?, ?, ?, ?);""", (airport_code, airport_name, city, country))
            super().get_connection.commit()
            print(f"The new airport of {airport_name} was successfully added to Air Asia's Database")
        except Exception as e:
            print("There was an error adding a new airport")
            print("The specific error adding a new airport was:", e)

    #The method for updating airport information
    def update_airport(self, airport_code, airport_name, city, country):
        try:
            super().get_cursor.execute("""UPDATE Airport SET airport_name = ?, city = ?, country = ? WHERE airport_code = ?;""",
                                       (airport_name, city, country, airport_code))
            super().get_connection.commit()
            print(f"The information for airport #{airport_name} was successfully updated")
        except Exception as e:
            print("There was an error updating the airport information")
            print("The specific error updating airport information was:", e)

    #The method for deleting airports based on airport_code provided
    def delete_airport(self, airport_code):
        try:
            super().get_cursor.execute("""DELETE FROM Airport WHERE airport_code =?;
                        """, (airport_code,))
            super().get_connection.commit()
            print(f"The airport #{airport_code} was successfully deleted from the database")
        except Exception as e:
            print("There was an error deleting the customer entry")
            print("The specific error was:", e)

    #This method will retrieve airport information by airport_code
    def retrieve_airport_information(self, airport_code = None):
        try:
            if airport_code is not None:
                retval = super().get_cursor.execute("""SELECT airport_code, airport_name, city, country FROM Airport WHERE airport_code = ?
                """, (airport_code,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute("""SELECT airport_code, airport_name, city, country FROM Airport""").fetchall()
        except Exception as e:
            print("There was an error retrieving airport information")
            print("The specific error retrieving airport information:", e)

    def getAllAirports(self):
        # returns airport details based on an airportCode.
        try:
            sql = "SELECT * FROM Airport;"
            super().get_cursor.execute(sql)
            result = super().get_cursor.fetchall()
            return result
        except Exception as e:
            print("Error in getAllAirport block:", e)

class Ticket(AirAsiaDatabase):#This class will contain all the CRUD methods for tickets
    #The method to add and create new ticket entries

    def addTicket(self, username, flightID, cost, purchaseDate):
        # Adds a new Ticket to the database.
        self.username = username
        self.flightID = flightID
        self.purchaseDate = purchaseDate
        
        try: 
            sql = "INSERT INTO Ticket(customer_id, flight_id, cost, purchase_date) VALUES (?, ?, ?, ?);"
            super().get_cursor().execute(sql, (username, flightID, cost, purchaseDate))
            super().get_conn.commit()
            print("Ticket is booked succesfully.")
        except Exception as e:
            print("Error in addTicket block::", e)
    
    def updateTicket(self, ticketNum, flightID, purchaseDate):
        # updates ticketdetails based on its ticket_num.
        try:
            sql = "UPDATE Ticket SET customer_id = ?, flight_id = ?, cost = ?, purchase_date = ?  WHERE ticket_num = ?;" 
            super().get_cursor.execute(sql, (flightID, purchaseDate, ticketNum))
            super().get_conn.commit()
            print("ticket details are updated succesfully.")
        except Exception as e:
            print("Error in updateTicket block: ", e)

    def deleteTicket(self, ticketNum):
        # deletes a ticket from the database based on the ticket_num.
        try: 
            sql = "DELETE FROM Ticket WHERE ticket_num = ?;" 
            super().get_cursor.execute(sql, (ticketNum,))
            super().get_conn.commit()
            print("Ticket is deleted succesfully.")
        except Exception as e:
            print("Error in deleteTicket block:", e)
    
    def getTicket(self, ticketNum):
        # returns ticket details based on a ticket_num.
        try:
            sql = "SELECT * FROM Ticket WHERE ticket_num = ?;"
            super().get_cursor.execute(sql, (ticketNum,))
            result = super().get_cursor.fetchall()
            return result
        except Exception as e:
            print("Error in getTicket block:", e)

    def getAllTickets(self):
        # returns ticket details based on a ticket_num.
        try:
            sql = "SELECT * FROM Ticket ;"
            super().get_cursor.execute(sql)
            result = super().get_cursor.fetchall()
            return result
        except Exception as e:
            print("Error in getTicket block:", e)        
            
#Employee CRUD Operations
class Employee(AirAsiaDatabase): #This class contains all the CRUD methods for the Employee table
    #This will be the method for adding

    def add_employee_info(self, first_name, last_name, job_title, flight_id, username, password): #These are the possible values that can be added for each employee profile
        try:
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            super().get_cursor.execute("""
            INSERT INTO Employee (first_name, last_name, job_title, flight_id, username, password) VALUES (?, ?, ?, ?, ?, ?);
            """, (first_name, last_name, job_title, flight_id, username, hashed_password))
            super().get_connection.commit()
            print(f"The employee {first_name} {last_name} was added to the database")
        except Exception as e:
            print("There was an error adding in this new employee")
            print("The specific error adding the employee was:", e)




    #This method will update employee information based on the provided employee_ID
    def update_employee_info(self, first_name, last_name, job_title, flight_id, username):
        try:
            super().get_cursor.execute("""UPDATE Employee SET first_name = ?, last_name = ?, job_title = ?, flight_id = ? WHERE username = ?;
            """, (first_name, last_name, job_title, flight_id, username))
            super().get_connection.commit()
            print(f"The employee information for employee {username} was successfully updated") #Every method will include a successful print statement since its easier to tell if it worked or not with one
            return True
        except Exception as e: #All the exceptions will follow the same general format as the add method
            print("There was an error updating the employee information")
            print("The specific error updating the employee was:", e)
            return False



    #This method deletes the employee based off of the provided employee_id
    def delete_employee(self, username):
        try:
            super().get_cursor.execute("""DELETE FROM Employee WHERE username =?;
            """, (username,))
            super().get_connection.commit()
            print(f"The employee {username} was successfully deleted from the database")
        except Exception as e:
            print("There was an error deleting the employee entry")
            print("The specific error was:", e)

    #This method will retrieve employee information by employee_id
    def retrieve_employee_information(self, username = None):
        try:
            if username is not None:
                retval = super().get_cursor.execute("""SELECT first_name, last_name, job_title, flight_id  FROM Employee WHERE username = ?
                """, (username,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute("""SELECT first_name, last_name, job_title, flight_id FROM Employee""").fetchall()
        except Exception as e:
            print("There was an error retrieving employee information")
            print("The specific error retrieving employee information:", e)

    def getAllEmployees(self):
        # returns employee details based on username.
        try:
            print('inside')
            sql = "SELECT * FROM Employee ;"
            super().get_cursor.execute(sql)
            result = super().get_cursor.fetchall()
            print(result)
            return result
        except Exception as e:
            print("Error in getEmployee block:", e)

    def get_employee_job_title(self, username):
        try:
            if username is not None:
                title = super().get_cursor.execute("""Select job_title FROM Employee WHERE username =?;
                """, (username,)).fetchone()
                print('title', title)
                return title[0] if title else None
            else:
                return super().get_cursor.execute("""SELECT first_name, last_name, job_title, flight_id FROM Employee""").fetchall()
        except Exception as e:
            print("There was an error retrieving the employee entry", e)

    def verifyEmployeeAuthentication(self, username, password):
        try:
            print(f"Verifying authentication for username: {username}")
            sql = "SELECT * FROM Employee WHERE username = ?;"
            super().get_cursor.execute(sql, (username,))
            user_data = super().get_cursor.fetchone()
            print(user_data)
            if not user_data:
                print("User not found")
                return False

            stored_hash_hex = user_data[6] # Store the hexadecimal hash string
            print("Stored hash (hex) found for user:", stored_hash_hex)
            # Convert the stored hash to bytes if it's not already
            if isinstance(stored_hash_hex, str):
                stored_hash_hex = stored_hash_hex.encode('utf-8')
            result = bcrypt.checkpw(password.encode('utf-8'), stored_hash_hex)
            print(f"Authentication result: {result}")
            return result

        except Exception as e:
            print(f"Error in authentication: {e}")
        return False 

#Flight CRUD Operations

class Flight(AirAsiaDatabase):  # This class contains all the CRUD methods for the Flights table
    # This will be the method for adding
    def add_flights_info(self, airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs):  # These are the possible values that can be added for each flight profile
        try:
            super().get_cursor.execute("""
            INSERT INTO Flight (airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?);
            """, (airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs))
            super().get_connection.commit()
            print(f"The flights {departure_date} {departure_gate} was added to the database")
        except Exception as e:
            print("There was an error adding in this new flights")
            print("The specific error adding the flight was:", e)



    # This method will update flights information based on the provided flight_ID
    def update_flight_info(self, airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs, flight_id):
        try:
            super().get_cursor.execute("""UPDATE Flight SET airportFrom = ?, airportTo = ?, aircraftType = ?, departure_date = ?, time = ?, departure_gate = ?, arrival_gate = ?, duration_in_hrs = ? WHERE flight_id = ?;
            """, (airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs, flight_id))
            super().get_connection.commit()
            print(
                f"The flight information for flight {flight_id} was successfully updated")  # Every method will include a successful print statement since its easier to tell if it worked or not with one
            return True
        except Exception as e:  # All the exceptions will follow the same general format as the add method
            print("There was an error updating the flight information")
            print("The specific error updating the flight was:", e)
            return False



    # This method deletes the flight based off of the provided flight_id
    def delete_flight(self, flight_id):
        try:
            super().get_cursor.execute("""DELETE FROM Flight WHERE flight_id =?;
            """, (flight_id,))
            super().get_connection.commit()
            print(f"The flight {flight_id} was successfully deleted from the database")
        except Exception as e:
            print("There was an error deleting the flight entry")
            print("The specific error was:", e)



    # This method will retrieve flight information by flight_id
    def retrieve_flight_information(self, flight_id):
        try:
            if flight_id is not None:
                retval = super().get_cursor.execute("""SELECT airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs FROM Flight WHERE flight_id = ?
                """, (flight_id,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute(
                    """SELECT airportFrom, airportTo, aircraftType, departure_date, time, departure_gate, arrival_gate, duration_in_hrs FROM Flight""").fetchall()
        except Exception as e:
            print("There was an error retrieving flight information")
            print("The specific error retrieving flight information:", e)

    def getAllFlights(self):
        # returns flight details based on an username.
        try:
            print('inside')
            sql = "SELECT * FROM Flight;"
            super().get_cursor.execute(sql)
            result = super().get_cursor.fetchall()
            print(result)
            return result
        except Exception as e:
            print("Error in getFlight block:", e)



class AirlineMain(Customer, Airport, Employee, Flight):

    def __init__(self):
        super().__init__()

    def updateAirportWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv) - eg : airport.csv: "))
            newCSV = CsvToDB(fileName, "airasiadb.sqlite", "Airport")
            newCSV.run()
        except Exception as e:
            print("Error while updating Airport with CSV: ", e)

    def updateTicketWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv) - eg : tickets.csv: "))
            newCSV = CsvToDB(fileName, "airasiadb.sqlite", "Ticket")
            newCSV.run()
        except Exception as e:
            print("Error while updating Airport with CSV: ", e)

    def updateFlightWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv)- eg : flights.csv: "))
            newCSV = CsvToDB(fileName, "airasiadb.sqlite", "Flight")
            newCSV.run()
        except Exception as e:
            print("Error while updating Flight with CSV: ", e)

    def updateCustomerWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv)- eg : customer.csv: "))
            newCSV = CsvToDBWithEncryption(fileName, "airasiadb.sqlite","Customer", "password")
            newCSV.run()
        except Exception as e:
            print("Error while updating Customer with CSV: ", e)

    def updateEmployeeWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv)- eg : employee.csv: "))
            newCSV = CsvToDBWithEncryption(fileName, "airasiadb.sqlite","Employee", "password")
            newCSV.run()
        except Exception as e:
            print("Error while updating Employee with CSV: ", e)

class UserAuthentication:
    def user_authentication(self):
        while True:
            try:
                print("\nWelcome to Airline Ticketing System")
                val = int(input("Please enter a number to proceed:\n1. Login\n2. Signup\n3. Exit\n"))
                
                if val == 1:
                    self.user_signin()
                elif val == 2:
                    self.user_signup()
                elif val == 3:
                    print("Thank you for using our system!")
                    exit()
                else:
                    print("Invalid Entry. Please try again.")
            except ValueError:
                print("Invalid Input. Please enter a number again.")
            except Exception as e:
                print(f"Error: {e}")

    def user_signin(self):
        user_type = self.get_user_type()
        if user_type == 'customer':
            self.customer_signin()
        elif user_type == 'employee':
            self.employee_signin()
        elif user_type == 'admin':
            self.admin_signin()

    def user_signup(self):
        user_type = self.get_user_type()
        if user_type == 'customer':
            self.customer_signup()
        elif user_type == 'employee':
            self.employee_signup()
        elif user_type == 'admin':
            print("Admin accounts cannot be created through signup. Please contact system administrator.")

    def get_user_type(self):
        while True:
            user_type = input("User type (customer/employee/admin): ").lower()
            if user_type in ['customer', 'employee', 'admin']:
                return user_type
            print("Invalid user type. Please enter 'customer', 'employee', or 'admin'.")

    def customer_signin(self):
        username = input("Username: ")
        password = input("Password: ")
        customer = Customer()
        if customer.verifyCustomerAuthentication(username, password):
            print("Customer Authentication Successful.")
            self.customer_user_actions()
        else:
            print("Authentication Failed. Please try again.")

    def employee_signin(self):
        username = input("Username: ")
        password = input("Password: ")
        employee = Employee()
        if employee.verifyEmployeeAuthentication(username, password):
            print("Employee Authentication Successful.")
            self.employee_user_actions()
        else:
            print("Authentication Failed. Please try again.")

    def admin_signin(self):
        username = input("Username: ")
        password = input("Password: ")
        employee = Employee()
        if employee.verifyEmployeeAuthentication(username, password):
            job_title = employee.get_employee_job_title(username)
            if job_title.lower() == 'admin':
                print("Admin Authentication Successful.")
                self.admin_user_actions()
            else:
                print("Authentication Failed. User is not an admin.")
        else:
            print("Authentication Failed. Please try again.")

    def customer_signup(self):
        print("Please enter following details to sign up:")
        
        username = input("Username: ")
        password = input("Password: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        dob = self.get_date_input("Date of Birth (YYYY-MM-DD): ")
        citizenship = input("Citizenship: ")
        email = input("Email: ")
        
        test = Customer()
        print('customer', test)
        test.add_customer_info(first_name, last_name, dob, citizenship, email, username, password)
        print("Signup successful. Please sign in to proceed.")

    def employee_signup(self):
        print("Please enter following details to sign up:")
        username = input("Username: ")
        password = input("Password: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        job_title = input("Job Title: ")
        flight_id = input("Flight ID: ")

        employee = Employee()
        employee.add_employee_info(first_name, last_name, job_title, flight_id, username, password)
        print("Signup successful. Please sign in to proceed.")

    def get_date_input(self, prompt):
        while True:
            date_str = input(prompt)
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def customer_user_actions(self):
        print("Customer actions menu")
        # Implement customer actions here

    def employee_user_actions(self):
        print("Employee actions menu")
        # Implement employee actions here

    # user admin functions
    def updateCustomer(self): #same as modify customer
        try:
            print("Please enter customer details to update:")
            self.username = str(input("Username: "))
            self.firstName = str(input("First Name: "))
            self.lastName = str(input("Last Name: "))
            dateComponents = input('Date of Birth (YYYY-MM-DD): ').split('-')
            year, month, day = [int(item) for item in dateComponents]
            self.dob = date(year, month, day)
            self.citizenship = str(input("Citizenship: "))
            self.email = str(input("Email: "))
            customer = Customer()
            customer.update_customer_info(self.firstName, self.lastName, self.dob, self.citizenship, self.email, self.username)
        except Exception as e:
            print("Error in update profile block: ", e)

    def delete_customer(self):
        try:
            customer = Customer()
            customer.delete_customer(str(input("Enter username to delete the customer: ")))
        except Exception as e:
            print("Error in delete_customer method: ", e)
            self.admin_user_actions()

    def retrieve_customer(self):
        try:
            customer = Customer()
            info = customer.retrieve_customer_information(str(input("Enter username to retrieve the customer: ")))
            print('Customer details are:', info)
        except Exception as e:
            print("Error in delete_customer method: ", e)
            self.admin_user_actions()

    #below ticket fucntions to be added by Leyna
    def book_ticket(self):
        try:
            pass
        except Exception as e:
            pass
    
    def modify_ticket(self):
        try:
            pass
        except Exception as e:
            pass
    
    def cancel_ticket(self):
        try:
            pass
        except Exception as e:
            pass

    def retrieve_ticket(self):
        try:
            pass
        except Exception as e:
            pass    
    
    def add_airport(self):
        try:
            airport_code = str(input("Enter Airport Code (Ex: DFW): "))
            airport_name = str(input("Enter Airport Name (Ex: Salt Lake City Intl Airport): "))
            airport_city = str(input("Enter Airport City: "))
            airport_country = str(input("Enter Airport Country: "))
            airport = Airport()
            airport.add_airport(airport_code, airport_name, airport_city, airport_country)
        except Exception as e:
            print("Error while adding airport: ", e)
            self.admin_user_actions()
    
    def update_airport(self):
        try:
            airport_code = str(input("Enter Airport Code (Ex: DFW): "))
            airport_name = str(input("Enter Airport Name (Ex: Salt Lake City Intl Airport): "))
            airport_city = str(input("Enter Airport City: "))
            airport_country = str(input("Enter Airport Country: "))
            airport = Airport()
            airport.update_airport(airport_code, airport_name, airport_city, airport_country)
        except Exception as e:
            print("Error while updating airport: ", e)
            self.admin_user_actions()
    
    def delete_airport(self):
        try:
            airport_code = str(input("Enter Airport Code (Ex: DFW): "))
            airport = Airport()
            airport.delete_airport(airport_code)
        except Exception as e:
            print("Error while updating airport: ", e)
            self.admin_user_actions()

    def retrieve_airport(self):
        try:
            airport_code = str(input("Enter Airport Code (Ex: DFW): "))
            airport = Airport()
            info = airport.retrieve_airport_information(airport_code)
            print('Airport details are: ', info)
        except Exception as e:
            print("Error while updating airport: ", e)
            self.admin_user_actions()        
    
    def add_flight(self):
        try:
            print("Please enter the following details: ")
            airportFrom = str(input("Departure Airport: "))
            airportTo = str(input("Destination Airport: "))
            aircraftType = (input("Aircraft Type: "))
            dateComponents = input('Departure Date: (YYYY-MM-DD): ').split('-')
            year, month, day = [int(item) for item in dateComponents]
            departureDate = date(year, month, day)
            departureTime = str(input("Departure Time: "))
            departureGate = str(input("Departure Gate: "))
            arrivalGate = str(input("Arrival Gate: "))
            duration = str(input("Flight Duration: "))
            Flight().add_flights_info(airportFrom, airportTo, aircraftType, departureDate, departureTime, departureGate, arrivalGate, duration)
        except Exception as e:
            print("Error while updating flight: ", e)
            self.adminActions()
    
    def update_flight(self):
        try:
            print("Please enter the following details: ")
            airportFrom = str(input("Departure Airport: "))
            airportTo = str(input("Destination Airport: "))
            aircraftType = (input("Aircraft Type: "))
            dateComponents = input('Departure Date: (YYYY-MM-DD): ').split('-')
            year, month, day = [int(item) for item in dateComponents]
            departureDate = date(year, month, day)
            departureTime = str(input("Departure Time: "))
            departureGate = str(input("Departure Gate: "))
            arrivalGate = str(input("Arrival Gate: "))
            duration = (input("Flight Duration: "))
            flightID = int(input("FlightID: "))

            Flight().update_flight_info(airportFrom, airportTo, aircraftType, departureDate, departureTime, departureGate, arrivalGate, duration, flightID)
        except Exception as e:
            print("Error while modifying flight: ", e)
            self.adminActions()
    
    def delete_flight(self):
        try:
            print("Please enter the following details: ")
            flightID = int(input("FlightID: "))
            Flight().delete_flight(flightID)
        except Exception as e:
            print("Error while deleting flight: ")

    def retrieve_flight(self):
        try:
            print("Please enter the following details: ")
            flightID = int(input("FlightID: "))
            info = Flight().retrieve_flight_information(flightID)
            print("Flight details are:", info)
        except Exception as e:
            print("Error while deleting flight: ")        

    def update_employee(self):
        try:
            firstName = str(input("Enter Employee First Name: "))
            lastName =  str(input("Enter Employee Last Name: "))
            jobTitle =  str(input("Enter Employee Job Title: "))
            flightID =  int(input("Enter Employee FlightID: "))
            employeeUsername =  str(input("Enter Employee Username: "))

            Employee().update_employee_info(firstName, lastName, jobTitle, flightID, employeeUsername)

        except Exception as e:
            print("Error while updating employee: ", e)
            self.admin_user_actions()
    
    def delete_employee(self):
        try:
            employeeUsername =  str(input("Enter Employee Username: "))
            Employee().delete_employee(employeeUsername)  

        except Exception as e:
            print("Error while deleting employee: ", e)
            self.admin_user_actions()

    def retrieve_employee(self):
        try:
            employeeUsername =  str(input("Enter Employee Username: "))
            info = Employee().retrieve_employee_information(employeeUsername)  
            print("Employee details are:", info)

        except Exception as e:
            print("Error while deleting employee: ", e)
            self.admin_user_actions()

    #below SEARCH fucntion to be added by Leyna

    def search_flight(self):
        try:
            pass
        except Exception as e:
            pass
    
    def generateFlightSalesReport(self):
        reportQuery = """
                        SELECT
                            f.flight_id,
                            f.airportTo,
                            f.departure_date,
                            SUM(t.cost) AS total_revenue,
                            COUNT(t.ticket_num) AS total_tickets_sold,
                            AVG(t.cost) AS average_ticket_price
                        FROM
                            Flight AS f
                        JOIN
                            Ticket AS t ON f.flight_id = t.flight_id
                        GROUP BY
                            f.flight_id, f.airportTo, f.departure_date
                        ORDER BY
                            f.flight_id;
                    """
        
        output = DbToCSV("airasiadb.sqlite", reportQuery, "FlightSaleReport.csv")

        output.writeToCsvFile()

    def generateEmployeeReport(self):
        reportQuery = """
                        SELECT
                            e.employee_id,
                            e.first_name AS employee_first_name,
                            e.last_name AS employee_last_name,
                            e.job_title,
                            f.flight_id,
                            f.airportTo,
                            f.departure_date,
                            f.time
                        FROM
                            Employee AS e
                        JOIN
                            Flight AS f ON e.flight_id = f.flight_id
                        ORDER BY
                            f.flight_id, e.employee_id;
                    """
        
        output = DbToCSV("airasiadb.sqlite", reportQuery, "EmployeeReport.csv")

        output.writeToCsvFile()

    def admin_user_actions(self):
        try:
            print("Welcome to Air Asia!")
            admin_menu_input = UserMenus.adminMenu(self)

            if admin_menu_input == 1: # Add/Modify/Delete a customer
                try:
                    menuInput = int(input("Please select an option from below: \n 1. Add Customer \n 2. Modify Customer \n 3. Delete Customer \n 4. Retrieve Customer \n 5. Back to the main menu \n 6. Exit \n"))
                    if menuInput == 1:
                        self.customer_signup()
                        self.admin_user_actions()
                        
                    elif menuInput == 2:
                        self.updateCustomer()
                        self.admin_user_actions()

                    elif menuInput == 3:
                        self.delete_customer()
                        self.admin_user_actions()

                    elif menuInput == 4:
                        self.retrieve_customer() 
                        self.admin_user_actions()   

                    elif menuInput == 5:
                        self.admin_user_actions()

                    elif menuInput == 6:
                        exit()

                    else:
                        print("Invalid Input. Please Try again.")
                        self.admin_user_actions()
                except Exception as e:
                    print("Error in Admin menu input: ", e)

            elif admin_menu_input == 2: # book/modify/cancel ticket
                try:
                    menuInput = int(input("Please select an option: \n 1. Book Ticket \n 2. Modify Ticket \n 3. Cancel Ticket \n 4. Retrieve Ticket \n 5. Back to the main menu \n 6. Exit \n"))
                    if menuInput == 1:
                        self.book_ticket()
                        self.admin_user_actions()

                    elif menuInput == 2:
                        self.modify_ticket()
                        self.admin_user_actions()

                    elif menuInput == 3:
                        self.cancel_ticket()
                        self.admin_user_actions()
                    
                    elif menuInput == 4:
                        self.retrieve_ticket()
                        self.admin_user_actions()

                    elif menuInput == 5:
                        self.admin_user_actions()

                    elif menuInput == 6:
                        exit()

                    else:
                        print("Invalid Input. Please Try again.")
                        self.admin_user_actions()
                except Exception as e:
                    print("Error in Admin menu input: ", e)

            elif admin_menu_input == 3 : # add/modify/delete airport
                try:
                    menuInput = int(input("Please select an option: \n 1. Add Airport \n 2. Modify Airport \n 3. Delete Airport \n 4. Retrieve Airport \n 5. Back to main menu \n 6. Exit \n"))
                    
                    if menuInput == 1: # selcted add airport 
                        self.add_airport()
                        self.admin_user_actions()
                        
                    elif menuInput == 2:
                        self.update_airport()
                        self.admin_user_actions()

                    elif menuInput == 3:
                        self.delete_airport()
                        self.admin_user_actions()

                    elif menuInput == 4:
                        self.retrieve_airport()
                        self.admin_user_actions()

                    elif menuInput == 5:
                        self.admin_user_actions()

                    elif menuInput == 6:
                        exit()
                    else:
                        print("Invalid Input. Please Try again.")
                        self.admin_user_actions()

                except Exception as e:
                    print("Error in Admin menu input: ", e)
                
            elif admin_menu_input == 4: # add/modify/delete flight
                try:
                    menuInput = int(input("Please select an option: \n 1. Add Flight \n 2. Modify Flight \n 3. Delete Flight \n 4. Retrieve Flight \n 5. Back to main menu \n 6. Exit \n"))
                    
                    if menuInput == 1:
                        self.add_flight()
                        self.admin_user_actions()
                        
                    elif menuInput == 2:
                        self.update_flight()
                        self.admin_user_actions()

                    elif menuInput == 3:
                        self.delete_flight()
                        self.admin_user_actions()

                    elif menuInput == 4:
                        self.retrieve_flight()
                        self.admin_user_actions()

                    elif menuInput == 5:
                        self.admin_user_actions()

                    elif menuInput == 6:
                        exit()
                    else:
                        print("Invalid Input. Please Try again.")
                        self.admin_user_actions()

                except Exception as e:
                    print("Error in Admin menu input: ", e)

            elif admin_menu_input == 5: # add/modify/delete an employee
       
                try:
                    menuInput = int(input("Please select an option: \n 1. Add Employee \n 2. Modify Employee \n 3. Delete Employee \n 4. Retrieve Employee \n 5. Back to main menu \n 6. Exit \n"))
                    
                    if menuInput == 1:
                        self.employee_signup()
                        self.admin_user_actions()
                        
                    elif menuInput == 2:
                        self.update_employee()
                        self.admin_user_actions()

                    elif menuInput == 3:
                        self.delete_employee()
                        self.admin_user_actions()

                    elif menuInput == 4:
                        self.retrieve_employee()
                        self.admin_user_actions()    

                    elif menuInput == 5:
                        self.admin_user_actions()

                    elif menuInput == 6:
                        exit()
                    else:
                        print("Invalid Input. Please Try again.")
                        self.admin_user_actions()

                except Exception as e:
                    print("Error in Admin menu input: ", e)

            elif admin_menu_input == 6: # searches for flights 
                self.search_flight()
                self.admin_user_actions()

            elif admin_menu_input == 7: # generate flight sales report
                self.generateFlightSalesReport()
                self.admin_user_actions()


            elif admin_menu_input == 8: # generate employee report for flights
                self.generateEmployeeReport() 
                self.admin_user_actions()


            elif admin_menu_input == 9:
                exit()
            else:
                print("Invalid menu input. Please try again.")
                self.admin_user_actions()

        except Exception as e:
            print("Error in the admin_user_actions block: ", e)
            self.admin_user_actions()

class UserMenus():
    def __init__(self):
        pass

    #add customer menu and employee menu here

    def adminMenu(self):
        try:
            val = int(input("Please select one of the options to proceed: \n Menu: \n 1. Add/Modify/Delete Customer \n 2. Book/Modify/Cancel Ticket \n 3. Add/Modify/Delete Airports  \n 4. Add/Modify/Delete Flights \n 5. Add/Modify/Delete Employees  \n 6. Search Flights \n 7. Generate Flight Sales Report \n 8. Generate Employee report for flights \n 9. Exit \n"))
            return val
        except ValueError:
            print("Invalid input. Please enter a number from the Menu.")
            self.adminMenu()
        except Exception as e:
            print("An Error has occured:", e)
            self.adminMenu()

