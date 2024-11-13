import socket
import json
import time

host = "192.168.1.25"
port = 42069
profilefound = False
queried = False
query = None
lastmessage = None

while True:
    if not queried:
        if not profilefound:
            cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cserver.connect((host, port))
            clientName = "testing"
            request = {'type':'init', 'name':'nate', 'clientname':clientName}
            request = json.dumps(request)
            cserver.send(request.encode('utf-8'))
            result = cserver.recv(20000).decode('utf-8')
            result = json.loads(result)
            print(repr(result))
            cserver.close()
            profilefound = True
            profile = result['excess']
        cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cserver.connect((host,port))
        message = input("command > ")
        lastmessage = message
        start = round(time.time() * 1000)
        request = {'type':'command', 'profile':profile, 'message':message, 'excess':None}
        request = json.dumps(request)
        cserver.send(request.encode('utf-8'))
        result = cserver.recv(20000).decode('utf-8')
        result = json.loads(result)
        print(repr(result))
        print("\n\n" + result['result'] + "\n")
        finish = round(time.time() * 1000)
        print(f"Process took {finish-start} milliseconds to complete.")
        cserver.close()
    if ('excess' in result and result['excess'] is not None) or queried:
        if 'query' in result['excess'] or 'query' in query:
            cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cserver.connect((host,port))
            message = input("query > ")
            start = round(time.time() * 1000)
            message = message.lower()
            whitelist = set('abcdefghijklmnopqrstuvwxyz 1234567890')
            message = ''.join(filter(whitelist.__contains__, message))
            message = message.split(" ")
            if query:
                request = {'type':'command', 'profile':profile, 'message':lastmessage, 'excess': {'queryanswer': message, 'query': query['query']}}
            else:
                request = {'type':'command', 'profile':profile, 'message':lastmessage, 'excess': {'queryanswer': message, 'query': result['excess']['query']}}
            request = json.dumps(request)
            cserver.send(request.encode('utf-8'))
            result = cserver.recv(20000).decode('utf-8')
            result = json.loads(result)
            print(repr(result))
            print("\n\n" + result['result'] + "\n")
            finish = round(time.time() * 1000)
            if 'excess' in result and result['excess'] is not None:
                if 'query' in result['excess']:
                    queried = True
                    query = result['excess']
            else:
                queried = False
                query = None
            cserver.close()
    else:            
        queried = False
        query = None