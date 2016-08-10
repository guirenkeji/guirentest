import httplib
import json

def httpdownloadpost (clientIp,params):
    data = {'url':params}
#     httpClient = None
    try:
        data = json.dumps(data)
        httpClient = httplib.HTTPConnection(clientIp,5015, timeout=30) 
        httpClient.request("POST",'/v2/client/download',data,{'Content-Type': 'application/json'})
        response = httpClient.getresponse()
        print response
    
    except Exception, e:
        print e 