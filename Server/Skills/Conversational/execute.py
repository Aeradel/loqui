from typing import final
from Core.Universal import functions as unifunc
from Core.Data import permanent as perm

from datetime import datetime
import asyncio
import requests
import bs4

keywords = []


async def hello(sentence, profile, excess, literal):
    greetings = [f"Hi, {profile['name']}.",
                 f"Hello, {profile['name']}.",
                 f"Howdy, {profile['name']}.",
                 f"Greetings, {profile['name']}"]

    now = datetime.now()
    currentHour = int(now.strftime("%I"))

    if currentHour >= 3 and currentHour < 12:
        greetings.append(f"Good morning, {profile['name']}.")
    elif currentHour >= 13 and currentHour < 18:
        greetings.append(f"Good afternoon, {profile['name']}.")
    elif currentHour != 12:
        greetings.append(f"Good evening, {profile['name']}.") 

    greeting = await unifunc.choosePhrase(greetings)

    return {'result': 'completed', 'text': greeting, 'profile': profile, 'excess': None}

async def time(sentence, profile, excess, literal):
    now = datetime.now()
    currentTime = now.strftime("%I:%M %p")

    phrasing = [f"The time is now {currentTime}.",
                f"It's currently {currentTime}.",
                f"It is now {currentTime}.",
                f"{currentTime}",
                f"{currentTime} is the current time."]

    finalphrase = await unifunc.choosePhrase(phrasing)

    return {'result': 'completed', 'text': finalphrase, 'profile': profile, 'excess': None}

async def whatismyname(sentence, profile, excess, literal):
    phrasing = await unifunc.choosePhrase([f"Your name is {profile['name']}.",
                                           f"I have your name saved as {profile['name']}",
                                           f"I recognize you as {profile['name']}.",
                                           f"I'm guessing your name is {profile['name']}."])

    return {'result': 'completed', 'text': phrasing, 'profile': profile, 'excess': None}

async def howareyou(sentence, profile, excess, literal):
    if excess is not None and "queryanswered" in excess:
        bad = ["bad", "not good", "terrible", "awful", 'worried', 'stressed']
        tone = 'good'
        for word in bad:
            if word in excess['answer']:
                tone = 'bad'

        if tone  == 'good':      
            phrasing = [f"Good to hear, {profile['name']}.",
                        f"Glad to hear that, {profile['name']}.",
                        f"That's good to hear, {profile['name']}."]
            if 'weather' in excess and excess['weather']['context'] == 'clear':
                phrasing.append("Glad to hear it. I bet the clear skies are helping.")
                phrasing.append("Good to hear. The nice weather today should help keep your day good.")
        elif tone == "bad":
            phrasing = [f"Sorry to hear, {profile['name']}.",
                        f"Sorry to hear that, {profile['name']}.",
                        f"I'm sorry to hear that, {profile['name']}."]
            if 'weather' in excess and excess['weather']['context'] == 'bad':
                phrasing.append("I'm sorry to hear that. The weather probably isn't helping either.")
                phrasing.append("Sorry to hear that. Hopefully the weather will improve soon and help better your day.") 

        finalphrase = await unifunc.choosePhrase(phrasing)

        return {'result': 'completed', 'text': finalphrase, 'profile': profile, 'excess': None}


    else:
        phrasing = [f"I am doing great, {profile['name']}. How are you doing?",
                    f"I am doing good. Thanks for asking, {profile['name']}. How are you doing?",
                    f"I'm doing good, {profile['name']}. How are you?",
                    f"Doing great. Thanks for asking. How are you, {profile['name']}?"]

        finalphrase = await unifunc.choosePhrase(phrasing)

        return {'result': 'completed', 'text': finalphrase, 'profile': profile, 'excess': {'queried': 'true', 'query': 'howareyou', 'possiblekeys': None}}

