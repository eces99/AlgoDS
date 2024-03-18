import re

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os.path
import ast


class Stock:
    def __init__(self, name, wkn, kuerzel, kursdaten=[]):
        self.name = name
        self.wkn = wkn
        self.kuerzel = kuerzel
        self.kursdaten = kursdaten  # List to store stock data for the past 30 days

class StockManager:
    def __init__(self, size=1301):
        self.size = size
        self.table = [None] * self.size
        self.stockname = {}  # Dictionary to match full stock names to their Kuerzel
        self.num_table = 0

    def hash_function(self, kuerzel):
        # Implement a suitable hash function using the name or symbol of the stock
        hash_total = 0
        for i in range(len(kuerzel)):
            hash_total += ord(kuerzel[i]) * (31 ** (len(kuerzel) - 1 - i))
        hash_value = hash_total % self.size
        return hash_value

    def quadratic_probe(self, index, attempt):
        # Implement quadratic probing for collision resolution
        index = int(index)
        return (index + attempt ** 2) % self.size

    def add_stock(self, stock):
        index = self.hash_function(stock.kuerzel)
        index = int(index)
        attempt = 0
        # Change index with quadratic probing in case of collision
        while self.table[index] is not None:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        self.table[index] = stock  # add stock/value to its key/index
        self.stockname[stock.name] = stock.kuerzel  # Add stock name as key and kuerzel as value to dictionary
        self.num_table += 1

    def delete_stock(self, key):
        # Implement efficient deletion from the hashtable
        newkey = ""

        if len(key) > 6:
            key = key.title()
            if key in self.stockname:
                newkey = self.stockname[key]  # If the key is the name, change key to name's symbol
                key = newkey
            else:
                print(f"Stock {key} not found!")
                return None
        key = key.upper()  # Uppercase key after changed to symbol
        index = int(self.hash_function(key))
        attempt = 0
        # Quadratic probing while there is a found stock but input key doesn't match
        while self.table[index] is not None and self.table[index].kuerzel != key:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        if self.table[index] is not None:  # If stock has been found and input key matches, delete stock
            print(f"Stock {self.table[index].name} ({self.table[index].kuerzel}) successfully deleted!")
            self.table[index] = None
            self.num_table -= 1
        else:
            print(f"Stock {key} not found!")

    def import_stock_data(self, currentstock, path):
        # Import stock data from a CSV file
        rows = []  # Stock data from a CSV file stored in an array
        with open(path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            # A single row from the CSV file is the stock data of a single day and one element in the array
            for row in csvreader:
                rows.append(row)
                if len(rows) >= 30:
                    break

        currentstock.kursdaten = rows

    def search_stock(self, key):
        newkey = ""
        if len(key) > 6:
            key = key.title()
            if key in self.stockname:
                newkey = self.stockname[key]  # If the key is the name, change key to name's symbol
                key = newkey
            else:
                return None
        key = key.upper()  # Uppercase key after changed to symbol
        index = self.hash_function(key)
        attempt = 0
        index = int(index)
        # Quadratic probing while there is a found stock but input key doesn't match
        while self.table[index] is not None and self.table[index].kuerzel != key:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        if self.table[index] is not None:  # If stock has been found and input key matches, return stock
            return self.table[index]
        else:
            return None

    def plot_stock_data(self, currentstock):
        # Plot the closing prices of the last 30 days
        # Extract date and closing price data for plotting
        dates = [row[0] for row in currentstock.kursdaten]
        close_prices = [float(row[4]) for row in currentstock.kursdaten]

        # Plot the data
        plt.figure(figsize=(15, 10))
        plt.plot(dates, close_prices)
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'Stock Price Over Time ({currentstock.name})')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.show()

    def save_to_file(self, file_path):
        # Extracting relevant attributes from StockManager
        data = []
        for stock in self.table:
            if stock is not None:  # Check if the stock is not None, only save non-empty table values
                data.append({
                    'Name': stock.name,
                    'WKN': stock.wkn,
                    'Symbol': stock.kuerzel,
                    'StockData': stock.kursdaten
                })
        # Create a DataFrame from the extracted data
        data = pd.DataFrame(data)
        # Write the DataFrame to a CSV file
        data.to_csv(file_path, index=False)

    def load_from_file(self, file_path):
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_path)

        # Iterate over the rows of the DataFrame and populate the StockManager table
        for _, row in data.iterrows():
            name = row['Name']
            wkn = row['WKN']
            kuerzel = row['Symbol']
            kursdaten = row['StockData']

            # Parse kursdaten_str from string to list of lists
            kursdaten = ast.literal_eval(kursdaten)

            # Check if stock already exists in current hashtable before adding externally
            stockkuerzel_already_exists = self.search_stock(kuerzel)
            stockname_already_exists = self.search_stock(name)
            if not (stockkuerzel_already_exists or stockname_already_exists):
                # Create a new Stock object
                stock = Stock(name, wkn, kuerzel, kursdaten)
                self.add_stock(stock)
                print(f"Stock {name} ({kuerzel}) added successfully!")
            else:
                print(f"Stock {name} or {kuerzel} already exists.")


