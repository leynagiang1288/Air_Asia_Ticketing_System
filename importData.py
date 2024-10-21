from airline_main import *

airline = AirAsiaDatabase()
airline.reset_database()

airlineRun = AirlineMain()

print("Customer file input:")
airlineRun.updateCustomerWithCSV()

# printing all customers
customer = Customer()
for cust in customer.getAllCustomers():
    print(cust)

print("Airport file input:")
airlineRun.updateAirportWithCSV()

# printing all airports
airport = Airport()
for airport in airport.getAllAirports():
    print(airport)

print("Ticket file input:")
airlineRun.updateTicketWithCSV()

# printing all airports
ticket = Ticket()
for ticket in ticket.getAllTickets():
    print(ticket)

