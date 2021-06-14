from h2o_wave import main, app, Q, ui
import manage_labs
import browse_labs
import dashboard
import session
import download_instances_csv
import manage_active_lab_instances
import manage_users
import manage_pre_warming


from logout import logout_method

async def setup_page(q: Q, user_name: str, user_role: str):

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
                ui.nav_item(name='manage_users', label='Manage Users'),
            ]),
            ui.nav_group('Reports', items=[
                ui.nav_item(name='recent_instances', label='Most Recent Instances (100)'),
                ui.nav_item(name='downloadInstancesCsv', label='Download Instances CSV'),
            ]),
            ui.nav_group(f'{user_name} ({user_role})', items=[
                ui.nav_item(name='logout', label='Logout'),
                #ui.nav_item(name='changePassword', label='Change Password'),
            ]),
            ui.nav_group('Theme', items=[
                ui.nav_item(name='neon', label='Neon')
            ]),
        ], 
    )

    await q.page.save()

async def delete_cards(q: Q):
    names = [
        'metrics',
        'editButtons',
        'metricsDashboard',
        'visiablelabs',
        'moreSettings',
        'individualab',
        'csv',
        'activelabs',
        'activeLabButtons',
        'active_users',
        'controller',
        'manage_pre_warming',
        'batch_details',
        'manage_pre_warming_settings'
    ]

    for name in names:
        del q.page[f'{name}']

    await q.page.save()

async def update_batch_metrics(q: Q):
    id = manage_pre_warming.current_batch
    manage_pre_warming.batch_details_api_call(id)
    q.page['batch_details'].items[4].text_m.content = manage_pre_warming.batch_metrics_body()
    await q.page.save()
    
