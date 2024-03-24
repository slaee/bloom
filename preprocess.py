from preprocessor import preprocess
import numpy as np
from pprint import pprint
import csv
import os

if __name__ == "__main__":
    php_samples_loc = 'test/samples/php'
    js_samples_loc = 'test/samples/javascript'

    php_samples = [os.path.join(php_samples_loc, f) for f in os.listdir(php_samples_loc) if os.path.isfile(os.path.join(php_samples_loc, f))]
    js_samples = [os.path.join(js_samples_loc, f) for f in os.listdir(js_samples_loc) if os.path.isfile(os.path.join(js_samples_loc, f))]

    for file in php_samples:
        print(f"\nProcessing {file}...")
        pattern = preprocess(file, "php")
        # Define the conditions for generating the combined_matrix
        combined_matrix = [
            1 if pattern[0].any() else 0,
            1 if pattern[1].any() else 0,
            1 if pattern[2].any() else 0,
            1 if pattern[3].any() else 0,
            0 if pattern[4][0].any() else 1,
            1 if pattern[5].any() else 0
        ]

        combined_matrix = np.array(combined_matrix).reshape(1, -1)
        combined_matrix = combined_matrix.flatten()

        pattern = pattern.flatten()

        # append the combined matrix to the pattern
        pattern = np.concatenate([pattern, combined_matrix], axis=0)
        with open('dataprocessing_dataset.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the combined data to the CSV file
            writer.writerow(pattern)  # Split the string and directly write to the CSV file

    for file in js_samples:
        print(f"\nProcessing {file}...")
        pattern = preprocess(file, "js")
        # Define the conditions for generating the combined_matrix
        combined_matrix = [
            1 if pattern[0].any() else 0,
            1 if pattern[1].any() else 0,
            1 if pattern[2].any() else 0,
            1 if pattern[3].any() else 0,
            0 if pattern[4][0].any() else 1,
            1 if pattern[5].any() else 0
        ]
        
        combined_matrix = np.array(combined_matrix).reshape(1, -1)
        combined_matrix = combined_matrix.flatten()

        pattern = pattern.flatten()

        # append the combined matrix to the pattern
        pattern = np.concatenate([pattern, combined_matrix], axis=0)
        with open('dataprocessing_dataset.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the combined data to the CSV file
            writer.writerow(pattern)  # Split the string and directly write to the CSV file

    print("\nAll files processed.")

   