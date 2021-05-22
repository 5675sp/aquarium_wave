from h2o_wave import main, app, Q, ui
import json
import requests
import pandas as pd  

from http.client import HTTPConnection, PRECONDITION_FAILED
import session

import time 
import threading

class Lab:
    def __init__(self, labId: str, title: str, duration: str):
        global _id
        _id += 1
        self.id = f'{_id}'
        self.labId = labId
        self.title = title
        self.duration = duration

# Create some labs(start empty)
labs = None

end = False

# Create columns for our lab table.
columns = [
    ui.table_column(name='lab_id', label='Lab ID', max_width = '50px'),
    ui.table_column(name='title', label='Title', max_width = '300px'),
    ui.table_column(name='duration', label='Duration'),
]


def browselabsmethod():

    s = session.getSession()
    url_browse_labs = "https://aquarium.h2o.ai/api/lab"
    req2 = s.get(url_browse_labs, verify=False)
    jsonRes = req2.json()
    global df
    df = pd.DataFrame.from_records(jsonRes)
    rowCount = df.shape[0]  

    global _id
    _id = 0
    # Create some labs
    global labs
    labs = [
        Lab(
            labId= str(df.loc[i].at["labId"]),
            title=df.loc[i].at["title"],
            duration=str(df.loc[i].at["durationMinutes"])) for i in range(rowCount)
    ]


async def browselabs(q: Q):

    q.page['visiablelabs'] = ui.form_card(box='3 1 -1 -1', items=[
        ui.table(
            name='labs',
            columns=columns,
            rows=[ui.table_row(
                name=lab.id, cells=[lab.labId, lab.title,lab.duration+' minutes']) for lab in labs],
            downloadable=False,
            height='1000px'
        ),
    ])

    await q.page.save()



def individualInstructionsMethod(selectedLab: int):
    global update_value
    update_value = selectedLab
    global selected_lab_id
    s = session.getSession()
    lab = df.loc[selectedLab - 1].at["labId"] 
    selected_lab_id = lab
    url_lab_instructions = f'https://aquarium.h2o.ai/api/lab/{str(lab)}'
    req = s.get(url_lab_instructions, verify=False)
    global jsonRes
    jsonRes = req.json()
    global header_markdown
    header_markdown = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
    global body_markdown
    body_markdown = f'''{jsonRes['instructions']}'''

    return jsonRes['state']
    

async def individualLab(q: Q, selectedLab: int, starting: str):

    if not starting:
        q.page['individualab'] = ui.form_card(
            box='3 1 -1 -1',
            items=[
                ui.text(header_markdown),
                ui.text(body_markdown),
                ui.buttons([
                    ui.button(name='startLab', label='Start Lab', disabled=False, primary=True),
                    ui.button(name='endLab', label='End Lab', disabled=True)
            ]),
            ]
        )
        await q.page.save()
    elif starting == 'running':
        q.page['individualab'] = ui.form_card(
            box='3 1 -1 -1',
            items= [
            ui.text(header_markdown),
            ui.text(body_markdown),
            ui.message_bar(type='success', text=f'An instance of lab {str(selected_lab_id)} has been created successfully...'),
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
            ]),
            ui.separator(label='Running lab instance information'),
            ui.text(lab_instance_metrics),
            ui.text(urls_markdown),
            ]
        )
        await q.page.save()
    else:
        q.page['individualab'] = ui.form_card(
            box='3 1 -1 -1',
            items= [
            ui.text(header_markdown),
            ui.text(body_markdown),
            ui.progress(label='Please wait, starting the lab may take several minutes...', caption=f'Using lab {str(selected_lab_id)}...'),
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
            ]),
            ui.separator(label='Running lab instance information'),
            ui.text(lab_instance_metrics),
            ui.text(urls_markdown),
            ]
        )
        await q.page.save()


def createLabInstanceMethod():

    s = session.getSession()
    create_lab_instance = "https://aquarium.h2o.ai/api/startLab"
    lab_id = f'{str(selected_lab_id)}'
    data = {"labId": lab_id}
    s.post(create_lab_instance, data=data, verify=False)

def endLabInstanceMethod(labId: int):

    s = session.getSession()
    end_lab_instance = "https://aquarium.h2o.ai/api/endLab"
    lab_id = f'{str(labId)}'
    data = {"labId": lab_id}
    s.post(end_lab_instance, data=data, verify=False)

           
def getInstanceMetrics(labId: int):

    s = session.getSession()
    url_lab = "https://aquarium.h2o.ai/api/lab/" + str(labId)
    req = s.get(url_lab, verify=False)
    jsonRes = req.json()

    return jsonRes



