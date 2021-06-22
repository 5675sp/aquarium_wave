from h2o_wave import Q, ui
import session
import pandas as pd  
from datetime import timedelta
from tzlocal import get_localzone
import pytz
from datetime import datetime
from dateutil import relativedelta

class Lab:
    def __init__(self, identification: str, title: str, type: str, name: str, email: str, state: str, _cloud_state: str, _cloud_resource_id: str, _minutes_remaining: str):
        global _id
        _id += 1
        self.id = f'{_id}'
        self.identification = identification
        self.title = title
        self.name = name
        self.email = email
        self.type = type
        self.state = state
        self._cloud_state = _cloud_state
        self._cloud_resource_id = _cloud_resource_id
        self._minutes_remaining = _minutes_remaining
        

individual_lab_metrics = None



# Create columns for our lab table.
columns = [
    ui.table_column(name='id', label='ID', max_width = '100px'),
    ui.table_column(name='title', label='Title', max_width = '400px'),
    ui.table_column(name='instance type name email', label='Instance Type', max_width = '100px'),
    ui.table_column(name='name', label='Name', max_width = '150px'),
    ui.table_column(name='email', label='Email', max_width = '250px'),
    ui.table_column(name='state', label='State', max_width = '100px'),
    ui.table_column(name='cloud state', label='Cloud State', max_width = '300px'),
    ui.table_column(name='cloud resources id', label='Cloud resources ID', max_width = '400px'),
    ui.table_column(name='minutes remaining', label='Minutes remaining', max_width = '150px'),
]


buttons = None
df = None
labs = None

def active_labs():

    session_holder = session.get_session()
    url_api_active = "https://aquarium.h2o.ai/api/active"
    req = session_holder.get(url_api_active, verify=False)
    jsonRes = req.json()
    global df
    df = pd.DataFrame.from_records(jsonRes)
    rowCount = df.shape[0]  

    global _id
    _id = 0
    # Create some labs
    
    global labs
    labs = [
        Lab(
            identification=str(df.loc[i].at["liId"]),
            title=df.loc[i].at["title"],
            name=df.loc[i].at["instanceType"],
            email=df.loc[i].at["userName"],
            type=df.loc[i].at["userEmail"],
            state=df.loc[i].at["state"],
            _cloud_state=df.loc[i].at["cloudState"],
            _cloud_resource_id=str(df.loc[i].at["cloudResourceId"]),
            _minutes_remaining=minutes_remaining(df.loc[i].at["runningStartTime"], df.loc[i].at["runningDurationMinutes"],df.loc[i].at["waitingStartTime"],df.loc[i].at["waitingDurationMinutes"])) for i in range(rowCount)
    ]
    


    global individual_lab_metrics 
    individual_lab_metrics = [
         ui.separator(label='Active Lab Instance Metrics'),
         ui.textbox(name='liId', label='ID', value='', disabled=True),
         ui.textbox(name='title', label='Title', value='', disabled=True),
         ui.textbox(name='instanceType', label='Instance Type', value='', disabled=True),
         ui.textbox(name='userName', label='Name', value='', disabled=True),
         ui.textbox(name='userEmail', label='Email', value='', disabled=True),
         ui.textbox(name='state', label='State', value='', disabled=True),
         ui.textbox(name='cloudState', label='Cloud state', value='', disabled=True),
         ui.textbox(name='cloudResourceId', label='Cloud resources ID', value='', disabled=True),
         ui.textbox(name='runningDurationMinutes', label='Minutes remaining', value='', disabled=True),
         ui.buttons([ui.button(name='extend',label='Extend', disabled=True)], justify='center'),
         ui.buttons([ui.button(name='end',label='End',disabled=True)], justify='center')
    ]

async def active_labs_table(q: Q):

    _number_of_active_lab_instances = len(df)

    if _number_of_active_lab_instances != 0:

        q.page['activelabs'] = ui.form_card(box='3 1 7 -1', items=[
            ui.text(f'There are {_number_of_active_lab_instances} active lab instances.'),
            ui.button(name='refresh_manage_active_lab_instances_page', label='Refresh Page', primary = True),
            ui.separator('') ,
            ui.inline(items = [
                ui.toggle(name='enable_extend_all_waiting', label = 'Enable extend all waiting',value = None, trigger=True),
                ui.button(name='extend_all_waiting_labs_by_30_minutes', label='Extend all waiting labs by 30 minutes', disabled=True, primary=True)
            ]),
            ui.inline(items = [
                ui.toggle(name='enable_extend_all_running', label = 'Enable extend all running',value = None, trigger=True),
                ui.button(name='extend_all_running_labs_by_30_minutes', label='Extend all running labs by 30 minutes', disabled=True, primary=True)
            ]),
            ui.inline(items = [
                ui.toggle(name='enable_end_button', label = 'Enable end button',value = None, trigger=True),
                ui.button(name='end_all_labs_immediately', label='End all labs immediately (USE WITH CAUTION!)', disabled=True, primary=True)
            ]),
            ui.separator('') ,
            ui.table(
                name='tableofactivelabs',
                columns=columns,
                rows=[ui.table_row(
                    name=lab.id, cells=[lab.identification, lab.title, lab.name, lab.email, lab.type ,lab.state,
                                        lab._cloud_state,lab._cloud_resource_id, lab._minutes_remaining]) for lab in labs],
                downloadable=False,
                height='1000px'
           
            ),
        ])

    else:

        q.page['activelabs'] = ui.form_card(box='3 1 7 -1', items=[
            ui.text(f'There are {_number_of_active_lab_instances} active lab instances.'),
            ui.button(name='refresh_manage_active_lab_instances_page', label='Refresh Page', primary = True),
            ui.separator('') 
        ])
       
    await q.page.save()


