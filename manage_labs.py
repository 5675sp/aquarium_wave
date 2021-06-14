from h2o_wave import Q, ui
import session
import pandas as pd 
import operator 

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
individual_lab_metrics = None


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

def manage_labs():

    session_holder = session.get_session()
    url_api_instructor_lab = "https://aquarium.h2o.ai/api/instructorlab"
    req = session_holder.get(url_api_instructor_lab, verify=False)
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


    global individual_lab_metrics 

    individual_lab_metrics = [
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
            ui.button(name='enabledLabQuickSettings', label='Enabled Quick Base Settings', disabled=True),
            ui.button(name='saveBaseSettings', label='Save Base Settings', disabled=True),
            ui.button(name='cancelBaseSettings', label='Cancel', disabled=True)
        ]),
        ui.separator(label=''),
         ui.buttons([
            ui.button(name='enabledLab', label='Enabled', disabled=True, primary=True),
            ui.button(name='disabledLab', label='Disabled', disabled=True, primary=True)
        ]),
        #ui.buttons([
        #    ui.button(name='visibleLab', label='Visible', disabled=True),
        #    ui.button(name='invisibleLab', label='Invisible', disabled=True)
        #]),
        ui.button(name='editLab', label='Edit', disabled=True),
    ]

async def manage_lab_settings(q: Q):

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


async def lab_metrics(q: Q, row: int, enable_lab_quick_settings: bool): 

    global individual_lab_metrics 

    global current_selected_lab
    current_selected_lab = row

    


    if row == 0: 
        q.page['editButtons'] = ui.form_card(box='10 1 -1 -1', items=individual_lab_metrics)
    else: 

        enabled_or_disabled =  bool(df.loc[row-1].at["enabled"])

        _enabled = None
        _disabled = None


        if enabled_or_disabled:
            _enabled = False
            _disabled = True
        else:
            _enabled = True
            _disabled = False

        global current_selected_lab_Id
        current_selected_lab_Id = str(df.loc[row-1].at["labId"])

        quick_setting_disable = None

        if enable_lab_quick_settings:
            quick_setting_disable = False
        else:
            quick_setting_disable = True

    
       
            
        individual_lab_metrics = [
            ui.separator(label='Lab Metrics/Settings'),
            ui.textbox(name='_labId', label='ID', value=str(df.loc[row-1].at["labId"]), disabled=enable_lab_quick_settings),
            ui.textbox(name='_name', label='Name', value=df.loc[row-1].at["name"], disabled=enable_lab_quick_settings),
            ui.textbox(name='_ownerName', label='Owner Name', value=df.loc[row-1].at["ownerName"], disabled=enable_lab_quick_settings),
            ui.textbox(name='_title', label='Title', value=df.loc[row-1].at["title"], disabled=enable_lab_quick_settings),
            ui.textbox(name='_cloudEnvName', label='Cloud Env', value=df.loc[row-1].at["cloudEnvName"], disabled=enable_lab_quick_settings),
            ui.textbox(name='_imageId', label='Image ID', value=df.loc[row-1].at["imageId"], disabled=enable_lab_quick_settings),
            ui.textbox(name='_instanceType', label='Instance Type', value=df.loc[row-1].at["instanceType"], disabled=enable_lab_quick_settings),
            ui.textbox(name='_durationMinutes', label='Duration', value=str(df.loc[row-1].at["durationMinutes"]), disabled=enable_lab_quick_settings),
            ui.textbox(name='_enabled', label='Enabled', value=str(df.loc[row-1].at["enabled"]), disabled=True),
            ui.buttons([
                ui.button(name='enabledLabQuickSettings', label='Enabled Quick Base Settings', disabled=quick_setting_disable, primary=True),
                ui.button(name='saveBaseSettings', label='Save Base Settings', disabled=operator.not_(quick_setting_disable), primary = True),
                ui.button(name='cancelBaseSettings', label='Cancel', disabled=operator.not_(quick_setting_disable), primary = True)
            ]),
            ui.separator(label=''),
            ui.buttons([
            ui.button(name='enabledLab', label='Enabled', disabled=_disabled, primary=True),
            ui.button(name='disabledLab', label='Disabled', disabled=_enabled, primary=True)
            ]),
            #ui.buttons([
            #   ui.button(name='visibleLab', label='Visible'),
            #   ui.button(name='invisibleLab', label='Invisible')
            #]),
            ui.button(name='editLab', label='Edit', primary=True),
        ]
        
        q.page['editButtons'] = ui.form_card(box='10 1 -1 -1', items=individual_lab_metrics)

        q.page['moreSettings'] = ui.meta_card(box='')
        print('moreSettings')        

    await q.page.save()



