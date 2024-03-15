import pandas as pd
import matplotlib.pyplot as plt
import csv


class Stock:
    def __init__(self, name, wkn, kuerzel):
        self.name = name
        self.wkn = wkn
        self.kuerzel = kuerzel
        self.kursdaten = []  # List to store price data for the past 30 days

class StockManager:
    def __init__(self, size=1301):
        self.size = size
        self.table = [None] * self.size
        self.stockname = {}

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
        if len(key) > 4:
            if key in self.stockname:
                newkey = self.stockname[key]
                key = newkey
            else:
                return None
        index = int(self.hash_function(key))
        attempt = 0
        while self.table[index] is not None and self.table[index].kuerzel != key:
            index = self.quadratic_probe(index, attempt)
            attempt += 1
        if self.table[index] is not None:
            self.table[index] = Stock("", "", "")

    def import_stock_data(self, currentstock, filename):
        # Import stock data from a CSV file
        filename = "aktien_csvs/" + filename
        fields = []
        rows = []
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)

        currentstock.kursdaten = rows

    def search_stock(self, key):
        newkey = ""
        if len(key) > 4:
            if key in self.stockname:
                newkey = self.stockname[key]
                key = newkey
            else:
                return None
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
        if currentstock.kursdaten:
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
        else:
            print("No stock data available.")

    def save_to_file(self, filename):
        # Save the hashtable to a file
        pass

    def load_from_file(self, filename):
        # Load the hashtable from a file
        pass
def main():
    stock_manager = StockManager()

    while True:
        print("\nMenu:")
        print("1. Add Stock")
        print("2. Delete Stock")
        print("3. Import Stock")
        print("4. Search Stock")
        print("5. Plot Stock")
        print("8. Quit")

        choice = input("Enter your choice: ")

# Add Stock
        if choice == '1':
            name = input("Enter stock name: ")
            wkn = input("Enter WKN: ")
            kuerzel = input("Enter stock kuerzel: ")
            stock_already_exists = stock_manager.search_stock(kuerzel)
            stock_already_exists_2 = stock_manager.search_stock(name)
            if not (stock_already_exists or stock_already_exists_2):
                new_stock = Stock(name, wkn, kuerzel)
                stock_manager.add_stock(new_stock)
                print("Stock added successfully!")
            else:
                print("Stock already exists.")
# Delete Stock
        elif choice == '2':
            search_key = input("Enter stock name or kuerzel: ")
            found_stock = stock_manager.search_stock(search_key)
            if found_stock:
                stock_manager.delete_stock(search_key)
                print("Stock successfully deleted")
            else:
                print("Stock not found")
# Import Stock
        elif choice == '3':
            search_key = input("Enter stock name or kuerzel: ")
            stock_filename = input("Enter the .csv file to be imported: ")
            found_stock = stock_manager.search_stock(search_key)
            stock_manager.import_stock_data(found_stock, stock_filename)
            print("\""+ stock_filename + "\" successfully imported to the Stock " + search_key + "!")
# Search Stock
        elif choice == '4':
            search_key = input("Enter stock name or kuerzel: ")
            found_stock = stock_manager.search_stock(search_key)
            if found_stock:
                print(f"Found stock: {found_stock.name} ({found_stock.kuerzel})")
                if found_stock.kursdaten:
                    print("Date, Open, High, Low, Close, Adj. Close, Volume")
                for row in found_stock.kursdaten[:1]:
                    for col in row:
                        print("%10s" % col, end=" "),
                    print('\n')
            else:
                print("Stock not found.")
# Plot Stock
        elif choice == "5":
            search_key = input("Enter stock name or kuerzel: ")
            found_stock = stock_manager.search_stock(search_key)
            if found_stock:
                stock_manager.plot_stock_data(found_stock)
            else:
                print("Stock not found!")

        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()