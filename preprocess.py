from preprocessor import preprocess
from pprint import pprint

if __name__ == "__main__":
    js_sample = 'test/samples/javascript/sample.js'
    php_sample = 'test/samples/php/sample.php'

    js_res = preprocess(js_sample, 'js')
    pprint(js_res)

    php_res = preprocess(php_sample, 'php')
    pprint(php_res)