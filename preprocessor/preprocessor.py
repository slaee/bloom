import re
import numpy as np
from sklearn.preprocessing import normalize
from .extractor import extract_variables
from .statement.matcher import *
import csv

def code_cleaner(filename):
    with open(filename, 'r') as f:
        code = f.read()
    # GENERAL: 
    # remove multiline comments
    code = re.sub(r'/\*(.*?)\*/', '', code, flags=re.DOTALL)
    # remove all single line comments (//|#) except if (//|#) is inside of a string like "htes // asdf" or 'htes # asdf'
    code = re.sub(r'(?<!\\)(["\'])(?:\\.|(?!\1).)*?\1|//.*?$|#.*?$', 
                  lambda m: m.group(0) if m.group(0).startswith('"') or m.group(0).startswith("'") else '', code, flags=re.MULTILINE)
    # remove all newlines after a ( ,|.|\(|\[ ) or spaces after a ( ,|.|\(|\[ )
    code = re.sub(r'(\[|\(|,|\.)\s+', r'\1', code)
    # remove all newlines before a ( ,|.|;|\)|\] ) or spaces before a ( ,|.|;|\)|\] )
    code = re.sub(r'\s+(\]|\)|,|\.|;)', r'\1', code)
    # remove all trailing comma before a ( \) | \] )
    code = re.sub(r',(\s*[\]\)])', r'\1', code)
    # split code into lines
    code = code.split('\n')
    # convert to numpy array for faster processing
    code = np.array(code)
    # remove leading and trailing whitespace
    code = np.char.strip(code)
    # remove all semi-colons and open curly braces at the end of a line
    for i in np.nditer(code, op_flags=['readwrite']):
        line = ''.join(i.item(0))
        i[...] = re.sub(r'(;|{)$', '', line).strip()
    # After removing aliens, we can remove some twigs symbols, single words and numbers
    # remove all elements that are one word or numeric only in a string or symbols only in a string.
    # Use NumPy vectorized operations with regular expressions to filter lines.
    non_whitespace = ~np.vectorize(lambda x: bool(re.match(r'^\W+$', x)))(code)
    non_word = ~np.vectorize(lambda x: bool(re.match(r'^\w+$', x)))(code)
    non_digit = ~np.vectorize(lambda x: bool(re.match(r'^\d+$', x)))(code)
    # Filter lines based on conditions
    code = code[non_whitespace & non_word & non_digit]
    # remove all php tags
    code = code[~np.char.startswith(code, '<?php') & ~np.char.startswith(code, '?>')]
    # lastly remove all empty lines
    code = code[code != '']
    return code

# Gets variable references of JS and PHP
def vars_references(vars, code):
    references = []
    for var in vars:
        # case sensitive and match whole word only or if wrapped in a special character
        var_pattern = r'(?<!\w)' + re.escape(var) + r'(?!\w)'
        var_references = [line for line in code if re.search(var_pattern, line)]
        references.append((var, var_references))
    return references

def check_variable_usage(code_snippet):
    # php regex rules for catching tainted variables with user input
    php_pattern = re.compile(r'(?:(\$_(?:GET|POST|REQUEST|SERVER|COOKIE|ENV|FILES)\b)|\b(?:GET|POST|REQUEST|SERVER|COOKIE|ENV|FILES)\b)\b')
    # pure js regex rules for catching tainted variables with user input
    js_pattern = re.compile(r'(?:\w+)\.(?:body|params|query|headers)', re.IGNORECASE)
    # express js regex rules for catching tainted variables with user input
    express_js_pattern = re.compile(r'(?:\w+)\.(?:body|params|query|headers|param|queryparam|get|post|paramfrom)', re.IGNORECASE)
    php_match = re.search(php_pattern, code_snippet)
    js_match = re.search(js_pattern, code_snippet)
    express_js_match = re.search(express_js_pattern, code_snippet)
    return bool(php_match), bool(js_match), bool(express_js_match)

def tainted_variables(references):
    tainted_variables = []
    for var, snippets in references:
        for snippet in snippets:
            matches = check_variable_usage(snippet)
            if any(matches):
                tainted_variables.append(var)
    # remove duplicates without changing the order
    tainted_variables = list(dict.fromkeys(tainted_variables))
    return tainted_variables

