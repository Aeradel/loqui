from Core.Command import executer as exe
from Core.Universal import functions as unifunc
from Core.Client import initialization as init
from Core.Data import pickling
from Skills.Memory import execute as memexe
from Skills.Walmart import settings
import asyncio
import json
import socket
import traceback

host = "192.168.1.25"
port = 42069
juststarted = True


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)




async def clientlisten():

    while True:
        try:
            global juststarted

            if juststarted == True:
                await init.initstart()
                await pickling.unpackpickles()
                await asyncio.sleep(2)
                await memexe.init()
                juststarted = False
                settings.settings = {
                    'walmartkey1':"6d498cd7e4ee5fc3d1a1f697c834a02c4646bd5bd2a3277da5f463745ff3397b",
                    'walmartkey2':"bed472b02ac613b52c079d4d1342bab9f6cc8d57be94b7911616ab84cf119a3a",
                    'walmartkey3':"6d5c823b6b90f3d894b91de6e3d595e6fbd04aca6d85607b5bf6187d5bed66ee",
                    'walmartkey4':"327785813a47ecb1a62d8134e9ad95ec26e799306ad461c6f20e2c29196b9a81",
                    'walmartkey5':"4885894ed0df353f0e2192f036a216aba5c8e35fcbe0c5ccf2316144143ce132",
                    'store_id': 3295
                }

            print(f"HOST {host} | Active and waiting for connection")
            
            await asyncio.sleep(1)
            await pickling.packpickles()

            client, clientAddr = server.accept()
            print(f"HOST {host} | Successful connection from CLIENT {clientAddr[0]}")
            request = client.recv(2450)
            await processrequest(request, client, clientAddr)
            
        except Exception as E:
            print(repr(E))
            traceback.print_exc()
            await asyncio.sleep(10)


async def processrequest(request, client, clientAddr):

        clientAddr = clientAddr[0]
        request = await unifunc.parserequest(request)

        if 'profile' in request:
            print(f"HOST {host} | Recieved {request['type']} request from CLIENT {clientAddr}-{request['profile']['name']}")
        else:
            print(f"HOST {host} | Recieved {request['type']} request from CLIENT {clientAddr}")

        if request['type'] == "command":
            result = await exe.exe(request['message'], request['profile'], request['excess'])
            result = await unifunc.makerequest(result['result'], 'command', result['text'], result['excess'])
            client.send(result)
            if 'profile' in request:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}-{request['profile']['name']}")
            else:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}")      

        if request['type'] == 'init':
            result, profile = await init.init(request['name'], [clientAddr, request['clientname']])
            jsonprofile = {'name': profile.name, 'key': profile.key, 'mainclient': profile.mainclient, 'clients': profile.clients, 'favorites':profile.favorites, 'details': profile.details}
            result = await unifunc.makerequest('profilequery', 'initprofile', result, jsonprofile)
            client.send(result)            

            if 'profile' in request:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}-{request['profile']['name']}")
            else:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}")    
                
asyncio.run(clientlisten())