import requests
import logging
from http.client import HTTPConnection
log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)
HTTPConnection.debuglevel = 1
s = requests.session()
url_login = "https://aquarium.h2o.ai/api/login"
data = {
    "reCaptchaSolution": "",
    "email": "sergio.perez@h2o.ai",
    "password": "FuE9zhYa20!"
}
req1 = s.post(url_login, data=data, verify=False)
print(req1.status_code)
print(req1.cookies.get_dict())







