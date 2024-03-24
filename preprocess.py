from preprocessor import preprocess
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
        preprocess(file, "php")

    for file in js_samples:
        print(f"\nProcessing {file}...")
        preprocess(file, "js")

    print("\nAll files processed.")

   