@app('/aquarium')
async def serve(q: Q):

    

    #|-------------------------session.py-------------------------|
    if not q.client.initialized:
        q.page['meta'] = ui.meta_card(box='')
        q.client.theme = 'default'
        q.client.initialized = True

        await session.login_options(q)
   
    if q.args.loginbutton:

       
        session.start_session(q.args.email, q.args.password)
        
        valid = session.get_valid()

        if valid:
            q.page.drop()
            q.page['meta'] = ui.meta_card(box='')
            q.client.theme = 'default'
            nameRole = session.top_bar()
            await setup_page(q, nameRole['userName'], nameRole['userRole'])
            dashboard.dashboard_metrics()
            await dashboard.dashboard(q) 
        else: 
            await session.login_failed(q)
       
    if q.args.option_one_openid:
        await session.login(q)

    if q.args.option_two_create_account:
        await session.creat_account(q)

    if q.args.back_from_login_page:
        await session.login_options(q)

    if q.args.back_from_create_account_page:
        await session.login_options(q)

    if q.args.logout:
        browse_labs.exit = True
        await delete_cards(q)
        logout_method()
        await session.login_options(q)


    #|-------------------------manage_labs.py-------------------------|
        
    if q.args.managelabs:
        browse_labs.exit = True
        await delete_cards(q)
        manage_labs.manage_labs()
        await manage_labs.manage_lab_settings(q)
        await manage_labs.lab_metrics(q, 0, True)

    if q.args.tableoflabs:
        await manage_labs.lab_metrics(q, (int(q.args.tableoflabs[0])), True)
        
    if q.args.editLab:
     
        await manage_labs.pop_settings(q)


    if q.args.enabledLab:
        await manage_labs.enabled_lab(q, 'true')
        print('enabledLab')

    if q.args.disabledLab:
        await manage_labs.enabled_lab(q, 'false')
      

    if q.args.cancel:
        await delete_cards(q)
        manage_labs.manage_labs()
        await manage_labs.manage_lab_settings(q)
        await manage_labs.lab_metrics(q, manage_labs.current_selected_lab, True)

    if q.args.save:
        manage_labs.save_lab_metrics(q)
        await delete_cards(q)
        manage_labs.manage_labs()
        await manage_labs.manage_lab_settings(q)
        await manage_labs.lab_metrics(q, manage_labs.current_selected_lab, True)

    if q.args.enabledLabQuickSettings:
        await manage_labs.lab_metrics(q, manage_labs.current_selected_lab, False)

    if q.args.cancelBaseSettings:
        await manage_labs.lab_metrics(q, manage_labs.current_selected_lab, True)

    if q.args.saveBaseSettings:
        manage_labs.save_quick_base_settings(q)
        await delete_cards(q)
        manage_labs.manage_labs()
        await manage_labs.manage_lab_settings(q)
        await manage_labs.lab_metrics(q, manage_labs.current_selected_lab, True)
        

    #|-------------------------browse_labs.py-------------------------|

    if q.args.browselabs: 
        browse_labs.exit = True
        await delete_cards(q)
        browse_labs.api_lab()
        await browse_labs.browse_labs(q)

    if q.args.labs: 
        await delete_cards(q)
        await browse_labs.individual_lab(q, (int(q.args.labs[0])))
        
    if q.args.startLab:
        lab_id = browse_labs.create_lab_instance()
        await browse_labs.individual_lab(q,lab_id)
       
    if q.args.endLab:
        await browse_labs.end_instance(q)

    if q.args.dashboard_message: #button to go to the browse labs page 
        await delete_cards(q)
        browse_labs.api_lab()
        await browse_labs.browse_labs(q)


    #|-------------------------dashboard.py-------------------------|


    if q.args.dashboard:
        browse_labs.exit = True
        await delete_cards(q)
        dashboard.dashboard_metrics()
        await dashboard.dashboard(q)

    if q.args.refresh_dashboard: # refresh dashboard page 
        await delete_cards(q)
        dashboard.dashboard_metrics()
        await dashboard.dashboard(q) 

    if q.args.syncNow:
        dashboard.start_sync()
        await delete_cards(q)
        dashboard.dashboard_metrics()
        await dashboard.dashboard(q) 


    if q.args.user_active_lab_instances:
        await delete_cards(q)
        await browse_labs.individual_lab(q, (int(q.args.user_active_lab_instances[0])))


    #|-------------------------manage_active_lab_instances.py-------------------------|


    if q.args.manage_active_lab_instances:
        browse_labs.exit = True
        await delete_cards(q)
        manage_active_lab_instances.active_labs()
       
        await manage_active_lab_instances.active_labs_table(q)
        await manage_active_lab_instances.active_lab_metrics(q, 0)

    if q.args.tableofactivelabs:
        await manage_active_lab_instances.active_lab_metrics(q, (int(q.args.tableofactivelabs[0])))

    if q.args.refresh_manage_active_lab_instances_page: 
        await delete_cards(q)
        manage_active_lab_instances.active_labs()
    
        await manage_active_lab_instances.active_labs_table(q)
        await manage_active_lab_instances.active_lab_metrics(q, 0)

    if q.args.extend: #if the extend button is click extend the lab instance 
        await delete_cards(q)
        manage_active_lab_instances.extend_lab_instance_method(q.args.liId)
        manage_active_lab_instances.active_labs()
        await manage_active_lab_instances.active_labs_table(q)
        await manage_active_lab_instances.active_lab_metrics(q,manage_active_lab_instances.selected_lab_instance)


    #|-------------------------manage_pre_warming.py-------------------------|

    
    if q.args.manage_pre_warming: #manage pre-warming batches 
        browse_labs.exit = True
        await delete_cards(q)
        await manage_pre_warming.manage_pre_warming(q)

    if q.args.create_new_pre_warming_batch: #create new pre-warm batch settings 
        await manage_pre_warming.pop_manage_pre_warming_settings(q)

    if q.args.active_batches: #show batch details of a given batch
        await delete_cards(q)
        manage_pre_warming.batch_details_api_call(q.args.active_batches[0])
        await manage_pre_warming.batch_details(q, q.args.active_batches[0])

    if q.args.create_batch: # button to create a batch 
        manage_pre_warming.start_batch(q.args.dropdown,q.args.number_of_instances)
        del q.page['manage_pre_warming_settings']
        await manage_pre_warming.manage_pre_warming(q)

    if q.args.batch_details_refresh_page: #refresh batche page detail
        
        id = manage_pre_warming.current_batch
        await delete_cards(q)
        manage_pre_warming.batch_details_api_call(id)
        await manage_pre_warming.batch_details(q, id)
    
    if q.args.enable_one:
        q.page['batch_details'].items[3].inline.items[0].toggle.value = True
        q.page['batch_details'].items[3].inline.items[1].button.disabled = False
        q.page['batch_details'].items[3].inline.items[2].button.disabled = False
        q.page['batch_details'].items[3].inline.items[3].button.disabled = False
        q.page['batch_details'].items[3].inline.items[4].button.disabled = False
     

    if q.args.enable_one == False:
        q.page['batch_details'].items[3].inline.items[0].toggle.value = False
        q.page['batch_details'].items[3].inline.items[1].button.disabled = True
        q.page['batch_details'].items[3].inline.items[2].button.disabled = True
        q.page['batch_details'].items[3].inline.items[3].button.disabled = True
        q.page['batch_details'].items[3].inline.items[4].button.disabled = True


    if q.args.enable_two:
        q.page['batch_details'].items[5].inline.items[0].toggle.value = True
        q.page['batch_details'].items[5].inline.items[1].button.disabled = False

    if q.args.enable_two == False:
        q.page['batch_details'].items[5].inline.items[0].toggle.value = False
        q.page['batch_details'].items[5].inline.items[1].button.disabled = True

    if q.args.enable_three:
        q.page['batch_details'].items[6].inline.items[0].toggle.value = True
        q.page['batch_details'].items[6].inline.items[1].button.disabled = False

    if q.args.enable_three == False:
        q.page['batch_details'].items[6].inline.items[0].toggle.value = False
        q.page['batch_details'].items[6].inline.items[1].button.disabled = True
  
    if q.args.enable_four:
        q.page['batch_details'].items[7].inline.items[0].toggle.value = True
        q.page['batch_details'].items[7].inline.items[1].button.disabled = False

    if q.args.enable_four == False:
        q.page['batch_details'].items[7].inline.items[0].toggle.value = False
        q.page['batch_details'].items[7].inline.items[1].button.disabled = True

    await q.page.save()

    if q.args.add_one_instance:
        manage_pre_warming.add_instances(1)
        await update_batch_metrics(q)

    if q.args.add_five_instances:
        manage_pre_warming.add_instances(5)
        await update_batch_metrics(q)
    
    if q.args.add_twenty_five_instances:
        manage_pre_warming.add_instances(25)
        await update_batch_metrics(q)

    if q.args.add_one_hundred_instances:
        manage_pre_warming.add_instances(100)
        await update_batch_metrics(q)

    if q.args.end_all_unclaimed_instances_in_batch:
        manage_pre_warming.end_unclaimed_in_pre_warm_batch()
        await update_batch_metrics(q)

    if q.args.end_all_instances_in_this_batch:
        manage_pre_warming.end_all_in_pre_warm_batch()
        await update_batch_metrics(q)

    if q.args.deactivate_batch:
        manage_pre_warming.deactivate_pre_warm_batch()
        manage_pre_warming.batch_details_api_call(manage_pre_warming.current_batch)
        q.page['batch_details'].items[2].text_m.content = manage_pre_warming.batch_metrics_header()
        q.page['batch_details'].items[4].text_m.content = manage_pre_warming.batch_metrics_body()
        await q.page.save()
        #await update_batch_metrics(q)





    #|-------------------------manage_users.py-------------------------|
    

    if q.args.manage_users:
        browse_labs.exit = True
        await delete_cards(q)
        await manage_users.users(q, True)

    if q.args.users: # when a row is click on the users page the table will be reload in order to avoid aninfitie reload 
        if manage_users.filter_status:
            await manage_users.users(q, True)
        else: 
            await manage_users.users(q, False)

    if q.args.refresh_manage_users_page: #refresh manage users page
        await delete_cards(q)
        if manage_users.filter_status:
            await manage_users.users(q, True)
        else: 
            await manage_users.users(q, False)

    if q.args.unfilter: #unfilter users table 
        await delete_cards(q)
        await manage_users.users(q, False)

    if q.args.filter: #filter users table 
        await delete_cards(q)
        await manage_users.users(q, True)        


    #|-------------------------download_instances_csv.py-------------------------|
    
    if q.args.recent_instances:
        browse_labs.exit = True
        await delete_cards(q)
        await download_instances_csv.csv_table(q)

    if q.args.instances:
        await download_instances_csv.csv_table(q)
    
    meta = q.page['meta']
    if q.args.neon:
        meta.theme = q.client.theme = 'neon' if q.client.theme == 'default' else 'default'
        await q.page.save()



        

    


    




    


    










    

    


    
   
        



  
    
    


