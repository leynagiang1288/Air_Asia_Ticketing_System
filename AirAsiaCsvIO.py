#This file will run import fucntions to import csv data to the database tables and vice-versa. Password hashing is also implemented to store the passsword in bytes 
# for customer and employee tables.

import bcrypt
import pandas as pd # type: ignore
import sqlite3

class CsvToDB:
    def __init__(self, csv_file, db_file, table_name):
        self.csv_file = csv_file
        self.db_file = db_file
        self.table_name = table_name

    def readCSVFile(self):
        try:
            df = pd.read_csv(self.csv_file)
            print(f"Successfully read CSV file!")
            return df
        except FileNotFoundError:
            print(f"CSV File '{self.csv_file}' not found.")
            return None
        except Exception as e:
            print("Error while reading the CSV file:", e)
            return None
        
    def writeToDB(self, df):
        try:
            conn = sqlite3.connect(self.db_file)
            df.to_sql(self.table_name, conn, if_exists='append', index=False)
            conn.close()
            print(f"The CSV file has been successfully written to the '{self.table_name}' table in the '{self.db_file}' database.")

        except sqlite3.OperationalError as e:
            print("An error occurred while writing to the SQLite database:", e)

        except Exception as e:
            print("An error occurred while writing to the SQLite database:", e)

    def run(self):
        df = self.readCSVFile()
        if df is not None:
            self.writeToDB(df)


class DbToCSV:
    def __init__(self, db_file, query, file_name):

        self.db_file = db_file
        self.query = query
        self.file_name = file_name

    def writeToCsvFile(self):
        try:
            conn = sqlite3.connect(self.db_file)
            df = pd.read_sql_query(self.query, conn)
            df.to_csv(self.file_name, index=False)
            print(f" '{self.db_file}' database has been successfully written to the '{self.file_name}' CSV file.")
        except sqlite3.OperationalError as e:
            print("An error occurred while reading from the SQLite database:", e)
        except Exception as e:
            print("An error occurred while writing to the CSV file:", e)
        finally:
            conn.close()

class CsvToDBWithEncryption:
    def __init__(self, csv_file, db_file, table_name, password):
        self.csv_file = csv_file
        self.db_file = db_file
        self.table_name = table_name
        self.password = password

    def readCSV(self):
        try:
            df = pd.read_csv(self.csv_file)
            return df
        except FileNotFoundError:
            print("CSV File not found.")
            return None
        except Exception as e:
            print("Error while reading the CSV file:", e)
            return None

    def writeToDB(self, df):
        try:
            conn = sqlite3.connect(self.db_file)
            df[f'{self.password}'] = [bcrypt.hashpw(str(val).encode(), bcrypt.gensalt()).decode() for val in df[f'{self.password}']]
            df.to_sql(self.table_name, conn, if_exists='append', index=False)
            conn.close()
            print(f"The CSV file has been successfully written to the '{self.table_name}' table in the '{self.db_file}' database.")

        except sqlite3.OperationalError as e:
            print("An error occurred while writing to the SQLite database:", e)

        except Exception as e:
            print("An error occurred while writing to the SQLite database:", e)

    def run(self):
        df = self.readCSV()
        if df is not None:
            self.writeToDB(df)
