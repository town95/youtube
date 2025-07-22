import requests
import re

SERVER = "https://client.webhostmost.com/clientarea.php?action=services"
HEADERS = {'Cookie': 'WHMCSlogin_auth_tk=dummy=='}

HTML_FILE = "login.html"

response = requests.get(SERVER, headers=HEADERS)
response.raise_for_status() # ensure we notice bad responses

with open(HTML_FILE, "wb") as file:
    file.write(response.content)

timeUntil = re.findall(r'Time until suspension:', response.text)
print(timeUntil)
if len(timeUntil) > 0 :
    print('success')
else :
    print('failed')

print('StatusCode: {}, StatusDescription: {}'.format(response.status_code, response.ok))
