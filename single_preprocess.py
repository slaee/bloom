import os
import sys
import csv
from preprocessor import preprocess


def process_file(input_file):
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == '.php':
        language = "php"
    elif file_extension == '.js':
        language = "js"
    else:
        print("Unsupported file type. Only .php and .js files are supported.")
        return

    print(f"\nProcessing {input_file}...")

    pattern = preprocess(input_file, language)

    with open('singe_dataprocessing_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(pattern)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python single_preprocess.py <file_path/input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("Invalid file path.")
        sys.exit(1)

    process_file(input_file)

    print("\nFile processed successfully.")

