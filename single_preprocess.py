import os
import sys
from preprocessor import preprocess

def process_file(input_file):
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == '.php':
        language = "php"
    elif file_extension == '.js':
        language = "js"
    else:
        print("Unsupported file type. Only .php and .js files are supported.")
        return None

    print(f"\nProcessing {input_file}...")

    pattern = preprocess(input_file, language)

    return pattern  # Return the processed pattern

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python single_preprocess.py <file_path/input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("Invalid file path.")
        sys.exit(1)

    preprocessed_features = process_file(input_file)
    if preprocessed_features is not None:
        print("\nFile processed successfully.")
    else:
        print("\nFailed to process the file.")

    # Return preprocessed_features
    sys.exit(preprocessed_features)
