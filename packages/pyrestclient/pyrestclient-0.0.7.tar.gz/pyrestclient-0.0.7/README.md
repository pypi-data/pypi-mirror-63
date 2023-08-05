# RESTClient
The cross-platform tool to work with http.


## Installation
For most users, the recommended method to install is via pip:
```cmd
pip install pyrestclient
```

or from source:

```cmd
python setup.py install
```

## Import
```python
from pyrestclient import RESTClient
```
---

## Changelog
#####0.0.7 (10.03.2020)
- Added query_params to all methods
- POST method was refactored to use .send_request()


#####0.0.6 (01.03.2020)
- removed full_url param. now it will automatically convert url. use "http[s]://site.com" format in methods to use full url.
- code refactoring

#####0.0.5 (01.03.2020)
- query params refactored to use urlencode
- added DELETE method

##### 0.0.4 (27.02.2020)
should_be_bad_request: assert text fixed
...

##### 0.0.1 (9.02.2020)
- initial commit