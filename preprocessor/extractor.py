import os
import subprocess

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JS_VARIABLE_EXTRACTOR = os.path.join(ROOT_PATH, "ast", "variables_extractor.js")
PHP_VARIABLE_EXTRACTOR = os.path.join(ROOT_PATH, "ast", "variables_extractor.php")

def extract_variables(file, lang):
    match lang:
        case "js":
            cmd = ["node", JS_VARIABLE_EXTRACTOR, "module", file]
        case "php":
            cmd = ["php", PHP_VARIABLE_EXTRACTOR, file]
        case _:
            raise Exception("Unsupported language")
        
    res = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode("utf-8")
    res = res.split(',')
    return res        
    