def main():
    stock_manager = StockManager()

    while True:
        print("\nMenu:")
        print("1. ADD")
        print("2. DELETE")
        print("3. IMPORT")
        print("4. SEARCH")
        print("5. PLOT")
        print("6. SAVE")
        print("7. LOAD")
        print("8. QUIT")

        choice = input("Enter your choice: ")

        # Add Stock
        if choice == '1':
            # inputs with validation
            while True:
                name = input("Enter stock name: ")
                if not name.strip():
                    print("Name cannot be empty.")
                    continue
                if not re.search('[a-zA-Z]', name):
                    print("Stock name should contain letters.")
                    continue
                if len(name) < 6:
                    print("Stock name should be longer than 6 letters.")
                    continue

                wkn = input("Enter WKN: ")
                if not wkn.strip():
                    print("WKN cannot be empty.")
                    continue
                if not wkn.isdigit() or len(wkn) != 6:
                    print("WKN should be a 6-digit number.")
                    continue

                kuerzel = input("Enter stock kuerzel: ")
                if not kuerzel.strip():
                    print("Stock kuerzel cannot be empty.")
                    continue
                if not kuerzel.isalpha():
                    print("Kürzel should only contain letters.")
                    continue

                # If all inputs are valid, break the loop
                break

            # Now, you have valid inputs stored in 'name', 'wkn', and 'kuerzel'
            name = name.title()
            kuerzel = kuerzel.upper()
            stockkuerzel_already_exists = stock_manager.search_stock(kuerzel)
            stockname_already_exists = stock_manager.search_stock(name)
            if not (stockkuerzel_already_exists or stockname_already_exists):
                new_stock = Stock(name, wkn, kuerzel)
                stock_manager.add_stock(new_stock)
                print(f"Stock {name} ({kuerzel}) added successfully!")
            else:
                print(f"Stock {name} or {kuerzel} already exists.")

        # Delete Stock
        elif choice == '2':
            if stock_manager.num_table == 0:
                print("Hash table is empty, nothing to delete.")
                continue
            search_key = input("Enter stock name or kuerzel: ")
            stock_manager.delete_stock(search_key)

        # Import Stock
        elif choice == '3':
            search_key = input("Enter stock name or kuerzel: ")
            stock_filename = input("Enter the .csv file to be imported: ")
            found_stock = stock_manager.search_stock(search_key)
            path = "aktien_csvs/" + stock_filename
            file_exists = os.path.exists(path)
            if not file_exists:
                print(".csv file \"" + stock_filename + "\" does not exist.")
                continue
            if not found_stock:
                print(f"Stock {search_key} not found.")
                continue
            stock_manager.import_stock_data(found_stock, path)
            print(f"\"{stock_filename}\" successfully imported to the Stock {found_stock.name} ({found_stock.kuerzel})!")


        # Search Stock
        elif choice == '4':
            search_key = input("Enter stock name or kuerzel: ")
            found_stock = stock_manager.search_stock(search_key)
            if found_stock:
                print(f"Found stock: {found_stock.name} ({found_stock.kuerzel})")
            else:
                print(f"Stock {search_key} not found.")
                continue
            if found_stock.kursdaten:
                print(f"Date{' ' * 7}Open{' ' * 7}High{' ' * 7}Low{' ' * 8}Close{' ' * 6}Adj Close{' ' * 4}Volume")
                for row in found_stock.kursdaten[:1]:
                    for col in row:
                        print("%10s" % col, end=" "),
                    print('\n')

        # Plot Stock
        elif choice == "5":
            search_key = input("Enter stock name or kuerzel: ")
            found_stock = stock_manager.search_stock(search_key)
            if not found_stock:
                print(f"Stock {search_key} not found.")
                continue
            if not found_stock.kursdaten:
                print(f"No stock data for {found_stock.name} ({found_stock.kuerzel}) available.")
                continue
            stock_manager.plot_stock_data(found_stock)

        # 6. SAVE <filename>: Programm speichert die Hashtabelle in eine Datei ab
        elif choice == '6':
            if stock_manager.num_table == 0:
                print("Hash table is empty, nothing to save.")
                continue
            filename = input("Enter file name: ")
            # Add .csv file extension to filename
            filename = filename + ".csv"
            # Construct the file path
            file_path = "./saved_tables/" + filename
            if not filename.strip():
                print("Filename cannot be empty.")
                continue
            stock_manager.save_to_file(file_path)
            print(f"Hashtable saved as \"{filename}\"!")

        # 7. LOAD <filename>: Programm lädt die Hashtabelle aus einer Datei
        elif choice == '7':
            filename = input("Enter file name: ")
            # Construct the file path
            file_path = "./saved_tables/" + filename
            file_exists = os.path.exists(file_path)
            if not file_exists:
                print(f"File \"{filename}\" cannot be found.")
                continue
            if os.path.getsize(file_path) < 34:  # 34 bytes -> filesize of an exported hashtable with empty inputs
                print(f"File \"{filename}\" is empty, cannot be loaded.")
                continue
            print(f"File \"{filename}\" successfully loaded!")
            stock_manager.load_from_file(file_path)

        # Exit
        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
