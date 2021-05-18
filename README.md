# Page downloader

---
[![python-ci](https://github.com/mnogom/python-project-lvl3/actions/workflows/python-ci.yml/badge.svg)](https://github.com/mnogom/python-project-lvl3/actions/workflows/python-ci.yml)
[![Actions Status](https://github.com/mnogom/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/mnogom/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c9a7a065349f3971e29c/maintainability)](https://codeclimate.com/github/mnogom/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c9a7a065349f3971e29c/test_coverage)](https://codeclimate.com/github/mnogom/python-project-lvl3/test_coverage)

---
### Installation
```commandline
pip3 install --upgrade git+https://github.com/mnogom/python-project-lvl3.git
```

---
### Usage
1. From command line
```commandline
usage: page-loader [-h] [-o OUTPUT] [-d] url

Page loader

positional arguments:
  url                   URL

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        destination for download
  -d, --debug           activate DEBUG mode
```

2. From Python
```python
import page_loader

page_loader.download("https://some_url.com/some_page", "path/to/file")
```

---
### Features
1. Download main page and all relative references
2. Progress bar
3. Debug mode (enable all logger messages)

*See examples below*

---
### Examples
#### Download page
[![asciicast](https://asciinema.org/a/NLQKhnpwyZbIufIZoF0j2AiR0.svg)](https://asciinema.org/a/NLQKhnpwyZbIufIZoF0j2AiR0)

#### Debug mod
[![asciicast](https://asciinema.org/a/tsHzffNYjqKZZZn9JJltp3aDG.svg)](https://asciinema.org/a/NLQKhnpwyZbIufIZoF0j2AiR0)