import requests
import re

SERVER = "http://sv66.dataonline.vn"
PORT_START = 35000
PORT_END = 36000

HTML_FILE = "sv66.html"

for i in range(PORT_START, PORT_END, 1) :
  try :
    response = requests.get(f"{SERVER}:{i}/sub")
    response.raise_for_status() # ensure we notice bad responses

    if response.ok :
        with open(HTML_FILE, "ab") as file:
            print(i)
            file.write(response.content)

  except Exception as e:
    #msg = 'error with build:{0}'.format(str(e))
    #print(msg)

    continue

#print('StatusCode: {}, StatusDescription: {}'.format(response.status_code, response.ok))
