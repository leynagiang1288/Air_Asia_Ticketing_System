from AirAsiaCsvIO import CsvToDB
from AirAsia import AirAsiaDatabase

class Customer(AirAsiaDatabase): #This class contains all the CRUD methods for the Customer table
    #This will be the method for adding
    def add_customer_info(self, first_name, last_name, dob, citizenship, email): #These are the possible values that can be added for each customer profile
        try:
            super().get_cursor.execute("""
            INSERT INTO Customer (first_name, last_name, dob, citizenship, email) VALUES (?, ?, ?, ?, ?);
            """, (first_name, last_name, dob, citizenship, email))
            super().get_connection.commit()
            print(f"The customer {first_name} {last_name} was added to the database")
        except Exception as e:
            print("There was an error adding in this new customer")
            print("The specific error adding the customer was:", e)

    #This method will update customer information based on the provided customer_ID
    def update_customer_info(self, customer_id, first_name, last_name, dob, citizenship, email):
        try:
            super().get_cursor.execute("""UPDATE Customer SET first_name = ?, last_name = ?, dob = ?, citizenship = ?, email = ? WHERE customer_id = ?;
            """, (first_name, last_name, dob, citizenship, email, customer_id))
            super().get_connection.commit()
            print(f"The customer information for customer {customer_id} was successfully updated") #Every method will include a successful print statement since its easier to tell if it worked or not with one
            return True
        except Exception as e: #All the exceptions will follow the same general format as the add method
            print("There was an error updating the customer information")
            print("The specific error updating the customer was:", e)
            return False

    #This method deletes the customer based off of the provided customer_id
    def delete_customer(self, customer_id):
        try:
            super().get_cursor.execute("""DELETE FROM Customer WHERE customer_id =?;
            """, (customer_id,))
            super().get_connection.commit()
            print(f"The customer {customer_id} was successfully deleted from the database")
        except Exception as e:
            print("There was an error deleting the customer entry")
            print("The specific error was:", e)

    #This method will retrieve customer information by customer_id
    def retrieve_customer_information(self, customer_id = None):
        try:
            if customer_id is not None:
                retval = super().get_cursor.execute("""SELECT first_name, last_name, dob, citizenship, email FROM Customer WHERE customer_id = ?
                """, (customer_id,)).fetchone()
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

class Airport(AirAsiaDatabase): #This class will contain all the CRUD methods for airports
    #The method to add and create new airport entries
    def add_airport(self, airport_name, city, country):
        try:
            super().get_cursor.execute(
                """INSERT INTO Airport (airport_name, city, country) VALUES (?, ?, ?);""", (airport_name, city, country))
            super().get_connection.commit()
            print(f"The new airport of {airport_name} was successfully added to Air Asia's Database")
        except Exception as e:
            print("There was an error adding a new airport")
            print("The specific error adding a new airport was:", e)

    #The method for updating airport information
    def update_airport(self, airport_id, airport_name, city, country):
        try:
            super().get_cursor.execute("""UPDATE Airport SET airport_name = ?, city = ?, country = ? WHERE airport_id = ?;""",
                                       (airport_name, city, country, airport_id))
            super().get_connection.commit()
            print(f"The information for airport #{airport_id} was successfully updated")
        except Exception as e:
            print("There was an error updating the airport information")
            print("The specific error updating airport information was:", e)

    #The method for deleting airports based on airport_id provided
    def delete_airport(self, airport_id):
        try:
            super().get_cursor.execute("""DELETE FROM Airport WHERE airport_id =?;
                        """, (airport_id,))
            super().get_connection.commit()
            print(f"The airport #{airport_id} was successfully deleted from the database")
        except Exception as e:
            print("There was an error deleting the customer entry")
            print("The specific error was:", e)

    #This method will retrieve airport information by airport_id
    def retrieve_airport_information(self, airport_id = None):
        try:
            if airport_id is not None:
                retval = super().get_cursor.execute("""SELECT airport_name, city, country FROM Airport WHERE airport_id = ?
                """, (airport_id,)).fetchone()
                return retval
            else:
                return super().get_cursor.execute("""SELECT airport_name, city, country FROM Airport""").fetchall()
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

