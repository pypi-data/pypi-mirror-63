import sys, os, datetime, json, mimetypes 

if sys.version_info.major < 3:
    from  urlparse import urlparse, parse_qs
    import SocketServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
else:
    from urllib.parse import urlparse, parse_qs
    from http.server import SimpleHTTPRequestHandler,socketserver as SocketServer

#Static resource path
ResoursePath = os.path.dirname(__file__) + "/static"

#Handler dict
RequestHandlers = {}

# default df which returns vmstat command result parsed.
def df(opts="") :
    outputLines = os.popen("df " + opts).read().splitlines()
    keywords = outputLines[0].split()
    disks = []
    for i in range(1,len(outputLines)):
        disk = {}
        values = outputLines[i].split()
        for j in range(len(values)) :
            disk[keywords[j]]= values[j]
        disks.append(disk)
    return disks

# default vmstat which returns vmstat command result parsed.
def vmstat(opts="") :
    outputLines = os.popen("vmstat " + opts).read().splitlines()
    keywords = outputLines[-2].split()
    cpu = {}
    values = outputLines[-1].split()
    for i in range(len(values)) :
        cpu[keywords[i]]= values[i]
    return cpu

RequestHandlers.update({"/df" : df})
RequestHandlers.update({"/vmstat" : vmstat})

# add or replace handler for path.
# path : requestPath, handler : function returns string or object which is json compatible: list or dict etc...
def onGet(path, handler) :
    RequestHandlers.update({path : handler})

class PortHoleHandler(SimpleHTTPRequestHandler) :
    def serve(self) :
        tmp = self.path.split("?",1)
        path = tmp[0]
        qs = tmp[1] if len(tmp) > 1 else ""
        queryParam = parse_qs(qs)

        # respond with registered handlers
        if path in RequestHandlers :
            data = RequestHandlers.get(path)()
            contentType = "application/json"
            if data is str :
                try :
                    json.loads(data)
                except :
                    contentType = "text/plain"
            else :
                data = json.dumps(data)
                
            self.response["code"] = 200
            self.response["contentType"] = contentType
            self.response["data"] = data
            return

        #response with static resource
        if path == "/" or path == "":
           path = "/index.html"

        self.response["code"] = 200
        self.response["contentType"] = self.guess_type(path)
        global ResoursePath
        self.response["filePath"] = os.path.abspath(ResoursePath) + path
        return

    def onError(self, error) :
        self.response["code"] = 500
        self.response["contentType"] =  "text/plain"
        self.response["data"] = str(error)

    def do_GET(self) :
        self.response = {"code" :200, "contentType":"", "data":None, "filePath":None}
        try :
            self.serve()
        except Exception as error :
            self.onError(error)
        finally :
            if self.response["filePath"] != None :
                try :
                    f = open(self.response["filePath"], "rb")
                    fs = os.fstat(f.fileno())
                    self.send_response(200)
                    self.send_header("Content-type", self.guess_type(self.response["filePath"]))
                    self.send_header("Content-Length", str(fs[6]))
                    self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                    self.end_headers()
                    self.copyfile(f, self.wfile)
                    f.close()
                    return
                except Exception as fErr:
                    self.send_response(404, "file not found : " + self.response["filePath"])
                    return
            
            self.send_response(200)
            self.send_header("Content-type", self.response["contentType"])
            self.send_header("Content-Length", len(self.response["data"]))          
            self.end_headers()
            self.wfile.write(self.response["data"].encode())
        return

def serve(host="", port=8000) : 
    print("Porthole server at :[" + host + ":" +  str(port)+"]")
    httpd = SocketServer.TCPServer((host, port), PortHoleHandler)
    httpd.serve_forever()

