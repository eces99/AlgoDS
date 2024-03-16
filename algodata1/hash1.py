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
        self.kursdaten = kursdaten  # List to store price data for the past 30 days

class StockManager:
    def __init__(self, size=1301):
        self.size = size
        self.table = [None] * self.size
        self.stockname = {} # Dictionary to match full stock names to their Kürzel

    def hash_function(self, kuerzel):
        # Implement a suitable hash function using the name or symbol of the stock
        hash_total = 0
        for i in range(len(kuerzel)):
            hash_total += ord(kuerzel[i]) * (31**(len(kuerzel)-1-i))
        hash_value = hash_total%self.size
        return hash_value

    def quadratic_probe(self, index, attempt):
        # Implement quadratic probing for collision resolution
        index = int(index)
        return (index + attempt**2) % self.size

    def add_stock(self, stock):
        index = self.hash_function(stock.kuerzel)
        index = int(index)
        attempt = 0
        while self.table[index] is not None:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        self.table[index] = stock
        self.stockname[stock.name] = stock.kuerzel

    def delete_stock(self, key):
        # Implement efficient deletion from the hashtable
        newkey = ""

        if len(key) > 6:
            key = key.title()
            if key in self.stockname:
                newkey = self.stockname[key]
                key = newkey
            else:
                return None
        key = key.upper()
        index = int(self.hash_function(key))
        attempt = 0
        while self.table[index] is not None and self.table[index].kuerzel != key:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        if self.table[index] is not None:
            self.table[index] = None

    def import_stock_data(self, currentstock, path):
        # Import stock data from a CSV file
        fields = []
        rows = []
        with open(path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
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
                newkey = self.stockname[key]
                key = newkey
            else:
                return None
        key = key.upper()
        index = self.hash_function(key)
        attempt = 0
        index = int(index)
        while self.table[index] is not None and self.table[index].kuerzel != key:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        if self.table[index] is not None:
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

    def save_to_file(self, filename):
        # Extracting relevant attributes from StockManager
        data = []
        for stock in self.table:
            if stock is not None:  # Check if the stock is not None
                data.append({
                    'Name': stock.name,
                    'WKN': stock.wkn,
                    'Symbol': stock.kuerzel,
                    'StockData': stock.kursdaten
                })
        # Construct the file path
        file_path = "./saved_tables/" + filename
        # Create a DataFrame from the extracted data
        data = pd.DataFrame(data)
        # Write the DataFrame to a CSV file
        data.to_csv(file_path, index=False)

    def load_from_file(self, filename):
        # Construct the file path
        file_path = "./saved_tables/" + filename

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

            # Create a new Stock object
            stock = Stock(name, wkn, kuerzel, kursdaten)

            self.add_stock(stock)
def main():
    stock_manager = StockManager()

    while True:
        print("\nMenu:")
        print("1. Add Stock")
        print("2. Delete Stock")
        print("3. Import Stock")
        print("4. Search Stock")
        print("5. Plot Stock")
        print("6. Save Hash Table")
        print("7. Load Hash Table")
        print("8. Quit")

        choice = input("Enter your choice: ")

# Add Stock
        if choice == '1':
            name = input("Enter stock name: ")
            if name == '':
                print("Name cannot be empty.")
                continue
            wkn = input("Enter WKN: ")
            if wkn == '':
                print("WKN cannot be empty.")
                continue
            kuerzel = input("Enter stock kuerzel: ")
            if kuerzel == '':
                print("Stock kuerzel cannot be empty.")
                continue

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
            search_key = input("Enter stock name or kuerzel: ")
            found_stock = stock_manager.search_stock(search_key)
            if found_stock:
                stock_manager.delete_stock(search_key)
                print(f"Stock {found_stock.name} ({found_stock.kuerzel}) successfully deleted!")
            else:
                print(f"Stock {search_key} not found!")

# Import Stock
        elif choice == '3':
            search_key = input("Enter stock name or kuerzel: ")
            stock_filename = input("Enter the .csv file to be imported: ")
            found_stock = stock_manager.search_stock(search_key)
            path = "aktien_csvs/" + stock_filename
            check_file = os.path.exists(path)
            if not check_file:
                print(".csv file \"" + stock_filename + "\" does not exist.")
            elif found_stock:
                stock_manager.import_stock_data(found_stock, path)
                print(f"\"{stock_filename}\" successfully imported to the Stock {found_stock.name} ({found_stock.kuerzel})!")
            else:
                print(f"Stock {search_key} not found.")

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
                print(f"Date{' '*7}Open{' '*7}High{' '*7}Low{' '*8}Close{' '*6}Adj Close{' '*4}Volume")
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
                filename = input("Enter file name: ")
                if filename == '':
                    print("Filename cannot be empty.")
                    continue
                stock_manager.save_to_file(filename)
                print(f"Hashtable saved as \"{filename}\"!")

# 7. LOAD <filename>: Programm lädt die Hashtabelle aus einer Datei
        elif choice == '7':
            filename = input("Enter file name: ")
            path = "./saved_tables/" + filename
            check_file = os.path.exists(path)
            if not check_file:
                print(f"File \"{filename}\" cannot be found.")
                continue
            if os.path.getsize(path) < 34:
                print(os.path.getsize(path))
                print(f"File \"{filename}\" is empty, cannot be loaded.")
                continue

            stock_manager.load_from_file(filename)
            print(f"File \"{filename}\" successfully loaded!")
# Exit
        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()