class AirlineMain(Customer, Airport):

    def __init__(self):
        super().__init__()

    def updateAirportWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv): "))
            newCSV = CsvToDB(fileName, "Air_Asia_Database.sqlite", "airport")
            newCSV.run()
        except Exception as e:
            print("Error while updating Airport with CSV: ", e)

    def updateFlightWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv): "))
            newCSV = CsvToDB(fileName, "Air_Asia_Database.sqlite", "flight")
            newCSV.run()
        except Exception as e:
            print("Error while updating Flight with CSV: ", e)

    def updateCustomerWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv): "))
            newCSV = CsvToDB(fileName, "Air_Asia_Database.sqlite","customer")
            newCSV.run()
        except Exception as e:
            print("Error while updating Customer with CSV: ", e)

    def updateEmployeeWithCSV(self):
        try:
            fileName = str(input("Please enter a file name (.csv): "))
            newCSV = CsvToDB(fileName, "Air_Asia_Database.sqlite","employee")
            newCSV.run()
        except Exception as e:
            print("Error while updating Employee with CSV: ", e)

# if __name__ == "__main__":
#     # Initialize the database
#     Air_Asia = AirAsiaDatabase()
#     Air_Asia.reset_database()

#     # Get the database file name
#     db_file = "Air_Asia_Database.sqlite"  # This should match the name in AirAsiaDatabase.__init__

#     # Import Customer data
#     customer_csv_to_sqlite = CsvToSQLite("customer.csv", db_file, "Customer")
#     customer_csv_to_sqlite.run()

#     # Import Airport data
#     airport_csv_to_sqlite = CsvToSQLite("airport.csv", db_file, "Airport")
#     airport_csv_to_sqlite.run()

#     # Now you can use your CRUD methods
#     customer1 = Customer()
#     airport1 = Airport()

#     # Retrieve and print all customers
#     print("All Customers:")
#     print(customer1.retrieve_customer_information())

#     # Retrieve and print all airports
#     print("\nAll Airports:")
#     print(airport1.retrieve_airport_information())

#     # Add a new customer
#     customer1.add_customer_info("Roja", "Chekuri", "1993-10-15", "Indian", "ltestg@gmail.com")

#     # Add a new airport
#     airport1.add_airport("Changi", "Singapore", "Singapore")

#     # Retrieve and print updated data
#     print("\nUpdated Customers:")
#     print(customer1.retrieve_customer_information())
#     print("\nUpdated Airports:")
#     print(airport1.retrieve_airport_information())

#     # Example of updating and deleting
#     customer1.update_customer_info(1, "John", "Doe", "1990-01-02", "American", "john.doe.updated@email.com")
#     airport1.delete_airport(1)

#     # Final data state
#     print("\nFinal Customer Data:")
#     print(customer1.retrieve_customer_information())
#     print("\nFinal Airport Data:")
#     print(airport1.retrieve_airport_information())
    
#############################################
#CODE TO TEST AND GENERATE DATABASE / INSTANCES
#Air_Asia = AirAsiaDatabase()
#Air_Asia.reset_database()
# customer1 = Customer()
#customer1.add_customer_info("Leyna", "Giang", "2001-06-08", "American", "leynagiang@gmail.com" )
#customer1.update_customer_info(1, "Leyna", "Giang", "2001-06-28", "American", "leynagiang@gmail.com")
#customer1.delete_customer(1)
#print(customer1.retrieve_customer_information(2))
# airport1 = Airport()
#airport1.add_airport("Delta", "Boston", "Massachusetts")
#airport1.update_airport(1, "Delta Airlines", "Boston", "Massachusetts")
#airport1.delete_airport(1)
#print(airport1.retrieve_airport_information(2))
