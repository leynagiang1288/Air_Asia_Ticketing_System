# Air_Asia_Ticketing_System
Air_Asia_Ticketing_System

Pending actions:
1.	Crud for flights,employee,tickets
2.	User authentication -> new user/Existing User
3.	Menus for each user -> employee/admin/customer
4.	User actions for each type of user.
5.	Project documentation
6.	PPT if necessary.

-----------------------------------
TBD : 

Leyna - Customer menu and actions
Sunita - Crud for flights,employee, employee user actions and menu
Roja - User authentication -> new user/Existing User, Crud for tickets, admin user actions and menu

Pending items :

Leyna : Customer menu and actions
Sunita : employee user actions and menu
Roja : admin actions for search flights and tickets

------------------------------------

Customer Use Cases:

CRUD for Customer
Search for Flights
Purchase a Flight Ticket
Cancel a Flight Ticket

------------------------------------

Employee Use Cases:

CRUD for Employee
Update personal profile
View flight schedules

------------------------------------

Admin use cases:

CRUD for Customer, Ticket, Airport, Flight, Employee
Generate Reports for Flight Sales
Generate Employee report for flights
All Customer Use Cases
All Employee Use Cases

----------------------------------------------------------------------
The below description to be retained after project completion:

------------------------------------------------------------------------

AIRASIA TICKETING SYSTEM

AirAsia, a regional airline operating in the Asian market, is undertaking a comprehensive overhaul of their IT systems. As part of this initiative, they require a new ticketing system to be built. This AirAsia Ticketing system will serve as the central repository for the following information:

Details of the airports served by AirAsia
Information about AirAsia's employee base (including pilots, flight attendants, mechanics, administrative staff, etc.)
Data on AirAsia's direct flight offerings
Customer information
Booking details for tickets
The system caters to two primary user types:

Customers
Employees (including administrators, who are also classified as employees)
To set up and run this project, follow these steps:

Step 1: Execute importData.py - This file will import all mock data csv files into sqllite database tables.
Important: This file should only be run once at the beginning of the setup process. Running it multiple times will overwrite existing data.

Step 2: Run index.py
This file initiates the user authentication process. You'll be presented with below login screen:

Welcome to Airline Ticketing System
Please enter a number to proceed:

Login
Signup
Exit
After selecting an option, you'll be prompted to specify the user type:
User type (customer/employee/admin):

Then, proceed to login with your username and password.

Step 3: Post-login Navigation
Upon successful authentication, you'll be directed to the appropriate menu based on your user type (customer, employee, or admin).

This system structure allows for efficient management of AirAsia's ticketing operations, catering to both customer needs and employee functionalities within a single, integrated platform.