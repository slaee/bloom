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
    # detect echo $anyvar
    echo_pattern = re.compile(r'echo\s*\$')
    # detect echo function 
    echo_function_pattern = re.compile(r'\b(?:echo|print|printf|sprintf|vprintf|vsprintf|innertext|outerhtml|innerHTML|outerHTML|document.write|document.writeln|document.open|document.close|document.writeIn|document.writeLn|document.writeInLn|text\s*=)\b', re.IGNORECASE)


    # Initialize counts to zero
    html_tag_count = 0
    concatenated_string_count = 0
    if re.search(html_tag_pattern, statement) or re.search(echo_function_pattern, statement):
        html_tag_count = 1
        if hasConcatenation(statement):
            concatenated_string_count = 1
    if re.search(echo_pattern, statement):
        html_tag_count = 1
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
    uri_scheme_pattern = re.compile(r'\b(?:http|https|ftp|ftps|sftp|ssh|scp|file|data|php|phar|expect|zip|rar|tar|gzip|bzip2|compress|zlib|ssh2|expect|data|php|phar|zip|rar|tar|gzip|bzip2|compress|zlib|ssh2)://\b', re.IGNORECASE)
    # Initialize counts to zero
    import_function_count = 0
    uri_scheme_count = 0
    uri_scheme_concatenation_count = 0
    concatenated_string_count = 0
    if re.search(import_function_pattern, statement):
        import_function_count = 1
        if hasConcatenation(statement):
            concatenated_string_count = 1
    if re.search(uri_scheme_pattern, statement):
        uri_scheme_count = 1
        if hasConcatenation(statement):
            uri_scheme_concatenation_count = 1
    # Return a single list containing the count of patterns found
    return [import_function_count, concatenated_string_count, uri_scheme_count, uri_scheme_concatenation_count]

def matchValidations(statement):
    # Define a pattern to match validation functions
    validation_function_pattern = re.compile(r'\b(?:filter_var|filter_input|filter_var_array|filter_input_array|preg_match|preg_match_all|htmlspecialchars|preg_replace|preg_replace_callback|preg_replace_callback_array|preg_split|preg_grep|preg_filter|preg_last_error|test|match|validate|check|verify|sanitize|clean|escape|encode|decode|hash|encrypt|decrypt|secure|validate|check|verify|sanitize|clean|escape|encode|decode|hash|encrypt|decrypt|secure)\b', re.IGNORECASE)
    operator_check_pattern = re.compile(r'\b(?:==|===|!=|!==|<=|>=|<|>)\b')
    if_statement_pattern = re.compile(r'\bif\s*\(\s*.*\s*\)')
    # Initialize counts to zero
    validation_function_count = 0
    operator_check_count = 0
    if_statement_count = 0
    if re.search(if_statement_pattern, statement):
        if_statement_count = 1
    if re.search(validation_function_pattern, statement):
        validation_function_count = 1
    if re.search(operator_check_pattern, statement):
        operator_check_count = 1
    return [if_statement_count, validation_function_count, operator_check_count]

