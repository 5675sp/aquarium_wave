from h2o_wave import Q, ui
import session

from tzlocal import get_localzone
import pytz
from datetime import timedelta
from datetime import datetime
from dateutil import relativedelta



def start_sync():
    session_holder = session.get_session()
    url_api_start_sync= "https://aquarium.h2o.ai/api/startSync"
    response = session_holder.post(url_api_start_sync, verify=False)
    print(response.status_code)


def dashboard_metrics():

    session_holder = session.get_session()
    url_api_dashboard = "https://aquarium.h2o.ai/api/dashboard"
    req = session_holder.get(url_api_dashboard, verify=False)
    global jsonRes
    jsonRes = req.json()
   

    size = len(jsonRes['activeLabs'])
   
    
    if size == 0:
        global myLabs
        #myLabs = f'''You have no active labs ([Browse Labs]() to start one).'''
        myLabs = [ui.button(name='dashboard_message', label='You have no active labs (Browse Labs to start one)', primary=True, disabled=False)]
    else:

        myLabs = []

        row_titles = []
        
        for i in range(size):
            title = jsonRes['activeLabs'][i]['title']
            lab_id = jsonRes['activeLabs'][i]['labId']

            row_titles.append(ui.table_row(name=f'{lab_id}', cells=[f'{title}']))
            

        myLabs.append(
            ui.table(name='user_active_lab_instances', columns=[
                ui.table_column(name='col1_title', label='Your currently active labs:', max_width = '400px'),
            ], rows=row_titles)
        )

            #holder = jsonRes['activeLabs'][i]['title']
            #labs = f'{labs}**{holder}**</br></br>'

        
        #myLabs = f'''Your currently active labs:</br></br> {labs}''' 

    global sample_markdown
    sample_markdown = f'''
</br>

Aquarium version: **{jsonRes['aquariumVersion']}**
</br>
</br>

Total active pre-warm batches: **{jsonRes['totalActivePrewarmBatches']}**

Total not-yet-queued lab instances: **{jsonRes['totalNotYetQueued']}**

Total queued lab instances: **{jsonRes['totalQueued']}**

Total starting lab instances: **{jsonRes['totalStarting']}**

Total waiting lab instances: **{jsonRes['totalWaiting']}**

Total running lab instances: **{jsonRes['totalRunning']}**

Total endqueued lab instances: **{jsonRes['totalEndQueued']}**

Total ending lab instances: **{jsonRes['totalEnding']}**

Total ended lab instances: **{jsonRes['totalEnded']}**

</br>

reCaptcha status: **{reCaptcha_format(jsonRes['skipReCaptchaUntilTimestamp'])}**

'''


    global admin
    admin = f'''

syncGeneration:	**{jsonRes['syncGeneration']}**

syncInProgress:	**{jsonRes['syncInProgress']}**

syncWaitTimestamp: **{timestamp_to_human_readable_date(jsonRes['syncWaitTimestamp'])}**

syncWakeupTimestamp: **{timestamp_to_human_readable_date(jsonRes['syncWakeupTimestamp'])}**

Total not yet reported to Salesforce: **{jsonRes['totalEndedNotReportedToSalesforce']}**

'''
    global list_of_items
    list_of_items =[
        
            ui.separator(label='Instructor'),
            ui.button(name='refresh_dashboard', label='Refresh page', primary=True),
            ui.text(sample_markdown),
            ui.buttons([
                ui.button(name='disableRecaptcha', label='Disable reCaptcha (temporary)', primary=True),
                ui.button(name='enableRecaptcha', label='Enable reCaptcha immediately', primary=True)
            ]),
            ui.separator(label='Admin'),
            ui.text(admin),
            ui.button(name='syncNow', label='Sync now', primary=True),
        ]

    for n in range(len(myLabs)):
        list_of_items.insert(n, myLabs[n])



async def dashboard(q: Q):

    q.page['metricsDashboard'] = ui.form_card(
        box='3 1 -1 -1',
        items=list_of_items
    )

    await q.page.save()
    
   
def timestamp_to_human_readable_date(timestamp: int):
    zone = str(get_localzone())
    timestamp = datetime.fromtimestamp(timestamp/1000, pytz.timezone(zone))
    human_readable_date =  timestamp.strftime("%a, %d %b %Y %I:%M:%S %p %Z")
    return human_readable_date
   

def reCaptcha_format(timestamp: int):

    zone = str(get_localzone())

    x= datetime.fromtimestamp(timestamp/1000, pytz.timezone(zone))

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

    pst = pytz.timezone(zone)
    x = datetime.now(pst)

    year = int(x.strftime("%Y"))
    month = int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    hour = int(x.strftime("%H"))
    minute = int(x.strftime("%M"))
    second = int(x.strftime("%S"))

    date_2 = datetime(year,month,day,hour,minute,second)

    #This will find the difference between the two dates
    difference = relativedelta.relativedelta(date_1, date_2)

  
    hours = difference.hours
    minutes = difference.minutes
    
    return f'Skipping reCaptcha for {hours} hours, {minutes} minutes'




   






 