async def update(q: Q):
    status = False

    s = session.getSession()
    url_lab = "https://aquarium.h2o.ai/api/lab/" + str(selected_lab_id)
    req = s.get(url_lab, verify=False)
    jsonRes = req.json()
    check_if_runnning = jsonRes['starting']
    
  
    while check_if_runnning: 
        
        if status or end == True:
            break

  
        req = s.get(url_lab, verify=False)
        jsonRes = req.json()
        outputs = jsonRes['outputs']

        global lab_instance_metrics
        lab_instance_metrics = f'''
Lab instance ID: {jsonRes['liId']}

Lab instance state: {jsonRes['state']}

Lab instance cloudState: {jsonRes['cloudState']}

Time right now: 

Time the lab instance was created: {jsonRes['createTime']}

Time the lab instance became usable by the user: {jsonRes['runningStartTime']}

Time remaining for instance use: 
'''
        

        if len(outputs) == 0:
            status = False
            global urls_markdown
            urls_markdown = f''''''
            q.page['individualab'].items = [
            ui.text(header_markdown),
            ui.text(body_markdown),
            ui.progress(label='Please wait, starting the lab may take several minutes...', caption=f'Using lab {str(selected_lab_id)}...'),
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
            ]),
            ui.separator(label='Running lab instance information'),
            ui.text(lab_instance_metrics),
            ui.text(urls_markdown),
            ]
        else: 
            status = True
            for urls in range(len(outputs)):
                urls_markdown = f'''{urls_markdown}{outputs[urls-1]['description']}: {outputs[urls-1]['value']}\r\n\r\n'''


            q.page['individualab'].items = [
            ui.text(header_markdown),
            ui.text(body_markdown),
            ui.message_bar(type='success', text=f'An instance of lab {str(selected_lab_id)} has been created successfully...'),
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
            ]),
            ui.separator(label='Running lab instance information'),
            ui.text(lab_instance_metrics),
            ui.text(urls_markdown),
            ]

        await q.page.save()
        await q.sleep(20)


async def createInstance(q: Q):

   
    await update(q)
    

async def endInstance(q: Q):

    global end
    end = True 
    
    endLabInstanceMethod(selected_lab_id)

    q.page['individualab'].items = [
            ui.text(header_markdown),
            ui.text(body_markdown),
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=False, primary=True),
                ui.button(name='endLab', label='End Lab', disabled=True, primary=False),

            ])
            ]

    await q.page.save()





---------



   if not q.client.initialized:
        q.client.initialized = True
        session.startSession()
        await setup_page(q)
        await dashboard.dashboard(q) #dasboard 

    if q.args.managelabs:
        await deleteCards(q)
        manage_labs.managelabsmethod()
        await manage_labs.manageLabsSettings(q)
        await manage_labs.labMetrics(q, 0)
    
    if q.args.browselabs: # browse Labs 
        await deleteCards(q)
        browse_labs.browselabsmethod()
        await browse_labs.browselabs(q)

    if q.args.dashboard:
        await deleteCards(q)
        await dashboard.dashboard(q) #dasboard 

    if q.args.tableoflabs:
        await manage_labs.labMetrics(q, (int(q.args.tableoflabs[0])))
        
    if q.args.editLab:
        await manage_labs.popSettings(q)

    if q.args.labs: #Particular browse lab -> Select a lab -> Request Lab Information -> 
        await deleteCards(q)
        await browse_labs.individualLab(q, (int(q.args.labs[0])))
        
    if q.args.startLab:
        lab_id = browse_labs.createLabInstanceMethod()
        await browse_labs.individualLab(q,lab_id)
       
    if q.args.endLab:
        await browse_labs.endInstance(q)

    if q.args.downloadInstancesCsv:
        await deleteCards(q)
        await download_instances_csv.csvTable(q)


    
        s = session.getSession()
    csv_url= "https://aquarium.h2o.ai/api/downloadInstancesCsv"
    req = s.get(csv_url, verify=False)
    resPonse = req.text


read_file = pd.read_csv('csv_file.txt', header = None)
    read_file.columns = parts 
    read_file.to_csv('original_csv_file.csv', index=None)




    f = open('csv_file.txt', 'r')
    line_count = 0
    for line in f:
        
        if line != "\n":
            line_count += 1

      for x in range(line_count-101):
                f.readline()



                 columnsHeader = "liId,batchId,userId,firstName,lastName,email,title,instanceType,createReason,endReason,state,cloudState,cloud,cloudRegion,createTime,submitted,startingStartTime,waitingStartTime,runningStartTime,endTime,date,labSeconds,cloudHours,cloudCostPerHour,cloudCost"
    resPonse = resPonse.replace(columnsHeader,'')   

    f = open('csv_file.txt', 'w')  
    f.write(resPonse)  

 

    parts = columnsHeader.split(',')
    n = len(parts)
    parts[n-1] = 'cloudCost'

    listColumns = parts

    read_file = pd.read_csv('csv_file.txt', header = None)
    read_file.columns = listColumns 
    read_file.to_csv('original_csv_file.csv', index=None)




     global lock
    if lock:
        await session.login(q)

   
    if q.args.loginbutton:

        email = q.args.email
        password = q.args.password
        session.startSession(email, password)
        valid = session.getResponse()
        
      
        if not q.client.initialized and valid == True:
            print('inside valid true')
            q.client.initialized = True
            lock = False
            del q.page['poplogin']
            await setup_page(q)
            await dashboard.dashboard(q) #dasboard 








            import requests
import logging
from http.client import HTTPConnection
from h2o_wave import Q, ui

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

async def login(q: Q):

   q.page['credentials'] = ui.meta_card(
        box='',
        layouts=[
            ui.layout(
                breakpoint='xs',
                width='1200px',
                zones=[
                    
                    ui.zone('login', align='center', justify='center', size='1000px'),
             
                ]
            )
        ]
    )

   q.page['logo'] = ui.header_card(
        box='logo',
        title='Aquarium',
        subtitle='H2O.ai',
    )


   space = '''</br>'''
    
   q.page['login'] = ui.form_card(
        box=ui.box('login', width='30%'),
        items=[
            ui.text(space),
            ui.separator('Aquarium'),
            ui.textbox(name='email', label='Email'),
            ui.textbox(name='password', label='Password', password=True),
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
        ]
    )

   await q.page.save()
