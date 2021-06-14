import requests
from h2o_wave import Q, ui

session_holder = None
valid = None
def start_session(user_email: str, user_password: str):

    global session_holder
    session_holder = requests.session()
    url_login = "https://aquarium.h2o.ai/api/login"

    data = {
        "reCaptchaSolution": "",
        "email": f'{user_email}',
        "password": f'{user_password}'

    }

    responseHolder = session_holder.post(url_login, data=data, verify=False)

    responseJson = responseHolder.json()
    
    global valid
    valid = responseJson['valid']

    print(type(session_holder))

    return session_holder

def get_session():
    return session_holder

def get_valid():
    return valid 

def top_bar():
    url_api_top_bar = "https://aquarium.h2o.ai/api/topbar"
    responseHolder = session_holder.get(url_api_top_bar, verify=False)
    responseJson = responseHolder.json()
    return responseJson
    
global space_one
space_one = f'''
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

global space_two
space_two = f'''
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
'''

async def login(q: Q):
  
    q.page['login'] = ui.form_card(box= '1 1 3 -1', items=[
        ui.text(space_two),
        ui.separator('Email'),
        ui.textbox(name='email', label=''),
        ui.separator('Password'),
        ui.textbox(name='password', label='', password=True),
        ui.buttons([ \
            ui.button(name='loginbutton', label='Login', primary=True)
        ], justify='center'),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='iforgotmypassword', label='I forgot my password', primary=False)
        ], justify='center'),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='back_from_login_page', label='Back', primary=True)
        ], justify='center')
    ])

    await q.page.save()

async def login_failed(q: Q):

    q.page['login'] = ui.form_card(box= '1 1 3 -1', items=[
        ui.text(space_two),
        ui.message_bar(type='error', text='Invalid credentials'),
        ui.separator('Email'),
        ui.textbox(name='email', label=''),
        ui.separator('Password'),
        ui.textbox(name='password', label='', password=True),
        ui.buttons([ \
            ui.button(name='loginbutton', label='Login', primary=True)
        ], justify='center'),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='iforgotmypassword', label='I forgot my password', primary=False)
        ], justify='center'),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='back_from_login_page', label='Back', primary=True)
        ], justify='center')
    ])

    await q.page.save()

global space_three
space_three = f'''
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
'''

async def login_options(q: Q):

    q.page['logo'] = ui.form_card(box= '4 1 -1 -1 ', items=[
        ui.text(space_one),
        ui.separator('Aquarium: H2O.ai'),
    ])

    q.page['login'] = ui.form_card(box= '1 1 3 -1', items=[
        ui.text(space_three),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='option_one_openid', label='Login using OpenId', primary=True)
        ], justify='center'),
        ui.buttons([ \
            ui.button(name='option_two_create_account', label='Create a new Account', primary=True)
        ], justify='center'),
        ui.separator(''),
        ui.separator('Please send us an email if you are having issues logging in.'),

    ])
    await q.page.save()
  

global space_four
space_four = f'''
</br></br>
</br></br>
</br></br>
</br></br>
</br></br>
'''
async def creat_account(q: Q):
  
    q.page['login'] = ui.form_card(box= '1 1 3 -1', items=[
        ui.text(space_four),
        ui.separator('First Name'),
        ui.textbox(name='first_name', label='', required=True),
        ui.separator('Last Name'),
        ui.textbox(name='last_name', label='', required=True),
        ui.separator('Organization'),
        ui.textbox(name='organization', label='', required=True),
        ui.separator('Country'),
        ui.textbox(name='country', label='', required=True),
        ui.separator('Email'),
        ui.textbox(name='create_account_email', label='', required=True),
        ui.separator('Mobile'),
        ui.textbox(name='mobile', label='', required=True, mask='+9 (999) 999 - 9999'),
        ui.buttons([ \
            ui.button(name='verify', label='Create account and verify mobile', primary=True)
        ], justify='center'),
        ui.separator(''),
        ui.buttons([ \
            ui.button(name='back_from_create_account_page', label='back', primary=True)
        ], justify='center'),
    ])

    await q.page.save()
