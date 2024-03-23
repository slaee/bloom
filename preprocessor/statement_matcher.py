import re

"""
Pattern for string concatenation:
    case 1 and case 2
    optionalGroup( ( " or ' or ` ) \s* ( + or . ) \s*) anychar_except( " or ' or ` ) optionalGroup( \s* ( + or . ) \s* ( " or ' or ` ) )

    case 3 
    let strings = requiredGroup ( " or ` ) anychar requiredGroup ( " or ` )
    - strings contains $anychar or ${anychar}
    - consider a string like "SELECT * FROM users WHERE user_id = '$userid1_2'"
    - consider a string like `SELECT * FROM users WHERE user_id = ${userid1_2}`
"""
def hasConcatenation(statement):
    case1 = re.compile(r'(["\'`]\s*[+\.]\s*?)\(?[a-zA-Z0-9_$]\)?[^"\'`]')
    case2 = re.compile(r'[^"\'`]\(?[a-zA-Z0-9_$]\)?\s*[+\.]\s*?["\'`]')
    case3 = re.compile(r'(\$\w+)|(\$\{\w+\})')
    grab_string = re.compile(r'(["`]).*?\1')
    string = re.finditer(grab_string, statement)
    # check for case 1 and case 2
    if re.search(case1, statement) or re.search(case2, statement):
        return True
    # if no match found in case 1 and case 2, check for case 3
    for s in string:
        if re.search(case3, s.group()):
            return True
    # if not match found in case 1-3, return False
    return False

# This will match SQL syntax and concatenated strings in a given SQL statement.
def matchSqlStament(statement):
    sql_syntax_pattern = re.compile(r'\b(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|AND|OR)\b', re.IGNORECASE)
    # Initialize counts to zero
    sql_syntax_count = 0
    concatenated_string_count = 0
    if re.search(sql_syntax_pattern, statement):
        sql_syntax_count = 1
        if hasConcatenation(statement):
            concatenated_string_count = 1
    # Return a single list containing the count of patterns found
    return [sql_syntax_count, concatenated_string_count]

def matchHTMLTags(statement):
    # Define a pattern to match HTML tags
    html_tag_pattern = re.compile(r'<.*?>')
    # Initialize counts to zero
    html_tag_count = 0
    concatenated_string_count = 0
    if re.search(html_tag_pattern, statement):
        html_tag_count = 1
        if hasConcatenation(statement):
            concatenated_string_count = 1
    # Return a single list containing the count of patterns found
    return [html_tag_count, concatenated_string_count]

def matchDangerousFunctions(statement):
    # Define a pattern to match dangerous functions
    dangerous_function_pattern = re.compile(r'\b(?:exec|system|shell_exec|passthru|eval|assert|create_function|popen|proc_open|preg_replace|unserialize|Function|ReflectionFunction|setTimeout|setInterval|spawn|execSync|execFile)\b', re.IGNORECASE)
    # Initialize counts to zero
    dangerous_function_count = 0
    concatenated_string_count = 0
    if re.search(dangerous_function_pattern, statement):
        dangerous_function_count = 1
        if hasConcatenation(statement):
            concatenated_string_count = 1
    # Return a single list containing the count of patterns found
    return [dangerous_function_count, concatenated_string_count]

def matchImportFunctions(statement):
    # Define a pattern to match import functions
    import_function_pattern = re.compile(r'\b(?:require|require_once|include|include_once|import|file_get_contents|fopen|fread|fclose|readfile|parse_ini_file|readFileSync|readFile)\b', re.IGNORECASE)
    # Initialize counts to zero
    import_function_count = 0
    concatenated_string_count = 0
    if re.search(import_function_pattern, statement):
        import_function_count = 1
        if hasConcatenation(statement):
            concatenated_string_count = 1
    # Return a single list containing the count of patterns found
    return [import_function_count, concatenated_string_count]

def matchValidationFunctions(statement):
    # Define a pattern to match validation functions
    validation_function_pattern = re.compile(r'\b(?:filter_var|filter_input|filter_var_array|filter_input_array|preg_match|preg_match_all|preg_replace|preg_replace_callback|preg_replace_callback_array|preg_split|preg_grep|preg_filter|preg_last_error|is_numeric|is_int|is_float|is_string|ctype_digit|ctype_alpha|test|match|validate|check|verify|sanitize|clean|escape|encode|decode|hash|encrypt|decrypt|secure|validate|check|verify|sanitize|clean|escape|encode|decode|hash|encrypt|decrypt|secure)\b', re.IGNORECASE)
    operator_check_pattern = re.compile(r'\b(?:==|===|!=|!==|<=|>=|<|>)\b')
    # Initialize counts to zero
    validation_function_count = 0
    operator_check_count = 0
    concatenated_string_count = 0
    if re.search(validation_function_pattern, statement):
        validation_function_count = 1
    if re.search(operator_check_pattern, statement):
        operator_check_count = 1
    return [validation_function_count, operator_check_count]
                                             

def matchPrototypePollution(statement):
    # Define a pattern to match prototype pollution
    prototype_assignment_pattern = re.compile(r'Object\.prototype\.[\w$]+\s*=\s*.+')
    object_assignment_pattern = re.compile(r'([\w$]+|Object)\s*=\s*{[\w$]+:\s*.+,')
    object_manipulation_pattern = re.compile(r'Object\.(assign|setPrototypeOf)\s*\([\w$]+\s*,\s*{[\w$]+:\s*.+}\s*\)')
    json_parse_pattern = re.compile(r'JSON\.parse\s*\([\w$]+\s*\)')
    property_check_pattern = re.compile(r'\bif\s*\(\s*!\s*[\w$]+\s*\.hasOwnProperty\s*\(\s*[\w$]+\s*\)\s*\)\s*{')
    default_object_assignment_pattern = re.compile(r'[\w$]+\s*=\s*[\w$]+\s*\|\|\s*{};')
    dynamic_property_assignment_pattern = re.compile(r'[\w$]+\s*\[\s*[\w$]+\s*\]\s*=\s*.+')
    array_copy_pattern = re.compile(r'const\s+[\w$]+\s*=\s*[\w$]+\s*\[\s*[\w$]+\s*\];')
    
    prototype_assignment_count = 0
    object_assignment_count = 0
    object_manipulation_count = 0
    json_parse_count = 0
    property_check_count = 0
    default_object_assignment_count = 0
    dynamic_property_assignment_count = 0
    array_copy_count = 0

    if re.search(prototype_assignment_pattern, statement):
        prototype_assignment_count += 1
    if re.search(object_assignment_pattern, statement):
        object_assignment_count += 1
    if re.search(object_manipulation_pattern, statement):
        object_manipulation_count += 1
    if re.search(json_parse_pattern, statement):
        json_parse_count += 1
    if re.search(property_check_pattern, statement):
        property_check_count += 1
    if re.search(default_object_assignment_pattern, statement):
        default_object_assignment_count += 1
    if re.search(dynamic_property_assignment_pattern, statement):
        dynamic_property_assignment_count += 1
    if re.search(array_copy_pattern, statement):
        array_copy_count += 1

    return [prototype_assignment_count, object_assignment_count, object_manipulation_count,
            json_parse_count, property_check_count, default_object_assignment_count,
            dynamic_property_assignment_count, array_copy_count]