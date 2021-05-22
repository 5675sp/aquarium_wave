from h2o_wave import Q, ui
import session
import pandas as pd  


def dashboardmethod():

    s = session.getSession()
    url_browse_labs = "https://aquarium.h2o.ai/api/dashboard"
    req2 = s.get(url_browse_labs, verify=False)
    global jsonRes
    jsonRes = req2.json()
   

    size = len(jsonRes['activeLabs'])
   
    
    if size == 0:
        global myLabs
        #myLabs = f'''You have no active labs ([Browse Labs]() to start one).'''
        myLabs = [ui.button(name='message', label='You have no active labs (Browse Labs to start one)', primary=False, disabled=False)]
    else:

  
        myLabs = []
        alert = f'''Your currently active labs:''' 
        myLabs.append(ui.text(alert))
        
        for i in range(size):
            
            holder = jsonRes['activeLabs'][i]['title']
            myLabs.append(ui.button(name=f'lab{i}', label=f'{holder}', primary=False, disabled=False))

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

reCaptcha status: **{jsonRes['skipReCaptchaUntilTimestamp']}**

'''

    global admin
    admin = f'''

syncGeneration:	**{jsonRes['syncGeneration']}**

syncInProgress:	**{jsonRes['syncInProgress']}**

syncWaitTimestamp: **{jsonRes['syncWaitTimestamp']}**

syncWakeupTimestamp: **{jsonRes['syncWakeupTimestamp']}**

Total not yet reported to Salesforce: **{jsonRes['totalEndedNotReportedToSalesforce']}**

'''
    global listOfItems
    listOfItems =[
            ui.separator(label='Instructor'),
            ui.button(name='refresh', label='Refresh page'),
            ui.text(sample_markdown),
            ui.buttons([
                ui.button(name='disableRecaptcha', label='Disable reCaptcha (temporary)'),
                ui.button(name='enableRecaptcha', label='Enable reCaptcha immediately')
            ]),
            ui.separator(label='Admin'),
            ui.text(admin),
            ui.button(name='syncNow', label='Sync now'),
        ]

    for n in range(len(myLabs)):
        listOfItems.insert(n, myLabs[n])





async def dashboard(q: Q):

    q.page['metricsDashboard'] = ui.form_card(
        box='3 1 -1 -1',
        items=listOfItems
    )

    await q.page.save()
    


   

    










 
