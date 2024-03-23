from preprocessor import preprocess

if __name__ == "__main__":
    js_sample = 'test/samples/javascript/sample.js'
    php_sample = 'test/samples/php/sample.php'

    js_res = preprocess(js_sample, 'js')
    print(js_res)