import csv
import re
from io import TextIOWrapper


def convert_string(input_string):
    # Convert capital letters to lowercase
    if not input_string or input_string == "":
        return None
    lowercase_string = input_string.lower()

    # Remove non-alphabetic characters
    cleaned_string = re.sub('[^a-z0-9]', '', lowercase_string)

    return cleaned_string


def csv_to_dictionary(file_path):
    result = {}
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            print(row)
        raw_headers = next(reader)  # Read the first row as headers
        headers = [convert_string(header) for header in raw_headers]  # Clean the headers using convert_string function
        #  create custom header for check
        header_dictionary = []
        for item in raw_headers:
            if item:
                header_dictionary.append({convert_string(item): item})
        for row in reader:
            row_data = {}
            for header, value in zip(headers, row):
                row_data[header] = value
            data.append(row_data)

        return data, header_dictionary


# Usage example:
csv_file_path = 'cvv.csv'  # Replace with your CSV file path
data, dictionary = csv_to_dictionary(csv_file_path)
print(data)
print(dictionary)
