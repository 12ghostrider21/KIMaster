import csv  # Import the csv module to handle CSV file operations
from enum import auto, Enum  # Import auto and Enum from the enum module to define enumerations


# Define an enumeration called LANGUAGE to represent different languages
class LANGUAGE(Enum):
    EN = auto()  # English language
    DE = auto()  # German language
    FR = auto()  # French language


# Define a class called LanguageHandler to manage language data from a CSV file
class LanguageHandler:
    # Initialize the LanguageHandler with the path to a CSV file
    def __init__(self, csv_file):
        self.csv_file = csv_file  # Store the CSV file path
        self.data = self._load_csv()  # Load the CSV data into a dictionary

    # Private method to load data from the CSV file into a dictionary
    def _load_csv(self):
        data = {}  # Initialize an empty dictionary to store the data
        # Open the CSV file in read mode with UTF-8-SIG encoding to handle BOM
        with open(self.csv_file, mode='r', encoding='utf-8-sig') as file:
            # Create a CSV DictReader to parse the CSV file with semicolon delimiter
            reader = csv.DictReader(file, delimiter=";")
            # Iterate over each row in the CSV file
            for row in reader:
                # Use the value in the "key" column as the dictionary key
                # Create a nested dictionary with the rest of the columns and their values
                data[row.get(r"key")] = {k: v for k, v in row.items() if k != "key"}
        return data  # Return the populated dictionary

    # Method to retrieve a translation entry for a given key and language
    def get(self, key_id, language):
        entry: dict = self.data.get(str(key_id))  # Get the entry for the given key as a dictionary
        if entry:  # If the entry exists
            return entry.get(language, None)  # Return the value for the specified language or None if not found
        return None  # Return None if the entry does not exist


# If this script is run as the main program
if __name__ == "__main__":
    LanguageHandler("language.csv")  # Create an instance of LanguageHandler with the specified CSV file