def tainted_vars_snippets(references, tainted_variables, variables):
    # Iterate over each variable in the variables list
    for var, snippets in references:
        for snippet in snippets:
            for variable in variables:
                # Check if the variable is used in the snippet
                if variable in snippet and variable != var:
                    # Add the variable to the references if it's not already present
                    if not any(variable == v[0] for v in references):
                        references.append((variable, []))
                    # Add the variable to the tainted variables list if it's not already present
                    if variable not in tainted_variables:
                        tainted_variables.append(variable)

    # Extract tainted snippets for each tainted variable
    tainted_var_and_snippets = []
    for tainted_var in tainted_variables:
        tainted_snippets = []
        for var, snippets in references:
            if var == tainted_var:
                tainted_snippets.extend(snippets)
        tainted_var_and_snippets.append((tainted_var, tainted_snippets))
    return tainted_var_and_snippets


def begin_preprocessing(variables, file):
    code = code_cleaner(file)
    references = vars_references(variables, code)
    tainted_vars = tainted_variables(references)
    tainted_result = tainted_vars_snippets(references, tainted_vars, variables)
    return tainted_result

def grab_pattern(tainted_varsnippets):
    if (len(tainted_varsnippets) == 0):
        return np.zeros((6, 8), dtype=float)

    var_sql_statements = []
    var_html_tags = []
    var_dangerous_functions = []
    var_import_functions = []
    var_validations = []
    var_objectprototype = []

    sql_statements = np.array([])
    html_tags = np.array([])
    dangerous_functions = np.array([])
    import_functions = np.array([])
    validations = np.array([])
    objectprototype = np.array([])

    for var, snippets in tainted_varsnippets:
        # (variable, found_patterns)
        for snippet in snippets:
            if len(sql_statements) == 0:
                sql_statements = np.append(sql_statements, matchSqlStament(snippet))
            else:
                sql_statements = np.sum([sql_statements, matchSqlStament(snippet)], axis=0)
            if len(html_tags) == 0:
                html_tags = np.append(html_tags, matchHTMLTags(snippet))
            else:
                html_tags = np.sum([html_tags, matchHTMLTags(snippet)], axis=0)
            if len(dangerous_functions) == 0:
                dangerous_functions = np.append(dangerous_functions, matchDangerousFunctions(snippet))
            else:
                dangerous_functions = np.sum([dangerous_functions, matchDangerousFunctions(snippet)], axis=0)
            if len(import_functions) == 0:
                import_functions = np.append(import_functions, matchImportFunctions(snippet))
            else:
                import_functions = np.sum([import_functions, matchImportFunctions(snippet)], axis=0)
            if len(validations) == 0:
                validations = np.append(validations, matchValidations(snippet))
            else:
                validations = np.sum([validations, matchValidations(snippet)], axis=0)
            if len(objectprototype) == 0:
                objectprototype = np.append(objectprototype, matchObjectPrototype(snippet))
            else:
                objectprototype = np.sum([objectprototype, matchObjectPrototype(snippet)], axis=0)

            var_sql_statements.append([var, sql_statements])
            var_html_tags.append([var, html_tags])
            var_dangerous_functions.append([var, dangerous_functions])
            var_import_functions.append([var, import_functions])
            var_validations.append([var, validations])
            var_objectprototype.append([var, objectprototype])

    # Create a matrix of patterns
    matrix = [
        sql_statements,
        html_tags,
        dangerous_functions,
        import_functions,
        validations,
        objectprototype
    ]
    
    # Find the maximum length of the arrays in the matrix
    max_length = max(len(arr) for arr in matrix)
    # Create a new matrix with the same number of rows as the original matrix
    pattern = np.zeros((len(matrix), max_length), dtype=int)
    # Fill the new matrix with values from the original array
    for i, arr in enumerate(matrix):
        pattern[i, :len(arr)] = arr

    # Define the conditions for generating the combined_matrix
    combined_matrix = [
        1 if sql_statements.any() else 0,
        1 if html_tags.any() else 0,
        1 if dangerous_functions.any() else 0,
        1 if import_functions.any() else 0,
        0 if validations[0].any() else 1,
        1 if objectprototype.any() else 0
    ]

    combined_matrix = np.array(combined_matrix).reshape(1, -1)
    combined_matrix = combined_matrix.flatten()

    # Normalize the matrix
    pattern = normalize(pattern, axis=1, norm='l1')

    pattern = pattern.flatten()

    # append the combined matrix to the pattern
    pattern = np.concatenate([pattern, combined_matrix], axis=0)

    return pattern

def preprocess(file, lang):
    match lang:
        case "js":
            variables = extract_variables(file, lang)
        case "php":
            variables = extract_variables(file, lang)
        case _:
            raise Exception("Unsupported language")
        
    if (len(variables) == 0):
        pattern = np.zeros((6, 8), dtype=float)
    else:
        res = begin_preprocessing(variables, file)
        pattern = grab_pattern(res)

    with open('dataprocessing_dataset.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the combined data to the CSV file
        writer.writerow(pattern)  # Split the string and directly write to the CSV file

    #return pattern

