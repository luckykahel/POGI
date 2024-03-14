import sqlite3

class DatabaseManager: #class creation
    def __init__(self, database): #constructor method 
        #instance variable
        self.database = database 
        self.connect = sqlite3.connect(self.database)
        self.cursor = self.connect.cursor()
        
        #----table creation----

        #bikes table consist of bike id, bike type, availability
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bikes (
                                bike_id INTEGER PRIMARY KEY,
                                bikeType TEXT NOT NULL,
                                availability INTEGER NOT NULL DEFAULT 1,
                                rate FLOAT NOT NULL
                            )''')
        
        #rental table consist of id, name of the renter, clock start and end, cellphone number, bike id referenced from bikes table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rental (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                clock_start TEXT NOT NULL,
                                clock_end TEXT,
                                cell_num INT NOT NULL,
                                bike_id INT,
                                rate FLOAT NOT NULL,
                                total_price FLOAT,
                                FOREIGN KEY (bike_id) REFERENCES bikes(bike_id)
                            )''')
        
        self.connect.commit()
        
    def close_connection(self): #method that closes the database
        self.connect.close()

    def add_bike(self, bikeType, rate=None):
        try:
            if rate is None or rate=='':
                #default rates for reg and prem if rate is not edited
                if bikeType.lower() == 'regular':
                    rate = 50
                elif bikeType.lower() == 'premium':
                    rate = 100
                else:
                    print("Invalid bike type.")
                    return False

            self.cursor.execute('''INSERT INTO bikes (bikeType, rate) VALUES (?, ?)''', (bikeType, rate))
            self.connect.commit()
            return True
        except sqlite3.IntegrityError: #exception if there is a duplicate
            print("Bike already exists.")
            return False
        
    def update_rate(self, bikeType, new_rate=None):
        bikecat = bikeType.lower() #to remove case sensitivity
        try:
            if new_rate is None or new_rate=='':
                #default rates for reg and prem if rate is not edited
                if bikeType.lower() == 'regular':
                    new_rate = 50
                elif bikeType.lower() == 'premium':
                    new_rate = 100
                else:
                    print("Invalid bike type.")
                    return False
            self.cursor.execute('''UPDATE bikes SET rate = ? WHERE LOWER(bikeType) = ?''', (new_rate, bikecat))
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            print("Failed to update rate.")
            return False

    def add_rental(self, name, start, cellNum, bikeNum, type): #method that adds values to rental table
        try:
            self.cursor.execute('''SELECT bikeType, rate FROM bikes WHERE bike_id = ? AND LOWER(bikeType) = ?''', (bikeNum, type.lower()))
            #self.cursor.execute('''SELECT bikeType, rate FROM bikes WHERE bike_id = ?''', (bikeNum,))
            bike_data = self.cursor.fetchone()
            print("bike_data:", bike_data) # 
            if bike_data: #if there is a data fetched from the row it will continue.
                bikeType, rate = bike_data
            else:
                print("Bike not found.")
                return False
            
            self.cursor.execute('''INSERT INTO rental (name, clock_start, cell_num, bike_id, rate) 
                                VALUES (?, ?, ?, ?, ?)''', (name, start, cellNum, bikeNum, rate)) #for the rental table and transaction history purposes
            self.cursor.execute('''UPDATE bikes SET availability = 0 WHERE bike_id = ?''', (bikeNum,)) #changes the value of availability since the bike is rented
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            print("Bike number not found or already rented.")
            return False
        
    def return_bike(self, bikeNum, end, total_price): #method that update the clock out from rental table.
        try:
            self.cursor.execute('''SELECT id FROM rental WHERE bike_id = ? AND clock_end IS NULL''', (bikeNum,)) #for validation if the bike is currently in used
            rental_id = self.cursor.fetchone() #variable holding the id selected from rental
            if not rental_id: #if it returns none meaning the bike is not currently rented and will return a false value
                print("Bike is not currently rented.")
                return False
            #will execute if the fetched value is not none
            self.cursor.execute('''UPDATE rental SET clock_end = ?, total_price = ? WHERE id = ?''', (end, total_price, rental_id[0]))
            self.cursor.execute('''UPDATE bikes SET availability = 1 WHERE bike_id = ?''', (bikeNum,)) #changes the value to 1 since it was returned
            self.connect.commit()
            return True
        except sqlite3.IntegrityError:
            print("Bike number not found or already returned.")
            return False

    def get_transactions_history(self): #method that creates the transaction history by combining different values from the bikes and rental table
        self.cursor.execute('''SELECT rental.name, rental.clock_start, rental.clock_end, rental.total_price, bikes.bike_id, bikes.bikeType 
                               FROM rental 
                               INNER JOIN bikes ON rental.bike_id = bikes.bike_id''')
        return self.cursor.fetchall() #fetch all row

    def generate_id(self, biketype):  #-------!!!!!!!!!!!PATESTING AKO NETO KUNG GUMAGANA DAPAT YUNG BIKETYPE EITHER NAKADEFINE NA REGULAR OR PREMIUM DEPENDE KUNG SAN PAGE
                                      # TAS KUNG ANO IRERETURN NETO YUN YUNG LAMAN NG ENTRY BOX THANKS!
        self.cursor.execute('''SELECT bike_id FROM bikes WHERE LOWER(bikeType) = ? AND availability = 1''', (biketype.lower(),))
        row = self.cursor.fetchone()
        if row:
            bike_id = row[0]  # extracting bike_id value from the current row
            return bike_id
        else:
            return "No Bikes Available"  # no matching row was found
        
    def generate_rate(self, biketype):
        self.cursor.execute('''SELECT rate FROM bikes WHERE LOWER(bikeType) = ?''', (biketype.lower(),))
        row = self.cursor.fetchone()
        if row:
            current_rate = row[0]  # extracting value from the current row
            return current_rate
        else:
            return "0"
        
    def view_table(self): #for testing only disregard
        self.cursor.execute('''SELECT * FROM bikes''')
        return self.cursor.fetchall()
    