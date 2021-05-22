from h2o_wave import main, app, Q, ui
import session
import pandas as pd  




class Lab:
    def __init__(self, labId: str, name: str, ownerName: str, title: str, cloudEnv: str, imageId: str, instanceType: str, duration: str, enabled: str):
        global _id
        _id += 1
        self.id = f'{_id}'
        self.labId = labId
        self.name = name
        self.ownerName = ownerName
        self.title = title
        self.cloudEnv = cloudEnv
        self.imageId = imageId
        self.instanceType = instanceType
        self.duration = duration
        self.enabled = enabled

        
# Create some labs
individualLabMetrics = None


# Create columns for our lab table.
columns = [
    ui.table_column(name='lab id', label='ID', max_width = '20px'),
    ui.table_column(name='name', label='Name', max_width = '250px'),
    ui.table_column(name='owner name', label='Owner Name', max_width = '100px'),
    ui.table_column(name='title', label='Title', max_width = '300px'),
    ui.table_column(name='cloud env', label='Cloud Env', max_width = '130px'),
    ui.table_column(name='image id', label='Image ID', max_width = '230px'),
    ui.table_column(name='instance type', label='Instance Type', max_width = '100px'),
    ui.table_column(name='duration', label='Duration', max_width = '80px'),
    ui.table_column(name='enabled', label='Enabled', max_width = '80px'),
]


buttons = None
df = None
labs = None

def managelabsmethod():

    s = session.getSession()
    url_browse_labs = "https://aquarium.h2o.ai/api/instructorlab"
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
            labId=str(df.loc[i].at["labId"]),
            name=df.loc[i].at["name"],
            ownerName=df.loc[i].at["ownerName"],
            title=df.loc[i].at["title"],
            cloudEnv=df.loc[i].at["cloudEnvName"],
            imageId=df.loc[i].at["imageId"],
            instanceType=df.loc[i].at["instanceType"],
            duration=str(df.loc[i].at["durationMinutes"]),
            enabled=str(df.loc[i].at["enabled"])) for i in range(rowCount)
    ]

    

    global individualLabMetrics 

    individualLabMetrics = [
         ui.separator(label='Lab Metrics/Settings'),
         ui.textbox(name='_labId', label='ID', value='', disabled=True),
         ui.textbox(name='_name', label='Name', value='', disabled=True),
         ui.textbox(name='_ownerName', label='Owner Name', value='', disabled=True),
         ui.textbox(name='_title', label='Title', value='', disabled=True),
         ui.textbox(name='_cloudEnvName', label='Cloud Env', value='', disabled=True),
         ui.textbox(name='_imageId', label='Image ID', value='', disabled=True),
         ui.textbox(name='_instanceType', label='Instance Type', value='', disabled=True),
         ui.textbox(name='_durationMinutes', label='Duration', value='', disabled=True),
         ui.textbox(name='_enabled', label='Enabled', value='', disabled=True),
         ui.buttons([
            ui.button(name='enabledLab', label='Enabled Quick Base Settings', disabled=True),
            ui.button(name='saveBaseSettings', label='Save Base Settings', disabled=True),
            ui.button(name='cancelBaseSettings', label='Cancel', disabled=True)
        ]),
        ui.separator(label=''),
         ui.buttons([
            ui.button(name='enabledLab', label='Enabled', disabled=True),
            ui.button(name='disabledLab', label='Disabled', disabled=True)
        ]),
        ui.buttons([
            ui.button(name='visibleLab', label='Visible', disabled=True),
            ui.button(name='invisibleLab', label='Invisible', disabled=True)

        ]),
        ui.button(name='editLab', label='Edit', disabled=True),
        

    ]

async def manageLabsSettings(q: Q):


    q.page['metrics'] = ui.form_card(box='3 1 7 -1', items=[
        ui.table(
            name='tableoflabs',
            columns=columns,
            rows=[ui.table_row(
                name=lab.id, cells=[lab.labId, lab.name, lab.ownerName, lab.title, lab.cloudEnv ,lab.imageId,
                                      lab.instanceType,lab.duration, lab.enabled]) for lab in labs],
            downloadable=False,
            height='1000px'
           
        ),
    ])

    await q.page.save()


async def labMetrics(q: Q, row: int):

    global individualLabMetrics 

    

    if row == 0: 
        q.page['editButtons'] = ui.form_card(box='10 1 -1 -1', items=individualLabMetrics)
    else: 
        individualLabMetrics = [
            ui.separator(label='Lab Metrics/Settings'),
            ui.textbox(name='_labId', label='ID', value=str(df.loc[row-1].at["labId"]), disabled=True),
            ui.textbox(name='_name', label='Name', value=df.loc[row-1].at["name"], disabled=True),
            ui.textbox(name='_ownerName', label='Owner Name', value=df.loc[row-1].at["ownerName"], disabled=True),
            ui.textbox(name='_title', label='Title', value=df.loc[row-1].at["title"], disabled=True),
            ui.textbox(name='_cloudEnvName', label='Cloud Env', value=df.loc[row-1].at["cloudEnvName"], disabled=True),
            ui.textbox(name='_imageId', label='Image ID', value=df.loc[row-1].at["imageId"], disabled=True),
            ui.textbox(name='_instanceType', label='Instance Type', value=df.loc[row-1].at["instanceType"], disabled=True),
            ui.textbox(name='_durationMinutes', label='Duration', value=str(df.loc[row-1].at["durationMinutes"]), disabled=True),
            ui.textbox(name='_enabled', label='Enabled', value=str(df.loc[row-1].at["enabled"]), disabled=True),
            ui.buttons([
                ui.button(name='enabledLab', label='Enabled Quick Base Settings', disabled=False, primary=True),
                ui.button(name='saveBaseSettings', label='Save Base Settings', disabled=True),
                ui.button(name='cancelBaseSettings', label='Cancel', disabled=True)
            ]),
            ui.separator(label=''),
            ui.buttons([
            ui.button(name='enabledLab', label='Enabled'),
            ui.button(name='disabledLab', label='Disabled')
            ]),
            ui.buttons([
            ui.button(name='visibleLab', label='Visible'),
            ui.button(name='invisibleLab', label='Invisible')

            ]),
            ui.button(name='editLab', label='Edit', primary=True),
        ]
        
        q.page['editButtons'] = ui.form_card(box='10 1 -1 -1', items=individualLabMetrics)

        q.page['moreSettings'] = ui.meta_card(box='')

    await q.page.save()

async def popSettings(q: Q):
    q.page['moreSettings'].dialog = ui.dialog(title='', items=[
        ui.separator(label='Base Settings'),
        ui.textbox(name='popName', label='Name', value=''),
        ui.textbox(name='popTitle', label='Title', value=''),
        ui.textbox(name='popCloudEnvName', label='Cloud Environment Name', value=''),
        ui.textbox(name='popCloudImageId', label='Cloud Image ID', value=''),
        ui.textbox(name='popCloudInstanceType', label='Cloud Instance Type', value=''),
        ui.textbox(name='popDurationInMinutes', label='Duration in Minutes', value=''),
        ui.separator(label='Student Instructions'),
        ui.textbox(name='popStudentInstructions', label='', multiline=True, height = '300px'),
        ui.separator(label='Cloud Template'),
        ui.textbox(name='popCloudTemplate', label='', multiline=True, height = '300px'),
        ui.buttons([ui.button(name='save',label='Save', primary=True)], justify='center'),
    ], closable=True, width='800px')

    await q.page.save()



