import csv


class LanguageHandler:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = self._load_csv()

    def _load_csv(self):
        data = {}
        with open(self.csv_file, mode='r', encoding='UTF-8') as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                data[row.get("key")] = {k: v for k, v in row.items() if k != "key"}
        return data

    def get(self, key_id, language):
        entry: dict = self.data.get(str(key_id))
        if entry:
            return entry.get(language, None)
        return None
