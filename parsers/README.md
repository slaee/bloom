# Building the lexers and parsers

### Requirements
- ANTLR4 version 4.13.1
- python packages
  - antlr4-python3-runtime==4.13.1
  - matplotlib
  - networkx
- Docker

### Building the lexers and parsers

To build the lexers and parsers run the following:
```
python3 transformGrammar.py
antlr4 -Dlanguage=Python3 *.g4
```

### Running the tests
run the main.py for examples
```
python3 main.py
```

For mor info: https://github.com/antlr/antlr4/blob/master/doc/python-target.md