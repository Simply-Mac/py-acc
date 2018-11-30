Introduction
============

acc is a Python 3.x module designed to work with the AppleCare Connect (ACC) API. It is meant to be used as a means for 
AppleCare Resellers to be able to enroll AppleCare+ plans for their customers.  

Please consult the ACC API documentation ([UAT](https://applecareconnect.apple.com/api-docs/accuat/html/WSImpManual.html?user=reseller),
[Production](https://applecareconnect.apple.com/api-docs/acc/html/WSReference.html?user=reseller)) for more details.

This is being open-sourced to gather feedback on how to make the module better and benefit the community at large.


Requirements
============

- Python 3.x or later
- Contents of requirements.txt in your Python environment
- ACC client certs (UAT/PROD) signed by Apple


Usage
=====

#### UAT Example

```python
# Get device details
import os
from py-acc import acc
os.environ['ACC_SHIPTO'] = '0000123456'
os.environ['ACC_ENV'] = 'UAT'
os.environ['ACC_UAT_CERT'] = '/path/to/acc/uat/cert.pem'
os.environ['ACC_UAT_PRIVATE_KEY'] = '/path/to/acc/uat/cert_private_key.pem'

post_data, full_response, error_code, error_message, call_type = acc.three_sixty_lookup(device_id='C021T5AFAK3')
```


#### PROD Example

```python
# Get device details
import os
from py-acc import acc
os.environ['ACC_SHIPTO'] = '0000123456'
os.environ['ACC_ENV'] = 'PROD'
os.environ['ACC_UAT_CERT'] = '/path/to/acc/prod/cert.pem'
os.environ['ACC_UAT_PRIVATE_KEY'] = '/path/to/acc/prod/cert_private_key.pem'

post_data, full_response, error_code, error_message, call_type = acc.three_sixty_lookup(device_id='C021T5AFAK3')
```


Credits
=====
- [Meraki Dashboard API for Python](https://github.com/meraki/dashboard-api-python)
- [Python library for communicating with GSX Web Services API](https://github.com/filipp/py-gsxws)
