from numpy.lib.function_base import append
from h2o_wave import Q, ui
import pandas as pd  

from http.client import HTTPConnection, PRECONDITION_FAILED
import session

from datetime import timedelta
from tzlocal import get_localzone
import pytz
from datetime import datetime

class Lab:
    def __init__(self, labId: str, title: str, duration: str):
        self.id = labId
        self.labId = labId
        self.title = title
        self.duration = duration

def api_lab():

    session_holder = session.get_session()
    url_api_lab = "https://aquarium.h2o.ai/api/lab"
    req = session_holder.get(url_api_lab, verify=False)
    jsonRes = req.json()
    df = pd.DataFrame.from_records(jsonRes)
    rowCount = df.shape[0]  

    # Create some labs
    global labs
    labs = [
        Lab(
            labId= str(df.loc[i].at["labId"]),
            title=df.loc[i].at["title"],
            duration=str(df.loc[i].at["durationMinutes"])) for i in range(rowCount)
    ]

async def browse_labs(q: Q):

    global exit 
    exit = True 

    # Create columns for our lab table.
    columns = [
        ui.table_column(name='lab_id', label='Lab ID', max_width = '50px'),
        ui.table_column(name='title', label='Title', max_width = '300px'),
        ui.table_column(name='duration', label='Duration'),
    ]

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



def lab_instance_metrics(selected_lab: int):

    session_holder = session.get_session()
    url_api_lab_number = f'https://aquarium.h2o.ai/api/lab/{str(selected_lab)}'
    req = session_holder.get(url_api_lab_number, verify=False)
    jsonRes = req.json()
    return jsonRes
    


async def individual_lab(q: Q, selected_lab: int):

    global selected_lab_id
    selected_lab_id = selected_lab

    jsonRes = lab_instance_metrics(selected_lab)
    lab_id = jsonRes['labId']

    header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
    body_instructions = f'''{jsonRes['instructions']}'''

    q.page['individualab'] = ui.form_card(
            box='3 1 -1 7',
            items= [
                ui.text(header_instructions),
                ui.text(body_instructions)
            ]
        )
    
    q.page['controller'] = ui.form_card(
            box='3 8 -1 -1',
            items= [
                ui.text('controller')
            ]
        )


    if not jsonRes['state']:
        q.page['controller'].items = [
                ui.buttons([
                    ui.button(name='startLab', label='Start Lab', disabled=False, primary=True),
                    ui.button(name='endLab', label='End Lab', disabled=True)
                ]),
            ]
    
        await q.page.save()
    else: 
        global exit
        exit = False
        while True:
            print('INSIDE WHILE')

            if exit: 
                break;

            jsonRes = lab_instance_metrics(selected_lab_id)

            print('--------------')
            print(jsonRes['title'])
            print('--------------')

            if jsonRes['state'] == '':
                print('EMPTY STATE')
                await individual_lab(q, selected_lab)
                break;

            if jsonRes['state'] != 'running':
                print('1')

                if jsonRes['cloudState'] == 'ROLLBACK_IN_PROGRESS':
                    print('2')
                    
                    lab_id = jsonRes['labId']
                    header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
                    body_instructions = f'''{jsonRes['instructions']}'''
                    lab_instance_instructions = f'''Lab instance ID: **{jsonRes['liId']}** \r\n \r\n\r Lab instance state: **{jsonRes['state']}** \r\n \r\n\r Lab instance cloudState: **{jsonRes['cloudState']}** \r\n \r\n\r Time right now: **{time_now()}** \r\n \r\n\r Time the lab instance was created: **{timestamp_to_human_readable_date(jsonRes['createTime'])}** \r\n \r\n\r Time the lab instance became usable by the user:  \r\n \r\n\r Time remaining for instance use:'''
                    urls_markdown = f''''''
                    q.page['controller'].items = [
                        ui.message_bar(type='error', text=f'Lab failed to start properly. Please try ending and restarting the lab. If this condition persists, please notify your Aquarium administrator. '),
                        ui.buttons([
                            ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                            ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
                        ]),
                        ui.separator(label='Running lab instance information'),
                        ui.text(lab_instance_instructions),
                        ui.text(urls_markdown)
                    ]
                    await q.page.save()
                    break;
                else:
                    print('3')
                    lab_id = jsonRes['labId']
                    header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
                    body_instructions = f'''{jsonRes['instructions']}'''
                    lab_instance_instructions = f'''Lab instance ID: **{jsonRes['liId']}** \r\n \r\n\r Lab instance state: **{jsonRes['state']}** \r\n \r\n\r Lab instance cloudState: **{jsonRes['cloudState']}** \r\n \r\n\r Time right now: **{time_now()}** \r\n \r\n\r Time the lab instance was created: **{timestamp_to_human_readable_date(jsonRes['createTime'])}** \r\n \r\n\r Time the lab instance became usable by the user:  \r\n \r\n\r Time remaining for instance use:'''
                    urls_markdown = f''''''
                    q.page['controller'].items = [
                        ui.progress(label='Please wait, starting the lab may take several minutes...', caption=f'Using lab {str(lab_id)}...'),
                        ui.buttons([
                            ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                            ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
                        ]),
                        ui.separator(label='Running lab instance information'),
                        ui.text(lab_instance_instructions),
                        ui.text(urls_markdown)
                    ]
                    
            elif jsonRes['state'] == 'running': 
                print('4')
                lab_id = jsonRes['labId']
                header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
                body_instructions = f'''{jsonRes['instructions']}'''
                lab_instance_instructions = f'''Lab instance ID: **{jsonRes['liId']}** \r\n \r\n\r Lab instance state: **{jsonRes['state']}** \r\n \r\n\r Lab instance cloudState: **{jsonRes['cloudState']}** \r\n \r\n\r Time right now: **{time_now()}** \r\n \r\n\r Time the lab instance was created: **{timestamp_to_human_readable_date(jsonRes['createTime'])}** \r\n \r\n\r Time the lab instance became usable by the user: **{timestamp_to_human_readable_date(jsonRes['runningStartTime'])}** \r\n \r\n\r Time remaining for instance use: **{timestamp_to_hours_minutes_format(jsonRes['runningStartTime'],jsonRes['durationMinutes'])}**'''
                urls_markdown = f''''''

                outputs = jsonRes['outputs']
                for urls in range(len(outputs)):
                    urls_markdown = f'''{outputs[urls-1]['description']}: <a href="{outputs[urls-1]['value']}" target="_blank">**{outputs[urls-1]['value']}**</a>\r\n\r\n {urls_markdown}'''

                q.page['controller'].items = [
                    ui.message_bar(type='success', text=f'An instance of lab {str(lab_id)} has been created successfully...'),
                    ui.buttons([
                        ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                        ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
                    ]),
                    ui.separator(label='Running lab instance information'),
                    ui.text(lab_instance_instructions),
                    ui.text(urls_markdown),
                ]

            await q.page.save()
            await q.sleep(20)
            print('|---------------------|')
            print(jsonRes)
            print('|---------------------|')

        print('OUTSIDE WHILE')
            


