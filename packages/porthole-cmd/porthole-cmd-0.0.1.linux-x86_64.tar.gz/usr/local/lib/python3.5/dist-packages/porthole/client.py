import sys, json

def fetch(url) :
    if not url.startswith("http") :
        url = "http://" + url
    
    if sys.version_info.major < 3:
        from  urlparse import urlparse
        from httplib import HTTPConnection, HTTPSConnection
    else:
        from http.client import HTTPConnection, HTTPSConnection
        from urllib.parse import urlparse
    
    urlParts = urlparse(url)
    if url.startswith("https://") :
        conn = HTTPSConnection(urlParts.netloc)
    else :
        conn = HTTPConnection(urlParts.netloc)
    
    path = url.lstrip(urlParts.scheme+"://").lstrip(urlParts.netloc)
    conn.request("GET", path)
    response = conn.getresponse()
    if response.status != 200 :
        raise Exception("Fail to connect URI : "+ url + " - " + response.status + ":" + response.reason)
    data = response.read()
    try :
        return {"response":json.loads(data.decode("utf-8"))}
    except Exception as err :
        raise Exception("Fail to Decode : "+ data.decode("utf-8"))
    

## eval data.cpu.io > 0 and all(disk.used > 90 for disk in data.disks)
def test(uri, exp) : 
    try :
        data = fetch(uri)
        for n in data :
            print(n)
        result = eval(exp, globals(), data)
        if not result : 
            return (False, "Expression returned false.\n" +"Expression : " + exp + "\n" + json.dumps(data,indent=4))
        return (True,None)
    except Exception as err :
        return (False, err)
    