async def covidquery(sentence, profile, excess, literal):

    url = "https://www.worldometers.info/coronavirus/"
    html_data = await get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")

    if "covid" not in perm.data:
        perm.data['covid'] = {}

    for block in info_div:
        text = block.find("h1", class_=None).get_text()
        count = block.find("span",  class_=None).get_text()
        if "Cases" in text or "cases" in text:
            perm.data['covid']['currentcount'] = await numberconvert(count)
        elif 'Deaths' in text or 'deaths' in text:
            perm.data['covid']['currentdeath'] = await numberconvert(count)
        elif 'Recovered' in text or 'recovered' in text:
            perm.data['covid']['currentrecovered'] = await numberconvert(count)

        
    if "deaths" in sentence or 'death' in sentence or 'died' in sentence:
        if not "pastdeath" in perm.data['covid']:
            phrase = await unifunc.choosePhrase([f"There have been {perm.data['covid']['currentdeath']} deaths due to COVID.", 
                                                        f"There is have been an estimated {perm.data['covid']['currentdeath']} deaths due to COVID.", 
                                                        f"COVID has taken an estimated {perm.data['covid']['currentdeath']} lives."])            
            perm.data['covid']['pastdeath'] = perm.data['covid']['currentdeath']
        else:
            if perm.data['covid']['currentdeath'] - perm.data['covid']['pastdeath'] > 0:
                phrase = await unifunc.choosePhrase([f"There have been {perm.data['covid']['currentdeath']} deaths due to COVID, which is an increase of {perm.data['covid']['currentdeath'] - perm.data['covid']['pastdeath']} since the last time you queried.", 
                                                            f"There is have been an estimated {perm.data['covid']['currentdeath']} deaths due to COVID, an increase of {perm.data['covid']['currentdeath'] - perm.data['covid']['pastdeath']} since the last query.", 
                                                            f"COVID has taken an estimated {perm.data['covid']['currentdeath']} lives, an increase of {perm.data['covid']['currentdeath'] - perm.data['covid']['pastdeath']} since the last query."])
            else:
                phrase = await unifunc.choosePhrase([f"There have been {perm.data['covid']['currentdeath']} deaths due to COVID. There has not been an increase since the last query.", 
                                                            f"There is have been an estimated {perm.data['covid']['currentdeath']} deaths due to COVID. There has been no increase since the last query.", 
                                                            f"COVID has taken an estimated {perm.data['covid']['currentdeath']} lives. There hasn't been an increase since the previous query."])            
            perm.data['covid']['pastdeath'] = perm.data['covid']['currentdeath']
    elif "recovered" in sentence or "recovery" in sentence or "recoveries" in sentence or "rate" in sentence:
        phrase = await unifunc.choosePhrase([f"There has been {perm.data['covid']['currentrecovered']} cases of recovered patients. The current recovery rate is estimated to be {round(perm.data['covid']['currentrecovered']/perm.data['covid']['currentcount'], 4)*100}%.",
                                             f"There have been {perm.data['covid']['currentrecovered']} recoveries. The recovery rate is estimated around {round(perm.data['covid']['currentrecovered']/perm.data['covid']['currentcount'], 4)*100}%.",
                                             f"There is an estimated {perm.data['covid']['currentrecovered']} recoveries worldwide, bringing the estimated recovery rate to {round(perm.data['covid']['currentrecovered']/perm.data['covid']['currentcount'], 4)*100}%."])        
        perm.data['covid']['pastrecovered'] = perm.data['covid']['currentrecovered'] 
    else:
        if not "pastcount" in perm.data['covid']:
            phrase = await unifunc.choosePhrase([f"There have been {perm.data['covid']['currentcount']} cases of COVID worldwide. There have been an estimated {perm.data['covid']['currentdeath']} deaths and {perm.data['covid']['currentrecovered']} recoveries.",
                                                 f"There is an estimated {perm.data['covid']['currentcount']} cases of COVID worldwide. There have been {perm.data['covid']['currentdeath']} deaths and {perm.data['covid']['currentrecovered']} recoveries.",
                                                 f"There is currently an estimated {perm.data['covid']['currentcount']} total cases of COVID worldwide. {perm.data['covid']['currentdeath']} deaths and {perm.data['covid']['currentrecovered']} recoveries."])
            perm.data['covid']['pastcount'] = perm.data['covid']['currentcount']
            perm.data['covid']['pastdeath'] = perm.data['covid']['currentdeath']
            perm.data['covid']['pastrecovered'] = perm.data['covid']['currentrecovered'] 
        else:
            if perm.data['covid']['currentcount'] - perm.data['covid']['pastcount'] > 0:
                phrase = await unifunc.choosePhrase([f"There have been {perm.data['covid']['currentcount']} cases of COVID worldwide, an increase of {perm.data['covid']['currentcount'] - perm.data['covid']['pastcount']} cases since the last query.",
                                                    f"There is an estimated {perm.data['covid']['currentcount']} cases of COVID worldwide, an increase of {perm.data['covid']['currentcount'] - perm.data['covid']['pastcount']} cases since the last time queried.",
                                                    f"There is currently an estimated {perm.data['covid']['currentcount']} total cases of COVID worldwide. There has been an increase of {perm.data['covid']['currentcount'] - perm.data['covid']['pastcount']} cases since last queried."])
            else:
                phrase = await unifunc.choosePhrase([f"There have been {perm.data['covid']['currentcount']} cases of COVID worldwide. There has not been an increase since the previous query.",
                                                    f"There is an estimated {perm.data['covid']['currentcount']} cases of COVID worldwide. There has been no increase in cases since the last query.",
                                                    f"There is currently an estimated {perm.data['covid']['currentcount']} total cases of COVID worldwide. There hasn't been an increase in cases since the previous query."])
                              
            perm.data['covid']['pastcount'] = perm.data['covid']['currentcount']
     

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def get_html_data(url):
	data = requests.get(url)
	return data