def create_lab_instance():
    session_holder = session.get_session()
    create_api_start_lab = "https://aquarium.h2o.ai/api/startLab"
    lab_id = f'{str(selected_lab_id)}'
    data = {"labId": lab_id}
    session_holder.post(create_api_start_lab, data=data, verify=False)

    return lab_id

def end_lab_instance(labId: int):
    session_holder = session.get_session()
    url_api_end_lab = "https://aquarium.h2o.ai/api/endLab"
    lab_id = f'{str(labId)}'
    data = {"labId": lab_id}
    session_holder.post(url_api_end_lab, data=data, verify=False)

           
async def end_instance(q: Q):
    
    global exit 
    exit = True 
    end_lab_instance(selected_lab_id)
    jsonRes = lab_instance_metrics(selected_lab_id)

    header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
    body_instructions = f'''{jsonRes['instructions']}'''

    q.page['individualab'].items = [
                ui.text(header_instructions),
                ui.text(body_instructions)
            ]
    

    q.page['controller'].items = [
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=False, primary=True),
                ui.button(name='endLab', label='End Lab', disabled=True, primary=False),

            ])
            ]

    await q.page.save()


def timestamp_to_human_readable_date(timestamp: int):
    zone = str(get_localzone())
    timestamp = datetime.fromtimestamp(timestamp/1000, pytz.timezone(zone))
    human_readable_date =  timestamp.strftime("%a, %d %b %Y %I:%M:%S %p %Z")
    return human_readable_date



def time_now():  

    zone = str(get_localzone())
    appropriate_zone = pytz.timezone(zone)
    date = datetime.now(appropriate_zone)
    date = date.strftime("%a, %d %b %Y %I:%M:%S %p %Z")

    return date

  
def timestamp_to_hours_minutes_format(running_start_time: int, running_duration_minutes: int):  

    if running_start_time == 0:
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
    
    total_seconds = (running_duration_minutes-total_minutes) * 60
   
    seconds = total_seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d hour(s), %02d minute(s)" % (hour, minutes)