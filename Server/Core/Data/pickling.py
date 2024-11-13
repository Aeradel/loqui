from Core.Client import profiles
from Core.Data import permanent as perm
from Core.Data import temporary as temp
from Core.Universal import variables as univars
from Skills.Client import settings as clientsettings
from Skills.Conversational import settings as conversettings
from Skills.Google import settings as googlesettings
from Skills.Memory import settings as memorysettings
from Skills.Walmart import settings as walmartsettings
from Skills.Weather import settings as weathersettings
from Skills.Automation import settings as autosettings

import pickle
import os 

async def packpickles():

    file = open('Server/Pickles/profiles.txt', 'ab')
    file.truncate(0)
    information = profiles.savedprofiles
    pickle.dump(information, file)
    file.close()

    file = open('Server/Pickles/settings.txt', 'ab')
    file.truncate(0)
    information = [clientsettings.settings, conversettings.settings, googlesettings.settings, 
                   memorysettings.settings, walmartsettings.settings, weathersettings.settings,
                   autosettings.settings]
    pickle.dump(information, file)
    file.close()

    file = open('Server/Pickles/data.txt', 'ab')
    file.truncate(0)
    information = [perm.data, temp.data, univars.vars]
    pickle.dump(information, file)
    file.close()

async def unpackpickles():

    pathsize = os.path.getsize('Server/Pickles/profiles.txt')
    if pathsize > 0:
        file = open('Server/Pickles/profiles.txt', 'rb')
        information = pickle.load(file)
        profiles.savedprofiles = information
        file.close()

    pathsize = os.path.getsize('Server/Pickles/settings.txt')
    if pathsize > 0:
        file = open('Server/Pickles/settings.txt', 'rb')
        information = pickle.load(file)
        clientsettings.settings = information[0]
        conversettings.settings = information[1]
        googlesettings.settings = information[2]
        memorysettings.settings = information[3]
        walmartsettings.settings = information[4]
        weathersettings.settings = information[5]
        autosettings.settings = information[6]
        file.close()

    pathsize = os.path.getsize('Server/Pickles/data.txt')
    if pathsize > 0:
        file = open('Server/Pickles/data.txt', 'rb')
        information = pickle.load(file)
        perm.data = information[0]
        temp.data = information[1]
        univars.vars = information[2]
        file.close()

