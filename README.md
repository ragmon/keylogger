# Key logger

Multiplatform key logger application written in Python.

## Features

* catching keyboard keys
* log keys into file
* sending keys chunk over SMTP
* CLI configuration

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to install Python 3.6 and pip packages:
* python-xlib == 0.25
* pyxhook == 1.0.0
* six == 1.12.0


```
sudo apt-get update \
    && sudo apt-get install python3 python3-pip \
    && pip install 'python-xlib==0.25' 'pyxhook==1.0.0' 'six==1.12.0'
```

### Usage

```
usage: Key logger [options]

optional arguments:
  -h, --help            show this help message and exit
  --output-file OUTPUT_FILE
                        Output file for storing keys [default: ./log.txt].
  --rw                  Rewrite output log file if exists [default: false].
```

### Running

Running with development environment.

To run with default configuration:

```
venv/bin/python linux/keylogger.py
```

To run and rewrite log file:

```
venv/bin/python linux/keylogger.py --rw
```

To run and set log file path:

```
venv/bin/python linux/keylogger.py --output-file=./my-log.txt
```

## Built With

* [pyxhook](https://github.com/JeffHoogland/pyxhook) - pyxhook is an implementation of pyhook that works on Linux

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ragmon/keylogger/tags). 

## Authors

* **Arthur Ragimov** - *Initial work* - [ragmon](https://github.com/ragmon)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
