from h2o_wave import main, app, Q, ui

import time 
import random 
import concurrent.futures

import json
import requests
import logging
from http.client import HTTPConnection


@app('/lab')
async def serve(q: Q):
    

        q.page['instance'] = ui.form_card(box='1 1 5 4', items=[
            ui.buttons([
                ui.button(name='start', label='Start Lab', primary=True),
                ui.button(name='end', label='End Lab', disabled=True),
            ]),
        ])

        if q.args.start:

            log = logging.getLogger('urllib3')
            log.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            log.addHandler(ch)
            HTTPConnection.debuglevel = 1
            s = requests.session()
            url_login = "https://aquarium.h2o.ai/api/login"

            data1 = {
                "reCaptchaSolution": "",
                "email": "sergio.perez@h2o.ai",
                "password": "FuE9zhYa20!"
            }

            

            req1 = s.post(url_login, data=data1, verify=False)
        
            #print(req1.status_code)
            print(req1.json())
            #print(req1.cookies.get_dict())

            test = s.get("https://aquarium.h2o.ai/api/downloadInstancesCsv", verify=False)
            print('*****************CSV********************')
            print('*******************CSV******************')
            print(test.text)
            print('*****************CSV********************')
            print('*******************CSV******************')

            url_start_lab = "https://aquarium.h2o.ai/api/startLab"

            headers = {
                "Content-type": "application/x-www-form-urlencoded"
            }

            lab_id = "24"

            data2 = {
                "labId": lab_id
            }

            req2 = s.post(url_start_lab, data=data2, headers=headers, verify=False)
            print('*************************************')
            print('*************************************')
            print(req2.status_code)
            print('*************************************')
            print('*************************************')
            print(req2.json())
            print('*************************************')
            print('*************************************')

            url_lab = "https://aquarium.h2o.ai/api/lab/" + lab_id
            req3 = s.get(url_lab, verify=False)

        
            q.page['instance'] = ui.form_card(box='1 1 5 4', items=[ui.progress(label='Please wait, starting the lab may take several minutes...', caption=f'Using lab {lab_id}...'),
                ui.buttons([
                    ui.button(name='start', label='Start Lab', disabled=True),
                    ui.button(name='end', label='End Lab', primary=True),
                ])
            ])
            
          
            await q.page.save()

            jsonRes = req3.json()
            outputs = jsonRes['outputs']

            print('CHECK FOR NEW CONTENT')
            while len(outputs) == 0:
                req3 = s.get(url_lab, verify=False)
                jsonRes = req3.json()
                outputs = jsonRes['outputs']
                time.sleep(20)
                print(jsonRes)
                print('|--------------------------|')
        
        
            lab_instance_id = jsonRes['liId']
            lab_instance_state = jsonRes['state']
            driverless_ai_url = jsonRes['outputs']


            url = driverless_ai_url[0]['value']
            sample_markdown = f'''&nbsp; &nbsp;Driverless AI URL: &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; [{url}]({url})'''

            q.page['instance'] = ui.form_card(box='1 1 5 4', items=[ui.message_bar(type='success', text=f'An instance of lab {lab_id} has been created successfully...'),
                ui.separator(label='Running lab instance information'),
                ui.table(name='table', columns=[
                    ui.table_column(name='col1', label='Name'),
                    ui.table_column(name='col2', label='Description'),
                ], rows=[
                    ui.table_row(name='row1', cells=['Lab instance ID:', str(lab_instance_id)]),
                    ui.table_row(name='row2', cells=['Lab instance state:', lab_instance_state]),
                ]), 
                    ui.text(sample_markdown),
                    ui.buttons([
                        ui.button(name='start', label='Start Lab', disabled=True),
                        ui.button(name='end', label='End Lab', primary=True),
                    ]), 
            ])


            await q.page.save()

        await q.page.save()
        

  
    
    


