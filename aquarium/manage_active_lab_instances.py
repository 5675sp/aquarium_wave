from h2o_wave import main, app, Q, ui
import session
import pandas as pd  





async def manage_active_lab_instances(q: Q):

    _number_of_active_lab_instances = len(df)

    q.page['manage_active_lab_instances'] = ui.form_card(box='3 1 7 3', items=[
        ui.text(f'There are {_number_of_active_lab_instances} active lab instances.'),
        ui.button(name='refresh_page', label='Refresh Page'),
        ui.separator('') ,
        ui.buttons([
            ui.button(name='enable_extend_all_waiting', label='Enable extend all waiting'),
            ui.button(name='extend_all_waiting_labs_by_30_minutes', label='Extend all waiting labs by 30 minutes', disabled=True)
        ]),
        ui.buttons([
            ui.button(name='enable_extend_all_running', label='Enable extend all running'),
            ui.button(name='extend_all_running_labs_by_30_minutes', label='Extend all running labs by 30 minutes', disabled=True)
        ]),
        ui.buttons([
            ui.button(name='enable_end_button', label='Enable end button'),
            ui.button(name='end_all_labs_immediately', label='End all labs immediately (USE WITH CAUTION!)', disabled=True)
        ])
    ])

    await q.page.save()



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
        

individualLabMetrics = None


# Create columns for our lab table.
columns = [
    ui.table_column(name='id', label='ID', max_width = '100px'),
    ui.table_column(name='title', label='Title', max_width = '400px'),
    ui.table_column(name='instance type name email', label='Instance Type', max_width = '100px'),
    ui.table_column(name='name', label='Name', max_width = '190px'),
    ui.table_column(name='email', label='Email', max_width = '190px'),
    ui.table_column(name='state', label='State', max_width = '100px'),
    ui.table_column(name='cloud state', label='Cloud State', max_width = '300px'),
    ui.table_column(name='cloud resources id', label='Cloud resources ID', max_width = '400px'),
    ui.table_column(name='minutes remaining', label='Minutes remaining', max_width = '150px'),
]


buttons = None
df = None
labs = None

def activeLabsMethod():

    s = session.getSession()
    url_active = "https://aquarium.h2o.ai/api/active"
    req2 = s.get(url_active, verify=False)
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
            identification=str(df.loc[i].at["liId"]),
            title=df.loc[i].at["title"],
            name=df.loc[i].at["instanceType"],
            email=df.loc[i].at["userName"],
            type=df.loc[i].at["userEmail"],
            state=df.loc[i].at["state"],
            _cloud_state=df.loc[i].at["cloudState"],
            _cloud_resource_id=str(df.loc[i].at["cloudResourceId"]),
            _minutes_remaining=str(df.loc[i].at["runningDurationMinutes"])) for i in range(rowCount)
    ]
    

  

    global individualLabMetrics 
    individualLabMetrics = [
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

async def activeLabsTable(q: Q):


    q.page['activelabs'] = ui.form_card(box='3 4 7 -1', items=[
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

    await q.page.save()



async def activeLabMetrics(q: Q, row: int):

    global individualLabMetrics 


    if row == 0: 
        q.page['activeLabButtons'] = ui.form_card(box='10 1 -1 -1', items=individualLabMetrics)
    else: 
        individualLabMetrics = [
            ui.separator(label='Lab Metrics/Settings'),
            ui.textbox(name='liId', label='ID', value=str(df.loc[row-1].at["liId"]), disabled=True),
            ui.textbox(name='title', label='Title', value=df.loc[row-1].at["title"], disabled=True),
            ui.textbox(name='instanceType', label='Instance Type', value=df.loc[row-1].at["instanceType"], disabled=True),
            ui.textbox(name='userName', label='Name', value=df.loc[row-1].at["userName"], disabled=True),
            ui.textbox(name='userEmail', label='Email', value=df.loc[row-1].at["userEmail"], disabled=True),
            ui.textbox(name='state', label='State', value=df.loc[row-1].at["state"], disabled=True),
            ui.textbox(name='cloudState', label='Cloud state', value=df.loc[row-1].at["cloudState"], disabled=True),
            ui.textbox(name='cloudResourceId', label='Cloud resources ID', value=str(df.loc[row-1].at["cloudResourceId"]), disabled=True),
            ui.textbox(name='runningDurationMinutes', label='Minutes remaining', value=str(df.loc[row-1].at["runningDurationMinutes"]), disabled=True),
            ui.buttons([ui.button(name='extend',label='Extend', primary=True)], justify='center'),
            ui.buttons([ui.button(name='end',label='End', primary=True, disabled=True)], justify='center')
        ]
        
        q.page['activeLabButtons'] = ui.form_card(box='10 1 -1 -1', items=individualLabMetrics)

    await q.page.save()





