import requests
import logging
from http.client import HTTPConnection
from h2o_wave import site, Q, ui, graphics as g

s = None
valid = None
def startSession(user_email: str, user_password: str):

    #Login into Aquarium and obtain JSESSIONID to call the following method after: /api/lab (GET)
    #For now SSL will be disabled(verify=False)

    #log = logging.getLogger('urllib3')
    #log.setLevel(logging.DEBUG)
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG)
    #log.addHandler(ch)
    #HTTPConnection.debuglevel = 1

    global s
    s = requests.session()
    url_login = "https://aquarium.h2o.ai/api/login"

    data1 = {
        "reCaptchaSolution": "",
        "email": f'{user_email}',
        "password": f'{user_password}'

    }

        

    responseHolder = s.post(url_login, data=data1, verify=False)

    responseJson = responseHolder.json()
    
    global valid
    valid = responseJson['valid']

    return s

def getSession():
    return s

def getValid():
    return valid 

def topbar():
    url_topbar = "https://aquarium.h2o.ai/api/topbar"
    responseHolder = s.get(url_topbar, verify=False)
    responseJson = responseHolder.json()
    return responseJson
    






async def login(q: Q):


    space1 = f'''
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br></br>
'''

    space2 = f'''
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
'''


    q.page['logo'] = ui.form_card(box= '4 1 -1 -1 ', items=[
        ui.text(space1),
        ui.separator('Aquarium: H2O.ai'),
    ])


    q.page['login'] = ui.form_card(box= '1 1 3 -1', items=[
        ui.text(space2),
        ui.separator('Email'),
        ui.textbox(name='email', label=''),
        ui.separator('Password'),
        ui.textbox(name='password', label='', password=True),
        ui.buttons([ \
            ui.button(name='loginbutton', label='Login', primary=True)
        ], justify='center'),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='createanewaccount', label='Create a new Account', primary=False)
        ], justify='center'),
        ui.buttons([ \
            ui.button(name='iforgotmypassword', label='I forgot my password', primary=False)
        ], justify='center'),
        ui.separator(''),
        ui.separator('Please send us an email if you are having issues logging in.'),

    ])



    await q.page.save()

  
