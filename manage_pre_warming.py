from h2o_wave import  Q, ui
import session
import pandas as pd 
from tzlocal import get_localzone
import pytz
from datetime import datetime

class Batch:
    def __init__(self, batchId: str, ownerName: str, title: str, createTime: str):
        self.id = f'{batchId}'
        self.batchId = batchId
        self.ownerName = ownerName
        self.title = title
        self.createTime = createTime


def list_of_all_active_pre_warm_batches():
    session_holder = session.get_session()
    url_api_prewarm_batch = "https://aquarium.h2o.ai/api/prewarmbatch"
    req = session_holder.get(url_api_prewarm_batch, verify=False)
    jsonRes = req.json()
    df = pd.DataFrame.from_records(jsonRes)
    return df


async def manage_pre_warming(q: Q):
  
    batch_list = [
        ui.button(name='create_new_pre_warming_batch', label='Create New Pre-Warming Batch', primary=True),
        ui.separator('')
    ]

    q.page['manage_pre_warming']  = ui.form_card(box='3 1 -1 -1', items=batch_list)

    df = list_of_all_active_pre_warm_batches()
    number_of_batches = df.shape[0] 

    if number_of_batches != 0:

        # Create some batches
        batches = [
            Batch(
                batchId=str(df.loc[i].at["batchId"]),
                ownerName=df.loc[i].at["ownerName"],
                title=df.loc[i].at["title"],
                createTime=timestamp_to_human_readable_date(df.loc[i].at["createTime"])) for i in range(number_of_batches)
        ]   
    
        # Create columns for our issue table.
        columns = [
            ui.table_column(name='Pre-Warming Batch #', label='Pre-Warming Batch #', max_width='180'),
            ui.table_column(name='Batch Owner', label='Batch Owner'),
            ui.table_column(name='Lab title', label='Lab title', max_width='400'),
            ui.table_column(name='Time the batch was created', label='Time the batch was created', max_width='300'),
        ]

        batch_list.append(
                ui.table(
                    name='active_batches',
                    columns=columns,
                    rows=[ui.table_row(
                        name=batch.id,
                        cells=[batch.batchId, batch.ownerName, batch.title, batch.createTime]
                    ) for batch in batches],
                    height='800px'
                )
        )

        q.page['manage_pre_warming'].items = batch_list
  
    q.page['manage_pre_warming_settings'] = ui.meta_card(box='')
    await q.page.save()



def list_of_all_labs():
    session_holder = session.get_session()
    url_api_instructor_lab = "https://aquarium.h2o.ai/api/instructorlab"
    req = session_holder.get(url_api_instructor_lab, verify=False)
    jsonRes = req.json()
    df = pd.DataFrame.from_records(jsonRes)
    return df


def start_batch(labId: int, total: int):
    session_holder = session.get_session()
    url_api_create_prewarm_batch = "https://aquarium.h2o.ai/api/createPrewarmBatch"
    data = {
        "labId": f'{labId}',
        "total": f'{total}'
    }
    session_holder.post(url_api_create_prewarm_batch, data=data, verify=False)


async def pop_manage_pre_warming_settings(q: Q):

    enable_labs_list = []

    df = list_of_all_labs()

    for i in range(df.shape[0]):
        enable_labs_list.append(df.loc[i].at["title"])

    q.page['manage_pre_warming_settings'].dialog = ui.dialog(title='', items=[
          ui.dropdown(name='dropdown', label='Choose lab to start', choices=[
            ui.choice(name=f'{df.loc[i].at["labId"]}', label=f'Lab {i+1}: {enable_labs_list[i]}') for i in range(len(enable_labs_list)) 
        ]),
        ui.textbox(name='number_of_instances', label='Specify number of instances to start'),
        ui.buttons([ui.button(name='create_batch',label='Create Batch', primary=True)], justify='center')
    ], closable=True, width='800px')

    await q.page.save()


def batch_details_api_call(id: int):
    session_holder = session.get_session()
    url_api_prewarm_batch = f'https://aquarium.h2o.ai/api/prewarmbatch/{id}'
    req = session_holder.post(url_api_prewarm_batch, verify=False)
    global jsonRes_global
    jsonRes_global = req.json()
    return jsonRes_global

def batch_metrics_header():
    jsonRes = jsonRes_global
    return f'Batch Owner: **{jsonRes["ownerName"]}** \r\n\r\n Batch create time: **{timestamp_to_human_readable_date(jsonRes["createTime"])}** \r\n\r\n Batch active: **{jsonRes["active"]}**'