async def pop_settings(q: Q):

    print('POP SETTINGS')

    name = f'''{df.loc[current_selected_lab-1].at["name"]}'''
    title = f'''{df.loc[current_selected_lab-1].at["title"]}'''
    cloud_environment_name = f'''{df.loc[current_selected_lab-1].at["cloudEnvName"]}'''
    cloud_image_id = f'''{df.loc[current_selected_lab-1].at["imageId"]}'''
    cloud_instance_type = f'''{df.loc[current_selected_lab-1].at["instanceType"]}'''
    duration_in_minutes = f'''{df.loc[current_selected_lab-1].at["durationMinutes"]}'''

    cloud_template = f'''{df.loc[current_selected_lab-1].at["cloudTemplate"]}'''
    pop_student_instructions = f'''{df.loc[current_selected_lab-1].at["instructions"]}'''

    q.page['moreSettings'].dialog = ui.dialog(title='', items=[
        ui.separator(label='Base Settings'),
        ui.textbox(name='popName', label='Name', value=name),
        ui.textbox(name='popTitle', label='Title', value=title),
        ui.textbox(name='popCloudEnvName', label='Cloud Environment Name', value=cloud_environment_name),
        ui.textbox(name='popCloudImageId', label='Cloud Image ID', value=cloud_image_id),
        ui.textbox(name='popCloudInstanceType', label='Cloud Instance Type', value=cloud_instance_type),
        ui.textbox(name='popDurationInMinutes', label='Duration in Minutes', value=duration_in_minutes),
        ui.separator(label='studentInstructions'),
        ui.textbox(name='popStudentInstructions', label='', value=pop_student_instructions, multiline=True, height = '500px'),
        ui.separator(label='Cloud Template'),
        ui.textbox(name='popCloudTemplate', label='',value=cloud_template, multiline=True, height = '500px'),
        ui.separator(label=''),
        ui.buttons([
            ui.button(name='save', label='Save', disabled=False, primary=True),
            ui.button(name='cancel', label='Cancel', disabled=False, primary=True)
        ], justify='center'),
    ], closable=False, width='800px')

    await q.page.save()



   

async def enabled_lab(q: Q, enabled:str):

    session_holder = session.get_session()
    url_api_set_lab_enabled = "https://aquarium.h2o.ai/api/setLabEnabled"
    data = {
        "labId": f'{q.args._labId}',
        "enabled": f'{enabled}'
    }
    session_holder.post(url_api_set_lab_enabled, data=data, verify=False)
    manage_labs()
    await manage_lab_settings(q)
    await lab_metrics(q, current_selected_lab, True)

   

def save_lab_metrics(q: Q):
    session_holder = session.get_session()
    url_api_instructor_lab_number = f'https://aquarium.h2o.ai/api/instructorlab/{current_selected_lab_Id}'
    data = {
        "name": f'{q.args.popName}',
        "cloudEnvName": f'{q.args.popCloudEnvName}',
        "title": f'{q.args.popTitle}',
        "imageId": f'{q.args.popCloudImageId}',
        "instanceType": f'{q.args.popCloudInstanceType}',
        "durationMinutes": f'{q.args.popDurationInMinutes}',
        "instructions": f'{q.args.popStudentInstructions}',
        "cloudTemplate": f'{q.args.popCloudTemplate}',
    }
    response = session_holder.post(url_api_instructor_lab_number, data=data, verify=False)
    print(response.status_code)


def save_quick_base_settings(q: Q):
    session_holder = session.get_session()
    url_api_instructor_lab_number = f'https://aquarium.h2o.ai/api/instructorlab/{q.args._labId}'
    data = {
        "name": f'{q.args._name}',
        "cloudEnvName": f'{q.args._cloudEnvName}',
        "title": f'{q.args._title}',
        "imageId": f'{q.args._imageId}',
        "instanceType": f'{q.args._instanceType}',
        "durationMinutes": f'{q.args._durationMinutes}',
        "instructions": f'{str(df.loc[int(q.args._labId)-1].at["instructions"])}',
        "cloudTemplate": f'{str(df.loc[int(q.args._labId)-1].at["cloudTemplate"])}',
    }
    response = session_holder.post(url_api_instructor_lab_number, data=data, verify=False)
    print(response.status_code)

    
    
      
       


