import requests
import json
url = 'http://10.73.148.236:8080/iCloud/fileUpload/uploadFile.dox?token=5846be1f777c486b89c2e4e70a199d2a'
path = 'abc.war'
files = {'file': open(path, 'rb')}
r = requests.post(url, files=files)
data = r.text
# d = data.encode('utf-8')
t =json.loads(data)
print t['data']['id'],t['data']['fileName']
# t = eval(t)
print type(t)