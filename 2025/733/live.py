import requests
import re
import urllib


URL_LOGIN = "https://client.webhostmost.com/login"
DA_LOGIN = 'user@example.com'
DA_PASS = 'pwd'
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

HTML_FILE1 = "login1.html"
HTML_FILE2 = "login2.html"


client = requests.session()
response = client.get(URL_LOGIN)
response.raise_for_status() # ensure we notice bad responses

with open(HTML_FILE1, "wb") as file:
    file.write(response.content)

# Retrieve the CSRF token first (three express, anyone below)
#tokens = re.findall(r"csrfToken = '(.*?)'", response.text)
#tokens = re.findall(r'token: "(.*?)"', response.text)
tokens = re.findall(r'name="token" value="(.*?)"', response.text)
print(tokens)

params = 'token={}&username={}&password={}'.format(tokens[0], urllib.parse.quote(DA_LOGIN), DA_PASS)
print('params: {}'.format(params))

response2 = client.post(URL_LOGIN, data=params, headers=HEADERS)
response2.raise_for_status() # ensure we notice bad responses

with open(HTML_FILE2, "wb") as file:
    file.write(response2.content)

timeUntil = re.findall(r'Time until suspension:', response2.text)
print(timeUntil)
if len(timeUntil) > 0 :
    print('success')
else :
    print('failed')

print('StatusCode: {}, StatusDescription: {}, Cookie: {}'.format(response2.status_code, response2.ok, response2.cookies))