async def numberconvert(number):
	whitelist = set('1234567890')
	number = ''.join(filter(whitelist.__contains__, number))
	return int(number)  

skills = {

    'hello': {
        'function': hello,
        'keys': ['Hi', 'Hello', 'Howdy', 'Sup', 'Good morning', 'Good afternoon', 'Good evening', 'Hey', 'Greetings'],
        'require': ['Hi', 'Hello', 'Howdy', 'Sup', 'morning', 'afternoon', 'evening', 'Hey', 'Greetings'],
        'blacklist': ['when', 'name', 'who', 'know', 'remember'],
    },
    'time': {
        'function': time,
        'keys': ['what time is it', 'whats the time', 'what time is it now', 'what is the time', 'can you tell me the time', 'what is the current time',
                'could you tell me the time', 'may i know the time', 'could i have the time'],
        'require': ['time'],
        'blacklist': ['open', 'close', 'when', 'sun', 'sunset', 'sunrise', 'set', 'rise', 'remember'],
    },
    'whatismyname': {
        'function': whatismyname,
        'keys': ['what is my name', "who am i", "do you know who i am", "whats my name", "who is logged in", "who is using this", "do you know me"],
        'require': ['name'],
        'blacklist': ['open', 'close', 'when', 'sun', 'sunset', 'sunrise', 'set', 'rise', 'remember'],
    },
    'howareyou': {
        'function': howareyou,
        'keys': ['how are you', 'how have you been', 'hows it going', 'hows everything', 'whats up'],
        'require': ["how"],
        'blacklist': ['when', 'sunset', 'sunrise', 'set', 'rise', 'remember'],
    },
    'covidquery':{
        'function': covidquery,
        'keys':['how many covid cases has there been', 'how many covid cases', 'how many covid deaths', 'how many covid recoveries', 'how many total covid cases', 'total covid cases', 'total covid deaths', 'total covid recoveries', 'what are the current covid stats', 'what are the current covid statistics', 'tell me about covid'],
        'require':['covid', 'cases', 'deaths', 'recoveries', 'worldwide'],
        'blacklist':[]
    }
}

for function in skills:
    for key in skills[function]['keys']:
        keywords.append(key)