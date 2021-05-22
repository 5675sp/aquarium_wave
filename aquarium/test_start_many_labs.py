import time
import http.client
import urllib.parse
from collections import OrderedDict
import argparse
import threading
import socket
import ssl


# noinspection PyMethodMayBeStatic
class TestClient (threading.Thread):
    def __init__(self, n, server, email, password, lab_id):
        threading.Thread.__init__(self)
        self.n = n
        self.email = email
        self.password = password
        self.lab_id = lab_id
        self.jsessionid = ""
        self.connection = http.client.HTTPSConnection(server, context=ssl._create_unverified_context())
        
        pass

    def print(self, message):
        print("User " + str(self.n) + " says: " + message)

    def pause(self, millis):
        time.sleep(millis / 1000.0)
        pass

    def headers(self):
        r = OrderedDict()
        r["Accept"] = "*/*"
        r["Cookie"] = "JSESSIONID=" + self.jsessionid
        return r

    def get_static_asset(self, url):
        
        
        self.connection.request("GET", url)
        
       
        #response = requests.get('http://aquarium.h2o.ai' + url , verify=False)
       

        r = self.connection.getresponse()

        #r = response
       
        #print('USING REQUETS')
        print(r.status)
        
        
     
        assert r.status == 200
        r.read()
        #print(r.content)
        #r.content


    def get_static_assets(self):
        urls = [
            "/runtime.ec2944dd8b20ec099bf3.js",
            "/main.069e35f8567a0547374c.js",
            "/styles.087577d94229e7bee9ae.css",
            "/polyfills.20ab2d163684112c2aba.js"
        ]

        for url in urls:
            self.get_static_asset(url)
            print('LINE-----------')
            

    def api_login(self):
        params = urllib.parse.urlencode({'reCaptchaSolution': '', 'email': self.email, 'password': self.password, 'withCredentials': 'true'})
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        self.connection.request("POST", "/api/login", params, headers)
        
        r = self.connection.getresponse()

        #print('LOGIN-CODE:')
        #print(r.status)
        #print(r.reason)

      
        #r = requests.post('http://aquarium.h2o.ai/api/login', data = {'reCaptchaSolution': '', 'email':'sergio.perez@h2o.ai', 'password': 'FuE9zhYa20!', 'withCredentials': 'true' }, headers=headers, verify=False)
       


        #print(r.text)
        print(r.status)
        print(r.headers)
        print(r.read().decode())
        #print(r.status_code)
        #print(r.headers)
        #print(r.cookies)
        
        assert r.status == 200
        #assert r.status_code == 200
        r.read()
        #r.content
        #print(r.content)
        #print('----------')
        
      
       
        
        cookie_string = r.getheader("Set-cookie")
        
        #cookie_string = r.headers['Set-cookie']
        cookie_lhs_rhs = cookie_string.split(";")
        parts = cookie_lhs_rhs[0].split("=")
        assert parts[0] == "JSESSIONID"
        self.jsessionid = parts[1]
        

    def get_api_topbar(self):
        self.connection.request("GET", "/api/topbar", headers=self.headers())
        r = self.connection.getresponse()
        assert r.status == 200
        r.read()

    def get_api_leftbar(self):
        self.connection.request("GET", "/api/leftbar", headers=self.headers())
        r = self.connection.getresponse()
        assert r.status == 200
        r.read()

    def get_api_dashboard(self):
        self.connection.request("GET", "/api/dashboard", headers=self.headers())
        r = self.connection.getresponse()
        assert r.status == 200
        r.read()

    def get_api_labs(self):
        self.connection.request("GET", "/api/lab", headers=self.headers())
        r = self.connection.getresponse()
        assert r.status == 200
        r.read()

    def get_api_lab(self, lab_id):
        self.connection.request("GET", "/api/lab/" + str(lab_id), headers=self.headers())
        r = self.connection.getresponse()
        assert r.status == 200
        r.read()

    def post_api_start_lab(self, lab_id):
        params = urllib.parse.urlencode({'labId': str(lab_id)})
        headers = self.headers()
        headers["Content-type"] = "application/x-www-form-urlencoded"
        self.connection.request("POST", "/api/startLab", params, headers)
        r = self.connection.getresponse()
        assert r.status == 200
        r.read()
        

    def run(self):
        self.print("static assets")
        self.get_static_assets()

        self.pause(5000)

        self.print("login")
        self.api_login()

        self.print("dashboard")
        self.get_api_topbar()
        self.get_api_leftbar()
        self.get_api_dashboard()

        self.pause(5000)

        self.print("lab list")
        self.get_api_topbar()
        self.get_api_leftbar()
        self.get_api_labs()

        self.pause(5000)

        self.print("lab")
        self.get_api_topbar()
        self.get_api_leftbar()
        self.get_api_lab(self.lab_id)

        self.pause(5000)

        self.print("start lab")
        self.post_api_start_lab(self.lab_id)

        i = 0
        #n = 100
        n = 1
        while i < n:
            self.print("poll lab (" + str(i) + " of " + str(n) + ")")
            self.get_api_lab(self.lab_id)
            self.pause(15 * 1000)
            i = i + 1


class TestRunner:
    def __init__(self, server, domain, password, start, end, lab_id):
        self.server = server
        self.domain = domain
        self.password = password
        self.start = start
        self.end = end
        self.lab_id = lab_id

    def run(self):
        threads = []

        ip_address = socket.gethostbyname(self.server)

        i = self.start
        while i <= self.end:
            #email = "aquarium.test." + str(i) + "@" + self.domain
            email = "sergio.perez" + "@" + self.domain
            c = TestClient(i, ip_address, email, self.password, self.lab_id)
            threads.append(c)
            c.start()
            i = i + 1

        # Wait infinitely.  Break out with a human CTRL-C.
        print("WAITING...")
        while True:
            
            time.sleep(10)


def main():
    parser = argparse.ArgumentParser(description='Run load test on aquarium')
    parser.add_argument("--server", type=str, required=True, help="e.g. aquarium.h2o.ai")
    parser.add_argument("--domain", type=str, required=True, help="e.g. h2o.ai")
    parser.add_argument("--password", type=str, required=True)
    parser.add_argument("--start", type=int, required=True, help="index of first test user; e.g. 1")
    parser.add_argument("--end", type=int, required=True, help="index of last test user; e.g. 500")
    parser.add_argument("--lab_id", type=int, required=True, help="aquarium lab id; e.g. 1")
    args = parser.parse_args()
    runner = TestRunner(args.server, args.domain, args.password, args.start, args.end, args.lab_id)
    runner.run()


if __name__ == '__main__':
    main()