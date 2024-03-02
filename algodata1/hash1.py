import pandas as pd
import matplotlib.pyplot as plt


class Stock:
    def __init__(self, name, wkn, kuerzel):
        self.name = name
        self.wkn = wkn
        self.kuerzel = kuerzel
        self.kursdaten = []  # List to store price data for the past 30 days

class StockManager:
    def __init__(self, size=1000):
        self.size = size
        self.table = [None] * self.size

    def hash_function(self, kuerzel):
        # Implement a suitable hash function using the name or symbol of the stock
        hash_total = 0
        for i in kuerzel:
            hash_total += ord(i)
        hash_value = hash_total/self.size
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

    def delete_stock(self, kuerzel):
        # Implement efficient deletion from the hashtable
        pass

    def import_stock_data(self, kuerzel, filename):
        # Import stock data from a CSV file
        pass

    def search_stock(self, key):
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

    def plot_stock_data(self, kuerzel):
        # Plot the closing prices of the last 30 days as ASCII graph
        pass

    def save_to_file(self, filename):
        # Save the hashtable to a file
        pass

    def load_from_file(self, filename):
        # Load the hashtable from a file
        pass

# Beispiel-Nutzung des Stock Managers:
stock_manager = StockManager()

# Beispiel: Hinzufügen einer Aktie
msft_stock = Stock("Microsoft", "123456", "MSFT")
stock_manager.add_stock(msft_stock)

# Beispiel: Suchen nach einer Aktie
found_stock = stock_manager.search_stock("MSFT")
if found_stock:
    print(f"Found stock: {found_stock.name}")
else:
    print("Stock not found")
