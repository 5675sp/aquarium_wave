from os import sep
from h2o_wave import main, app, Q, ui
import session 
import csv
import pandas as pd

class Row:
    def __init__(
     self,
     liId: str, 
     batchId: str, 
     userId: str,
     firstName: float, 
     lastName: str, 
     email: str, 
     title: str, 
     instanceType: str, 
     createReason: str, 
     endReason: str, 
     state: str, 
     cloudState: str, 
     cloud: str, 
     cloudRegion: str, 
     createTime: str, 
     submitted: str, 
     startingStartTime: str, 
     waitingStartTime: str,
     runningStartTime: str,
     endTime: str,
     date: str,
     labSeconds: str,
     cloudHours: str,
     cloudCostPerHour: str,
     cloudCost: str
     ):
       
        self.id = liId
        self.liId = liId
        self.batchId = batchId
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.title = title
        self.instanceType = instanceType
        self.createReason = createReason
        self.endReason = endReason
        self.state = state
        self.cloudState = cloudState
        self.cloud = cloud
        self.cloudRegion = cloudRegion
        self.createTime = createTime
        self.submitted = submitted
        self.startingStartTime = startingStartTime 
        self.waitingStartTime = waitingStartTime
        self.runningStartTime = runningStartTime
        self.endTime = endTime
        self.date = date
        self.labSeconds = labSeconds
        self.cloudHours = cloudHours
        self.cloudCostPerHour = cloudCostPerHour
        self.cloudCost = cloudCost



async def csv_table(q: Q):


    q.page['csv'] = ui.form_card(box='3 1 -1 -1', items=[
       ui.progress(label='Loading most recent instances (100)')
    ])

    await q.page.save()

    session_holder = session.get_session()
    url_api_downloadInstancesCsv = "https://aquarium.h2o.ai/api/downloadInstancesCsv"
    req = session_holder.get(url_api_downloadInstancesCsv, verify=False)
    resPonse = req.text 

    f = open('csv_file.txt', 'w')  
    f.write(resPonse)  
    f.close()

    df = pd.read_csv('csv_file.txt') 

    columns = [
        ui.table_column(name='liId', label='liId', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='batchId', label='batchId', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='userId', label='userId', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='firstName', label='firstName', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='lastName', label='lastName', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='email', label='email', sortable=True, searchable=True, filterable=True, max_width = '350px'),
        ui.table_column(name='title', label='title', sortable=True, searchable=True, filterable=True, max_width = '350px'),
        ui.table_column(name='instanceType', label='instanceType', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='createReason', label='createReason', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='endReason', label='endReason', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='state', label='state', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='cloudState', label='cloudState', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='cloud', label='cloud', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='cloudRegion', label='cloudRegion', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='createTime', label='createTime', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='submitted', label='submitted', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='startingStartTime', label='startingStartTime', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='waitingStartTime', label='waitingStartTime', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='runningStartTime', label='runningStartTime', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='endTime', label='endTime', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='date', label='date', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='labSeconds', label='labSeconds', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='cloudHours', label='cloudHours', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='cloudCostPerHour', label='cloudCostPerHour', sortable=True, searchable=True, filterable=True),
        ui.table_column(name='cloudCost', label='cloudCost', sortable=True, searchable=True, filterable=True),
    ]


    rowCount = df.shape[0] 
    
    rowsInfo = [
        Row(
            liId = str(df.loc[i].at["liId"]), 
            batchId = str(df.loc[i].at["batchId"]), 
            userId = str(df.loc[i].at["userId"]),
            firstName = str(df.loc[i].at["firstName"]), 
            lastName = str(df.loc[i].at["lastName"]), 
            email = str(df.loc[i].at["email"]), 
            title = str(df.loc[i].at["title"]), 
            instanceType = str(df.loc[i].at["instanceType"]), 
            createReason = str(df.loc[i].at["createReason"]), 
            endReason = str(df.loc[i].at["endReason"]), 
            state = str(df.loc[i].at["state"]), 
            cloudState = str(df.loc[i].at["cloudState"]), 
            cloud = str(df.loc[i].at["cloud"]), 
            cloudRegion = str(df.loc[i].at["cloudRegion"]), 
            createTime = str(df.loc[i].at["createTime"]), 
            submitted = str(df.loc[i].at["submitted"]), 
            startingStartTime = str(df.loc[i].at["startingStartTime"]), 
            waitingStartTime = str(df.loc[i].at["waitingStartTime"]),
            runningStartTime = str(df.loc[i].at["runningStartTime"]),
            endTime = str(df.loc[i].at["endTime"]),
            date = str(df.loc[i].at["date"]),
            labSeconds = str(df.loc[i].at["labSeconds"]),
            cloudHours = str(df.loc[i].at["cloudHours"]),
            cloudCostPerHour = str(df.loc[i].at["cloudCostPerHour"]),
            cloudCost = str(df.loc[i].at["cloudCost"])) for i in range(rowCount-100, rowCount)
    ]


    
    q.page['csv'].items = [
        ui.table(
            name='instances',
            columns=columns,
            rows=[ui.table_row(
                name=rowInfo.id,
                cells=[rowInfo.liId, rowInfo.batchId, rowInfo.userId ,rowInfo.firstName, rowInfo.lastName,
                       rowInfo.email, rowInfo.title, rowInfo.instanceType, rowInfo.createReason,rowInfo.endReason, 
                       rowInfo.state, rowInfo.cloudState, rowInfo.cloud, rowInfo.cloudRegion, rowInfo.createTime, rowInfo.submitted , 
                       rowInfo.startingStartTime, rowInfo.waitingStartTime, rowInfo.runningStartTime, rowInfo.endTime, rowInfo.date, rowInfo.labSeconds,
                       rowInfo.cloudHours, rowInfo.cloudCostPerHour, rowInfo.cloudCost ]
            ) for rowInfo in rowsInfo],
            groupable=True,
            downloadable=True,
            resettable=True,
            height='1040px'
        )
    ]

    
    await q.page.save()









    


