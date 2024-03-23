# Bloom 
A new intelligent web vulnerability scanner framework with static analysis utilizing machine learning.

# Development

```bash
git clone https://github.com/slaee/bloom.git -b dev
```

## ANTLR4 Build

You can build docker image from source code locally. 
```shell
cd antlr4
docker build -t antlr/antlr4 --platform linux/amd64 .
```
    


## ANTLR4 Run

For security reasons is **ANTLR4 Docker image** designed to run in the current folder only, so a container doesn't have any access to any other folders on a host system. Since this is a transparent call of Docker image from command line, where new files are generated, it is also a good idea to execute code inside a Docker as a non root user and match it to the host caller.

Calling a dockerized ANTLR4 image can look like this:

Sample:
```shell
cd parsers/php/Python3
docker run --rm -u $(id -u ${USER}):$(id -g ${USER}) -v `pwd`:/work antlr/antlr4 -Dlanguage=Python3 *.g4
```

## Integration as alias
```shell
alias antlr4='docker run -it -u $(id -u ${USER}):$(id -g ${USER}) -v $(pwd):/work antlr/antlr4 $@'
```

For WINDOWS to integrate an alias you must use git bash and add the above alias at the end of ~/.bashrc line:
```shell
nano ~/.bashrc
# add the above alias at the end of the file then run:
source ~/.bashrc
```

      
## ANTLR4 Test
```shell
cd parsers/php
antlr4 -Dlanguage=Python3 *.g4
```

## Create virtual environment
```shell
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies
```shell
pip install -r requirements.txt
```

Once you have completed the above steps, you can start the application by reading the README.md file from `parsers` folder.


# References
Latest antlr4 docker image installation: https://github.com/antlr/antlr4/tree/master/docker
