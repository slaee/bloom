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
        print(s.group())
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