async def active_lab_metrics(q: Q, row: int):

    global selected_lab_instance
    selected_lab_instance = row

    global individual_lab_metrics 
    if row == 0: 
        q.page['activeLabButtons'] = ui.form_card(box='10 1 -1 -1', items=individual_lab_metrics)
    else: 
        individual_lab_metrics = [
            ui.separator(label='Lab Metrics/Settings'),
            ui.textbox(name='liId', label='ID', value=str(df.loc[row-1].at["liId"]), disabled=True),
            ui.textbox(name='title', label='Title', value=df.loc[row-1].at["title"], disabled=True),
            ui.textbox(name='instanceType', label='Instance Type', value=df.loc[row-1].at["instanceType"], disabled=True),
            ui.textbox(name='userName', label='Name', value=df.loc[row-1].at["userName"], disabled=True),
            ui.textbox(name='userEmail', label='Email', value=df.loc[row-1].at["userEmail"], disabled=True),
            ui.textbox(name='state', label='State', value=df.loc[row-1].at["state"], disabled=True),
            ui.textbox(name='cloudState', label='Cloud state', value=df.loc[row-1].at["cloudState"], disabled=True),
            ui.textbox(name='cloudResourceId', label='Cloud resources ID', value=str(df.loc[row-1].at["cloudResourceId"]), disabled=True),
            ui.textbox(name='runningDurationMinutes', label='Minutes remaining', value=minutes_remaining(df.loc[row-1].at["runningStartTime"], df.loc[row-1].at["runningDurationMinutes"], df.loc[row-1].at["waitingStartTime"], df.loc[row-1].at["waitingDurationMinutes"]), disabled=True),
            ui.buttons([ui.button(name='extend',label='Extend', primary=True)], justify='center'),
            ui.buttons(items = [ui.button(name='end',label='End', primary=True, disabled=True)], justify='center')
        ]
        
        q.page['activeLabButtons'] = ui.form_card(box='10 1 -1 -1', items=individual_lab_metrics)

    await q.page.save()


def extend_lab_instance(lidId: int):
    session_holder = session.get_session()
    url_api_extend_lab_instance = "https://aquarium.h2o.ai/api/extendLabInstance"
    
    data = {
        "liId": {lidId},
    }
    session_holder.post(url_api_extend_lab_instance, data=data, verify=False)


def end_lab_instance(lidId: int):
    session_holder = session.get_session()
    url_api_end_lab_instance_instance = "https://aquarium.h2o.ai/api/endLabInstance"
    data = {
        "liId": {lidId},
    }
    session_holder.post(url_api_end_lab_instance_instance, data=data, verify=False)

def extend_all_waiting():
    session_holder = session.get_session()
    url_api_extend_all_waiting = "https://aquarium.h2o.ai/api/extendAllWaiting"
    session_holder.post(url_api_extend_all_waiting, verify=False)

def extend_all_running():
    session_holder = session.get_session()
    url_api_extend_all_running = "https://aquarium.h2o.ai/api/extendAllRunning"
    session_holder.post(url_api_extend_all_running, verify=False)

def end_all_lab_instances():
    session_holder = session.get_session()
    url_api_end_all_lab_instances = "https://aquarium.h2o.ai/api/endAll"
    session_holder.post(url_api_end_all_lab_instances, verify=False)

    
def minutes_remaining(running_start_time: int, running_duration_minutes: int, waitingStartTime: int, waitingDurationMinutes: int):  


    if running_start_time == 0:
        if waitingStartTime != 0:
            running_start_time = waitingStartTime
            running_duration_minutes = waitingDurationMinutes
        else: 
            return 'starting'


    zone = str(get_localzone())

    x= datetime.fromtimestamp(running_start_time/1000, pytz.timezone(zone))

    year = int(x.strftime("%Y"))
    month = int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    hour = int(x.strftime("%H"))
    minute = int(x.strftime("%M"))
    second = int(x.strftime("%S"))

    date_1 = datetime(year,month,day,hour,minute,second)


    year = int(x.strftime("%Y"))
    month = int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    hour = int(x.strftime("%H"))
    minute = int(x.strftime("%M"))
    second = int(x.strftime("%S"))

    appropriate_zone = pytz.timezone(zone)
    x = datetime.now(appropriate_zone)

    year = int(x.strftime("%Y"))
    month = int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    hour = int(x.strftime("%H"))
    minute = int(x.strftime("%M"))
    second = int(x.strftime("%S"))

    date_2 = datetime(year,month,day,hour,minute,second)

    total_seconds = date_2 - date_1

    total_minutes = int(total_seconds / timedelta(minutes=1))

    return str(running_duration_minutes-total_minutes)

