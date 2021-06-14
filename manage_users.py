from numpy.lib.function_base import append
from h2o_wave import Q, ui
import pandas as pd  

import session

from tzlocal import get_localzone
import pytz
from datetime import datetime
from dateutil import relativedelta


class User:
    def __init__(self, userId: str, role: str, name: str, email: str, logins: str, lastLoginTime: str, countLabInstances: str):
        self.id = userId
        self.userId = userId
        self.role = role
        self.name = name
        self.email = email
        self.logins = logins
        self.lastLoginTime = lastLoginTime
        self.countLabInstances = countLabInstances

def users_metrics(filter:bool):

    global filter_status
    filter_status = filter


    session_holder = session.get_session()
    url_api_user = "https://aquarium.h2o.ai/api/user"
    req = session_holder.get(url_api_user, verify=False)
    jsonRes = req.json()
    global number_of_users
    number_of_users = len(jsonRes)
    df = pd.DataFrame.from_records(jsonRes)
    
    index = df.index
    number_of_rows = len(index)


    recent_logins = []
    for i in range(number_of_rows):
        holder = last_logged_in(df.loc[i].at["lastLoginTime"])

        if holder[1] != False:
            recent_logins.append(i)
    
    global number_of_recent_logins    
    number_of_recent_logins = len(recent_logins)

    if filter:
        global aquarium_users
        aquarium_users = [
            User(
                userId= str(df.loc[recent_logins[i]].at["userId"]),
                role=df.loc[recent_logins[i]].at["role"],
                name=str(df.loc[recent_logins[i]].at["name"]),
                email=str(df.loc[recent_logins[i]].at["email"]),
                logins=str(df.loc[recent_logins[i]].at["logins"]),
                lastLoginTime=last_logged_in(df.loc[recent_logins[i]].at["lastLoginTime"])[0],
                countLabInstances=str(df.loc[recent_logins[i]].at["countLabInstances"])) for i in range(number_of_recent_logins)
        ]
    else:
        aquarium_users = [
            User(
                userId= str(df.loc[i].at["userId"]),
                role=df.loc[i].at["role"],
                name=str(df.loc[i].at["name"]),
                email=str(df.loc[i].at["email"]),
                logins=str(df.loc[i].at["logins"]),
                lastLoginTime=last_logged_in(df.loc[i].at["lastLoginTime"])[0],
                countLabInstances=str(df.loc[i].at["countLabInstances"])) for i in range(number_of_users)
        ]




async def users(q: Q, filter:bool):

    columns = [
        ui.table_column(name='userId', label='ID', max_width = '50px', searchable=True),
        ui.table_column(name='role', label='Role', max_width = '300px', searchable=True, filterable=True),
        ui.table_column(name='name', label='Name', searchable=True),
        ui.table_column(name='email', label='Email', searchable=True),
        ui.table_column(name='logins', label='Logins', searchable=True),
        ui.table_column(name='last_logged_in', label='Last logged in', searchable=True, filterable=True),
        ui.table_column(name='labs_taken', label='Labs taken', searchable=True),
    ]

    q.page['active_users'] = ui.form_card(box='3 1 -1 -1', items=[
        ui.progress('Loading users...')
    ])

    await q.page.save()


    users_metrics(filter)

    q.page['active_users'] = ui.form_card(box='3 1 -1 -1', items=[
        ui.separator(label=f'There are {number_of_users} users'),
        ui.separator(label=f'{number_of_recent_logins} users have logged in within the last eight hours'),
        ui.buttons([ \
            ui.button(name='refresh_manage_users_page', label='Refresh Page', primary=True)
        ], justify='center'),
        ui.buttons([ \
            ui.button(name='unfilter', label='Unfilter', primary=True),
            ui.button(name='filter', label='Filter', primary=True)
        ], justify='center'),
        ui.table(
            name='users',
            columns=columns,
            rows=[ui.table_row(
                name=user.id, cells=[user.userId, user.role,user.name, user.email, user.logins, user.lastLoginTime, user.countLabInstances]) for user in aquarium_users],
            downloadable=True,
            groupable=True,
            resettable=True,
            height='1000px'
        ),
    ])

    await q.page.save()



def last_logged_in(timestamp: int):

    if timestamp != 0:

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
        difference = relativedelta.relativedelta(date_2, date_1)

  
        years = difference.years
        months = difference.months
        days = difference.days
        hours = difference.hours
        minutes = difference.minutes

        #print('********')
        #print(years)
        #print(months)
        #print(days)
        #print(hours)
        #print(minutes)
        #print('********')

        past_eight_hours = False

        if years == 0 and months == 0 and days == 0:
            
            if hours < 8:
                past_eight_hours = True 
          
                


        if years == 0 and  months == 0 and days == 0 and hours == 0 and minutes == 0:
            return ['just now', past_eight_hours]

        if years != 0:
            if years == 1:
                return [f'{str(years)} year ago', past_eight_hours]
            else:
                return [f'{str(years)} years ago', past_eight_hours]
        elif months != 0:
            if months == 1:
                return [f'{str(months)} month ago', past_eight_hours]
            else:
                return [f'{str(months)} months ago', past_eight_hours]
        elif days != 0:
            if days == 1:
                return [f'{str(days)} day ago', past_eight_hours]
            else:
                return [f'{str(days)} days ago', past_eight_hours]
        elif hours != 0:
            if hours == 1:
                return [f'{str(hours)} hour ago', past_eight_hours]
            else: 
                return [f'{str(hours)} hours ago', past_eight_hours]
        elif minutes != 0:
            if minutes == 1:
                return [f'{str(minutes)} minute ago', past_eight_hours]
            else:
                return [f'{str(minutes)} minutes ago', past_eight_hours]

        

    else:
        return ['Never logged in', False]

    