def matchPrototype(statement):
    # Compile regex patterns for each category and prototype pollution
    object_type_patterns = re.compile(r'Object\.(assign|getOwnPropertyDescriptor|getOwnPropertyDescriptors|getOwnPropertyNames|getOwnPropertySymbols|is|preventExtensions|seal|create|assign\s*\(.+__proto__\s*:|create\s*\(.+__proto__\s*)')
    object_prototype_patterns = re.compile(r'Object\.prototype\.(constructor|__defineGetter__|__defineSetter__|hasOwnProperty|__lookupGetter__|__lookupSetter__|isPrototypeOf|setPrototypeOf|propertyIsEnumerable|toString|valueOf|__proto__|toLocaleString)')
    string_type_patterns = re.compile(r'String\.(fromCharCode|fromCodePoint|raw)')
    string_prototype_patterns = re.compile(r'String\.prototype\.(constructor|anchor|big|blink|bold|charAt|charCodeAt|codePointAt|concat|endsWith|fontcolor|fontsize|fixed|includes|indexOf|italics|lastIndexOf|link|localeCompare|match|matchAll|normalize|padEnd|padStart|repeat|replace|search|slice|small|split|strike|sub|substr|substring|sup|startsWith|toString|trim|trimStart|trimLeft|trimEnd|trimRight|toLocaleLowerCase|toLocaleUpperCase|toLowerCase|toUpperCase|valueOf|replaceAll|at)')
    number_type_patterns = re.compile(r'Number\.(isFinite|isInteger|isNaN|isSafeInteger|parseFloat|parseInt|MAX_VALUE|MIN_VALUE|NaN|NEGATIVE_INFINITY|POSITIVE_INFINITY|MAX_SAFE_INTEGER|MIN_SAFE_INTEGER|EPSILON)')
    number_prototype_patterns = re.compile(r'Number\.prototype\.(constructor|toExponential|toFixed|toPrecision|toString|valueOf|toLocaleString)')
    array_type_patterns = re.compile(r'Array\.(isArray|from|of)')
    array_prototype_patterns = re.compile(r'Array\.prototype\.(constructor|concat|copyWithin|fill|find|findIndex|lastIndexOf|pop|push|reverse|shift|unshift|slice|sort|splice|includes|indexOf|join|keys|entries|values|forEach|filter|flat|flatMap|map|every|some|reduce|reduceRight|toLocaleString|toString|at)')
    function_type_patterns = re.compile(r'Function\.(arguments|caller)')
    function_prototype_patterns = re.compile(r'Function\.prototype\.(constructor|apply|bind|call|toString)')
    boolean_type_patterns = re.compile(r'Boolean\.(prototype)')
    boolean_prototype_patterns = re.compile(r'Boolean\.prototype\.(constructor|toString|valueOf)')
    json_parse_patterns = re.compile(r'JSON\.parse\s*\(.+__proto__\s*:')
    other_type_patterns = re.compile(r'Map\.prototype\.(set|get|delete)\s*\(.+__proto__\s*:' 
                                r'|Set\.prototype\.(add|delete)\s*\(.+__proto__\s*:' 
                                r'|RegExp\.prototype\.(exec|test)\s*\(.+__proto__\s*:')

    # Initialize counts for each category and prototype pollution
    object_type_patterns_count = 0
    object_prototype_patterns_count = 0
    string_type_patterns_count = 0
    string_prototype_patterns_count = 0
    number_type_patterns_count = 0
    number_prototype_patterns_count = 0
    array_type_patterns_count = 0
    array_prototype_patterns_count = 0
    function_type_patterns_count = 0
    function_prototype_patterns_count = 0
    boolean_type_patterns_count = 0
    boolean_prototype_patterns_count = 0
    json_parse_patterns_count = 0
    other_type_patterns_count = 0

    # Count occurrences of patterns for each category
    if re.search(object_type_patterns, statement):
        object_type_patterns_count += 1
    if re.search(object_prototype_patterns, statement):
        object_prototype_patterns_count += 1
    if re.search(string_type_patterns, statement):
        string_type_patterns_count += 1
    if re.search(string_prototype_patterns, statement):
        string_prototype_patterns_count += 1
    if re.search(number_type_patterns, statement):
        number_type_patterns_count += 1
    if re.search(number_prototype_patterns, statement):
        number_prototype_patterns_count += 1
    if re.search(array_type_patterns, statement):
        array_type_patterns_count += 1
    if re.search(array_prototype_patterns, statement):
        array_prototype_patterns_count += 1
    if re.search(function_type_patterns, statement):
        function_type_patterns_count += 1
    if re.search(function_prototype_patterns, statement):
        function_prototype_patterns_count += 1
    if re.search(boolean_type_patterns, statement):
        boolean_type_patterns_count += 1
    if re.search(boolean_prototype_patterns, statement):
        boolean_prototype_patterns_count += 1
    if re.search(json_parse_patterns, statement):
        json_parse_patterns_count += 1
    if re.search(other_type_patterns, statement):
        other_type_patterns_count += 1

    # Return counts as a list in the desired order
    return [object_type_patterns_count, string_type_patterns_count, number_type_patterns_count, array_type_patterns_count, 
            function_type_patterns_count, boolean_type_patterns_count, json_parse_patterns_count, other_type_patterns_count]