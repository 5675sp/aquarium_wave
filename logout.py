import session

def logout_method():

    s = session.get_session()
    url_logout = "https://aquarium.h2o.ai/api/logout"
    s.get(url_logout, verify=False)
    print('user has been logout')

