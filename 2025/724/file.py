from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

from urllib.parse import parse_qs, urlparse,  unquote
import json
import urllib

import requests
from requests.auth import HTTPBasicAuth

DA_HOST = 'https://server8.webhostmost.com:2222'
DA_LOGIN = 'username'
DA_PASS = 'password'
AUTH = HTTPBasicAuth(DA_LOGIN, DA_PASS)
HEADERS = {'Content-Type': 'application/json'}

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('path = {}'.format(self.path))
      
        parsed_path = urlparse(self.path)
        pq = parse_qs(parsed_path.query)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, pq))

        action = ''
        path = ''
        chmod = ''
        username = ''

        if len(pq.get('action', [])) > 0 :
            action = pq.get('action', [])[0]

        if len(pq.get('path', [])) > 0 :
            path = pq.get('path', [])[0]

        if len(pq.get('chmod', [])) > 0 :
            chmod = pq.get('chmod', [])[0]

        if len(pq.get('username', [])) > 0 :
            username = pq.get('username', [])[0]

        print('query: action = {}, path = {}, chmod = {}, username = {}'.format(action, path, chmod, username))
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')

        elif parsed_path.path == '/dir':
            try:
                if action in ['', 'tree'] :
                    if path == '' :
                        path = '/'

                    url = f"{DA_HOST}/CMD_FILE_MANAGER?json=yes&action=parent_tree&path={path}"
                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                elif action == 'all' :
                    if path == '' :
                        path = '/'

                    url = f"{DA_HOST}/CMD_FILE_MANAGER?json=yes&action=json_all&path={path}"
                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write('action parameter wrong'.encode())
                    return

            except Exception as e:
                msg = 'error with build:{0}'.format(str(e))
                print(msg)

                self.send_response(500)
                self.end_headers()
                self.wfile.write(msg.encode())
                return

        elif parsed_path.path == '/file':
            try:
                if path == '' :
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'No path')
                    return

                elif chmod != '' :

                    params = {}
                    params['select0'] = path
                    params['json'] = 'yes'
                    params['action'] = 'multiple'
                    params['permission'] = 'yes'
                    params['chmod'] = chmod
                    params['recursive'] = 'no'


                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_post = f"{DA_HOST}/CMD_FILE_MANAGER?json=yes"
                    response = requests.post(url_post, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

                else :
                    url = f"{DA_HOST}/CMD_FILE_MANAGER?path={path}"
                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return

            except Exception as e:
                msg = 'error with build:{0}'.format(str(e))
                print(msg)

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