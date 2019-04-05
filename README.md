# Key logger

Multiplatform key logger application written in Python.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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

### Running

```
venv/bin/python linux/keylogger.py
```

## Built With

* [pyxhook](https://github.com/JeffHoogland/pyxhook) - pyxhook is an implementation of pyhook that works on Linux

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ragmon/keylogger/tags). 

## Authors

* **Arthur Ragimov** - *Initial work* - [ragmon](https://github.com/ragmon)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
