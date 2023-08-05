# enclosed

Python library that parses text and generates closed/enclosed tokens

## About

This package provides a Python library that will parse an input text and produce tokens enclosed or not enclosed within an _open_symbol_ and _close_symbol_ .


## Install

```bash
pip3 install --user enclosed
```

## How to use
```python
from enclosed import Parser

print(Parser().tokenize("Hello {World}"))
```