def batch_metrics_body():
    jsonRes = jsonRes_global
    return f'Total batch size: **{jsonRes["total"]}** \r\n\r\n Total not yet queued: **{jsonRes["totalNotYetQueued"]}** \r\n\r\n Total queued: **{jsonRes["totalQueued"]}** \r\n\r\n Total starting: **{jsonRes["totalStarting"]}** \r\n\r\n Total waiting: **{jsonRes["totalWaiting"]}** \r\n\r\n Total running: **{jsonRes["totalRunning"]}** \r\n\r\n Total endQueued: **{jsonRes["totalEndQueued"]}** \r\n\r\n Total ending: **{jsonRes["totalEnding"]}** \r\n\r\n Total ended: **{jsonRes["totalEnded"]}** \r\n\r\n Total failed: **{jsonRes["totalFailed"]}** \r\n\r\n Total rolled back: **{jsonRes["totalRolledback"]}** \r\n\r\n Total claimed: **{jsonRes["totalClaimed"]}**' 

async def batch_details(q: Q, id: int):

    global current_batch
    current_batch = id

    jsonRes = jsonRes_global

    q.page['batch_details']  = ui.form_card(box='3 1 -1 -1', items=[
        ui.text_xl(content=f'Pre-Warming Batch {id} ({jsonRes["title"]})'),
        ui.button(name='batch_details_refresh_page', label='Refresh page', primary=True),
        ui.text_m(content=batch_metrics_header()),
        ui.inline(items = [
            ui.toggle(name='enable_one', value = None, trigger=True),
            ui.button(name='add_one_instance', label='Add 1 instance', primary = True, disabled=True),
            ui.button(name='add_five_instances', label='Add 5 instances', primary=True, disabled=True),
            ui.button(name='add_twenty_five_instances', label='Add 25 instances', primary=True, disabled=True),
            ui.button(name='add_one_hundred_instances', label='Add 100 instances', primary=True, disabled=True)
        ], inset = True),
        ui.text_m(content=batch_metrics_body()),
        ui.inline(
            items = [
                ui.toggle(name='enable_two', value = None, trigger=True),
                ui.button(name='end_all_unclaimed_instances_in_batch', label='End all unclaimed instances in this batch(in-use instances are not affected)', primary=True, disabled=True)
            ], inset = True
        ),
        ui.inline(
            items = [
                ui.toggle(name='enable_three', value = None, trigger=True),
                ui.button(name='end_all_instances_in_this_batch', label='End all instances in this batch', primary=True, disabled=True)
            ], inset = True
        ),
        ui.inline(
            items = [
                ui.toggle(name='enable_four', value = None,  trigger=True),
                ui.button(name='deactivate_batch', label='Deactivate this batch (this does not end instances)', primary=True, disabled=True)
            ], inset = True
        )
    ])

    await q.page.save()
    #await q.sleep(20)
    #await update_batch_details(q)
    

async def update_batch_details(q: Q):
    
    global Stop
    stop = False

    while True:
        if stop: 
            break;

        batch_details_api_call(current_batch)
        q.page['batch_details'].items[2].text_m.content = batch_metrics_header()
        q.page['batch_details'].items[4].text_m.content = batch_metrics_body()
        await q.page.save()
        await q.sleep(20)
        print('BATCH BEING UPDATED')






def add_instances(number_of_instances: int):
    session_holder = session.get_session()
    url_api_add_to_prewarm_batch = f'https://aquarium.h2o.ai/api/addToPrewarmBatch'
    data = {
        "batchId": f'{current_batch}',
        "numToAdd": f'{number_of_instances}',
    }
    session_holder.post(url_api_add_to_prewarm_batch, data=data, verify=False)



def end_unclaimed_in_pre_warm_batch():
    session_holder = session.get_session()
    url_end_unclaimed_in_pre_warm_batch = f'https://aquarium.h2o.ai/api/endUnclaimedInPrewarmBatch'
    data = {
        "batchId": f'{current_batch}'
    }
    response = session_holder.post(url_end_unclaimed_in_pre_warm_batch, data=data, verify=False)
    print('-----------------------')
    print(response)
    print('-----------------------')
    print(response.status_code)
    print('-----------------------')

def end_all_in_pre_warm_batch():
    session_holder = session.get_session()
    url_end_all_in_pre_warm_batch = f'https://aquarium.h2o.ai/api/endAllInPrewarmBatch'
    data = {
        "batchId": f'{current_batch}'
    }
    response = session_holder.post(url_end_all_in_pre_warm_batch, data=data, verify=False)
    print('-----------------------')
    print(response)
    print('-----------------------')
    print(response.status_code)
    print('-----------------------')


def deactivate_pre_warm_batch():
    session_holder = session.get_session()
    url_deactivate_pre_warm_batch = f'https://aquarium.h2o.ai/api/deactivatePrewarmBatch'
    data = {
        "batchId": f'{current_batch}'
    }
    response = session_holder.post(url_deactivate_pre_warm_batch, data=data, verify=False)
    print('-----------------------')
    print(response)
    print('-----------------------')
    print(response.status_code)
    print('-----------------------')

def timestamp_to_human_readable_date(timestamp: int):
    zone = str(get_localzone())
    timestamp = datetime.fromtimestamp(timestamp/1000, pytz.timezone(zone))
    human_readable_date =  timestamp.strftime("%a, %d %b %Y %I:%M:%S %p %Z")
    return human_readable_date




 


 

 

 
 
 
