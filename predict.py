from preprocessor import preprocess
import os
import pickle
import sys
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

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
    
    preprocessed_features = process_file(input_file).reshape(1, -1)
    print("Preprocessed features:", preprocessed_features)

    # Step 2: Load the saved model
    with open('bloom_randomforest.sav', 'rb') as f:
        model = pickle.load(f)

    # Calculate time
    import time
    start_time = time.time()
    # Step 3: Make predictions
    predictions = model.predict(preprocessed_features)
    print("Time taken:", time.time() - start_time)

    # Inject feature names
    feature_names = [
        "SQL Injection (SQLi)",
        "Cross-Site Scripting (XSS)",
        "Command/Code Injection",
        "File Inclusion",
        "Prototype Pollution"
    ]

    print(predictions)

    # # Get the names of features with values being 1
    predicted_features = [name for name, value in zip(feature_names, predictions[0]) if value == 1]

    # Print only the features with values being 1
    if predicted_features:
        print("Prediction:", ", ".join(predicted_features))
    else:
        print("Prediction: No vulnerabilities detected")


    # Return preprocessed_features
    sys.exit(1)