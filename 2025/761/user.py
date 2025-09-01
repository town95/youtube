from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

from urllib.parse import parse_qs, urlparse,  unquote
import json
import urllib

import requests
from requests.auth import HTTPBasicAuth

DA_HOST = 'https://server3.webhostmost.com:2222'
DA_LOGIN = 'hostmost3'
DA_PASS = '9numzJQ-Pf-n4n6F9xl8QbWN_trdrZQp'
AUTH = HTTPBasicAuth(DA_LOGIN, DA_PASS)
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('path = {}'.format(self.path))
      
        parsed_path = urlparse(self.path)
        pq = parse_qs(parsed_path.query)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, pq))

        username = ''
        suspended = ''
        
        if len(pq.get('username', [])) > 0 :
            username = pq.get('username', [])[0]

        if len(pq.get('suspended', [])) > 0 :
            suspended = pq.get('suspended', [])[0]

        print('query: username = {}, suspended = {}'.format(username, suspended))
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')

        elif parsed_path.path == '/sub':
            try:
                if username == '' :
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'No username')
                    return

                elif suspended.upper() in ['NO', 'YES'] :
                    if suspended.upper() == 'YES' :
                    	params = f"location=CMD_SELECT_USERS&suspend=Suspend&select0={username}"
                    else :
                    	params = f"location=CMD_SELECT_USERS&suspend=Unsuspend&select0={username}"

                    print(params)

                    url_post = f"{DA_HOST}/CMD_API_SELECT_USERS"
                    response2 = requests.post(url_post, data=params, auth=AUTH, headers=HEADERS)
                    params2 = dict(x.split('=') for x in unquote(response2.text).strip().split('&') if '=' in x)
                    print(params2)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(str(params2).encode('utf-8'))
                    return

                else:
                    url = f"{DA_HOST}/CMD_API_SHOW_USER_CONFIG?user={username}"
                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    params = dict(x.split('=') for x in unquote(response.text).strip().split('&') if '=' in x)
                    print(response.text)
                    print(params)
                    print(json.dumps(params).encode())
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(params).encode())
                    return

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write("error with build:{0}".format(str(e)).encode())
                return
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

server_address = ('', 8080)
print("serving at port", 8080)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
httpd.serve_forever()