from numpy.lib.function_base import append
from h2o_wave import Q, ui
import pandas as pd  

from http.client import HTTPConnection, PRECONDITION_FAILED
import session



class Lab:
    def __init__(self, labId: str, title: str, duration: str):
        self.id = labId
        self.labId = labId
        self.title = title
        self.duration = duration

def browselabsmethod():

    s = session.getSession()
    url_browse_labs = "https://aquarium.h2o.ai/api/lab"
    req2 = s.get(url_browse_labs, verify=False)
    jsonRes = req2.json()
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


async def browselabs(q: Q):

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



def labInstanceMetrics(selectedLab: int):

    s = session.getSession()
    url_lab_instructions = f'https://aquarium.h2o.ai/api/lab/{str(selectedLab)}'
    req = s.get(url_lab_instructions, verify=False)
    jsonRes = req.json()
    return jsonRes
    


async def individualLab(q: Q, selectedLab: int):

    global selected_lab_id
    selected_lab_id = selectedLab

    jsonRes = labInstanceMetrics(selectedLab)
    lab_id = jsonRes['labId']

    header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
    body_instructions = f'''{jsonRes['instructions']}'''

    q.page['individualab'] = ui.form_card(
            box='3 1 -1 -1',
            items= [
                ui.text(header_instructions),
                ui.text(body_instructions)
            ]
        )
  

    if not jsonRes['state']:
        q.page['individualab'].items = [
                ui.text(header_instructions),
                ui.text(body_instructions),
                ui.buttons([
                    ui.button(name='startLab', label='Start Lab', disabled=False, primary=True),
                    ui.button(name='endLab', label='End Lab', disabled=True)
                ])
            ]
        await q.page.save()
    else: 
        global exit
        exit = False
        while True:
            print(f'----------------{selectedLab}')
            holder = jsonRes['state']
            print(f'----------------{holder}')
            print(f'-----------{exit}')
            if exit: 
                print('EXIT')
                break;

            if jsonRes['state'] != 'running':
                lab_id = jsonRes['labId']
                header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
                body_instructions = f'''{jsonRes['instructions']}'''
                lab_instance_metrics = f'''Lab instance ID: {jsonRes['liId']} \r\n \r\n\r Lab instance state: {jsonRes['state']} \r\n \r\n\r Lab instance cloudState: {jsonRes['cloudState']} \r\n \r\n\r Time right now: \r\n \r\n\r Time the lab instance was created: {jsonRes['createTime']} \r\n \r\n\r Time the lab instance became usable by the user: {jsonRes['runningStartTime']} \r\n \r\n\r Time remaining for instance use:'''
                urls_markdown = f''''''
                q.page['individualab'].items = [
                    ui.text(header_instructions),
                    ui.text(body_instructions),
                    ui.progress(label='Please wait, starting the lab may take several minutes...', caption=f'Using lab {str(lab_id)}...'),
                    ui.buttons([
                        ui.button(name='startLab', label='Start Lab', disabled=True, primary=False),
                        ui.button(name='endLab', label='End Lab', disabled=False, primary=True),
                    ]),
                    ui.separator(label='Running lab instance information'),
                    ui.text(lab_instance_metrics),
                    ui.text(urls_markdown)
                ]
            else: 
                lab_id = jsonRes['labId']
                header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
                body_instructions = f'''{jsonRes['instructions']}'''
                lab_instance_metrics = f'''Lab instance ID: {jsonRes['liId']} \r\n \r\n\r Lab instance state: {jsonRes['state']} \r\n \r\n\r Lab instance cloudState: {jsonRes['cloudState']} \r\n \r\n\r Time right now: \r\n \r\n\r Time the lab instance was created: {jsonRes['createTime']} \r\n \r\n\r Time the lab instance became usable by the user: {jsonRes['runningStartTime']} \r\n \r\n\r Time remaining for instance use:'''
                urls_markdown = f''''''

                outputs = jsonRes['outputs']
                for urls in range(len(outputs)):
                    urls_markdown = f'''{outputs[urls-1]['description']}: {outputs[urls-1]['value']}\r\n\r\n {urls_markdown}'''


                q.page['individualab'].items = [
                    ui.text(header_instructions),
                    ui.text(body_instructions),
                    ui.message_bar(type='success', text=f'An instance of lab {str(lab_id)} has been created successfully...'),
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
            jsonRes = labInstanceMetrics(selected_lab_id)


def createLabInstanceMethod():

    s = session.getSession()
    create_lab_instance = "https://aquarium.h2o.ai/api/startLab"
    lab_id = f'{str(selected_lab_id)}'
    data = {"labId": lab_id}
    s.post(create_lab_instance, data=data, verify=False)

    return lab_id

def endLabInstanceMethod(labId: int):

    s = session.getSession()
    end_lab_instance = "https://aquarium.h2o.ai/api/endLab"
    lab_id = f'{str(labId)}'
    data = {"labId": lab_id}
    s.post(end_lab_instance, data=data, verify=False)

           
async def endInstance(q: Q):
    
    global exit 
    exit = True 
    endLabInstanceMethod(selected_lab_id)
    jsonRes = labInstanceMetrics(selected_lab_id)

    header_instructions = f'''## {jsonRes['title']} \r\n \r\n\r Lab ID:  {jsonRes['labId']}\r\n\r\n Lab duration:   {jsonRes['durationMinutes']} minutes\r\n\r\n'''
    body_instructions = f'''{jsonRes['instructions']}'''

    q.page['individualab'].items = [
            ui.text(header_instructions),
            ui.text(body_instructions),
            ui.buttons([
                ui.button(name='startLab', label='Start Lab', disabled=False, primary=True),
                ui.button(name='endLab', label='End Lab', disabled=True, primary=False),

            ])
            ]

    await q.page.save()





