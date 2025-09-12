from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

from urllib.parse import parse_qs, urlparse,  unquote
import json
import urllib

import requests
from requests.auth import HTTPBasicAuth

DA_HOST = 'https://server7.webhostmost.com:2222'
DA_LOGIN = 'username'
DA_PASS = 'password'
AUTH = HTTPBasicAuth(DA_LOGIN, DA_PASS)
HEADERS = {'Content-Type': 'application/json'}

EXPIRES_ON = '2025-10-06T12:06:02.000Z'

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('path = {}'.format(self.path))
      
        parsed_path = urlparse(self.path)
        pq = parse_qs(parsed_path.query)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, pq))

        action = ''
        keyname = ''
        keyvalue = ''
        id = ''
        
        if len(pq.get('action', [])) > 0 :
            action = pq.get('action', [])[0]

        if len(pq.get('keyname', [])) > 0 :
            keyname = pq.get('keyname', [])[0]

        if len(pq.get('keyvalue', [])) > 0 :
            keyvalue = pq.get('keyvalue', [])[0]

        if len(pq.get('id', [])) > 0 :
            id = pq.get('id', [])[0]

        print('query: action = {}, keyname = {}, keyvalue = {}, id = {}'.format(action, keyname, keyvalue, id))
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')

        elif parsed_path.path == '/loginkey':
            try:
                if action == '' :
                    url = f"{DA_HOST}/api/login-keys/keys"

                    if keyname != '' :
                        url = f"{DA_HOST}/api/login-keys/keys/{keyname}"

                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                elif action == 'commands' :
                    url = f"{DA_HOST}/api/login-keys/commands"

                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                elif action == 'log' :
                    if keyname == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No keyname')
                        return

                    url = f"{DA_HOST}/api/login-keys/keys/{keyname}/history"

                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                elif  action== 'create' :
                    if keyname == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No keyname')
                        return

                    if keyvalue == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No keyvalue')
                        return

                    params = {}
                    params['hasExpiry'] = True
                    params['expires'] = EXPIRES_ON
                    params['autoRemove'] = True
                    params['allowLogin'] = True
                    params['allowCommands'] = []
                    params['denyCommands'] = []
                    params['allowNetworks'] = []
                    params['id'] = keyname
                    params['password'] = keyvalue
#when the user(DA_LOGIN) is not a admin role, please delete the # (it is necessary only with GUI)
#in fact, it is not necessary when calling API to create a login key
#                    params['currentPassword'] = DA_PASS

                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_post = f"{DA_HOST}/api/login-keys/keys"
                    response2 = requests.post(url_post, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                elif  action== 'save' :
                    if keyname == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No keyname')
                        return

                    params = {}
                    params['hasExpiry'] = True
                    params['expires'] = EXPIRES_ON
                    params['autoRemove'] = True
                    params['allowLogin'] = True
                    params['allowCommands'] = []
                    params['denyCommands'] = []
                    params['allowNetworks'] = []
#                    params['id'] = keyname
                    if keyvalue != '' :
                        params['password'] = keyvalue
#when the user(DA_LOGIN) is not a admin role, please delete the # (it is necessary only with GUI)
#in fact, it is not necessary when calling API to create a login key
#                    params['currentPassword'] = DA_PASS

                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_patch = f"{DA_HOST}/api/login-keys/keys/{keyname}"
                    response2 = requests.patch(url_patch, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                elif  action== 'delete' :
                    if keyname == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No keyname')
                        return

                    url_delete = f"{DA_HOST}/api/login-keys/keys/{keyname}"
                    response2 = requests.delete(url_delete, auth=AUTH)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write('action parameter wrong'.encode())
                    return

            except Exception as e:
                msg = 'error with build:{0}'.format(str(e))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(msg.encode())
                return

        elif parsed_path.path == '/loginurl':
            try:
                if action == '' :
                    url = f"{DA_HOST}/api/login-keys/urls"

                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                elif  action== 'create' :
                    params = {}
                    params['expires'] = EXPIRES_ON
                    params['redirectURL'] = ''
                    params['allowNetworks'] = []
#when the user(DA_LOGIN) is not a admin role, please delete the # (it is necessary only with GUI)
#in fact, it is not necessary when calling API to create a login key
#                    params['currentPassword'] = DA_PASS

                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_post = f"{DA_HOST}/api/login-keys/urls"
                    response2 = requests.post(url_post, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                elif  action== 'delete' :
                    if id == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No id')
                        return

                    url_delete = f"{DA_HOST}/api/login-keys/urls/{id}"
                    response2 = requests.delete(url_delete, auth=AUTH)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write('action parameter wrong'.encode())
                    return

            except Exception as e:
                msg = 'error with build:{0}'.format(str(e))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(msg.encode())
                return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

server_address = ('', 8080)
print("serving at port", 8080)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
httpd.serve_forever()