from os import lockf
from h2o_wave import main, app, Q, ui
import manage_labs
import browse_labs
import dashboard
import session
import download_instances_csv
import manage_active_lab_instances
#from manage_active_lab_instances import manage_active_lab_instances


from h2o_wave.core import expando_to_dict


global lock
lock = True
async def setup_page(q: Q, userName: str, userRole: str):

    q.page['header1'] = ui.header_card(
        box='1 1 2 1',
        title='Aquarium',
        subtitle='H2O.ai',
    )

    q.page['nav'] = ui.nav_card(
        box='1 2 2 -1',
        items=[
            ui.nav_group('Menu', items=[
                ui.nav_item(name='dashboard', label='Dashboard'),
                ui.nav_item(name='browselabs', label='Browse Labs'),
            ]),
            ui.nav_group('Instructor', items=[
                ui.nav_item(name='manage_pre_warming', label='Manage Pre-Warming'),
                ui.nav_item(name='manage_active_lab_instances', label='Manage Active Lab Instances'),
                ui.nav_item(name='managelabs', label='Manage Labs'),
            ]),
            ui.nav_group('Admin', items=[
                ui.nav_item(name='manage-users', label='Manage Users'),
            ]),
            ui.nav_group('Reports', items=[
                ui.nav_item(name='downloadInstancesCsv', label='Download Instances CSV'),
            ]),
            ui.nav_group(f'{userName} ({userRole})', items=[
                ui.nav_item(name='logout', label='Logout'),
                ui.nav_item(name='changePassword', label='Change Password'),
            ])
        ], 
        
        
    )

    await q.page.save()

async def deleteCards(q: Q):
    names = [
        'metrics',
        'editButtons',
        'metricsDashboard',
        'visiablelabs',
        'moreSettings',
        'individualab',
        'csv',
        'manage_active_lab_instances',
        'activelabs',
        'activeLabButtons'

    ]

    for name in names:
        del q.page[f'{name}']

    await q.page.save()

@app('/aquarium')
async def serve(q: Q):


    if not q.client.initialized:
        q.client.initialized = True
        session.startSession('sergio.perez@h2o.ai', 'FuE9zhYa20!')
        nameRole = session.topbar()
        await setup_page(q, nameRole['userName'], nameRole['userRole'])
        dashboard.dashboardmethod()
        await dashboard.dashboard(q) #dasboard


        #await session.login(q)
   

    #if q.args.loginbutton:
       
        #session.startSession(q.args.email, q.args.password)
        #valid = session.getValid()

        #if valid:
            #q.page.drop()
            #await setup_page(q)
            #await dashboard.dashboard(q) #dasboard
        
  
            

    if q.args.managelabs:
        await deleteCards(q)
        manage_labs.managelabsmethod()
        await manage_labs.manageLabsSettings(q)
        await manage_labs.labMetrics(q, 0)
    
    if q.args.browselabs: # browse Labs 
        await deleteCards(q)
        browse_labs.browselabsmethod()
        await browse_labs.browselabs(q)

    if q.args.dashboard:
        await deleteCards(q)
        dashboard.dashboardmethod()
        await dashboard.dashboard(q) #dasboard 

    if q.args.tableoflabs:
        await manage_labs.labMetrics(q, (int(q.args.tableoflabs[0])))
        
    if q.args.editLab:
        await manage_labs.popSettings(q)

    if q.args.labs: #Particular browse lab -> Select a lab -> Request Lab Information -> 
        await deleteCards(q)
        await browse_labs.individualLab(q, (int(q.args.labs[0])))
        
    if q.args.startLab:
        lab_id = browse_labs.createLabInstanceMethod()
        await browse_labs.individualLab(q,lab_id)
       
    if q.args.endLab:
        await browse_labs.endInstance(q)

    if q.args.downloadInstancesCsv:
        await deleteCards(q)
        await download_instances_csv.csvTable(q)

    if q.args.instances:
        await download_instances_csv.csvTable(q)

    if q.args.manage_active_lab_instances:
        await deleteCards(q)
        manage_active_lab_instances.activeLabsMethod()
        await manage_active_lab_instances.manage_active_lab_instances(q)
        await manage_active_lab_instances.activeLabsTable(q)
        await manage_active_lab_instances.activeLabMetrics(q, 0)

    if q.args.tableofactivelabs:
        await manage_active_lab_instances.activeLabMetrics(q, (int(q.args.tableofactivelabs[0])))

    if q.args.refresh_page: #refresh active lab instances page
        await deleteCards(q)
        manage_active_lab_instances.activeLabsMethod()
        await manage_active_lab_instances.manage_active_lab_instances(q)
        await manage_active_lab_instances.activeLabsTable(q)
        await manage_active_lab_instances.activeLabMetrics(q, 0)


    

    



        

    


    




    


    










    

    


    
   
        



  
    
    


