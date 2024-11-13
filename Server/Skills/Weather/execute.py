from Skills.Weather import forecaster as forecast
from Skills.Weather import settings

from datetime import datetime
import zipcodes

keywords = []

async def todayweather(sentence, profile, excess, literal):

    day = await forecast.todayfull()

    return {'result': 'completed', 'text': day['message'], 'profile': profile, 'excess': {'weather': day}}

async def currentconditions(sentence, profile, excess, literal):

    day = await forecast.currentconditions()

    return {'result': 'completed', 'text': day['message'], 'profile': profile, 'excess': {'weather': day}}

async def sevendayweather(sentence, profile, excess, literal):

    week = await forecast.sevenday()

    return {'result': 'completed', 'text': week['message'], 'profile': profile, 'excess': {'weather': week}}

async def fivedayweather(sentence, profile, excess, literal):

    week = await forecast.fiveday()

    return {'result': 'completed', 'text': week['message'], 'profile': profile, 'excess': {'weather': week}}

async def precise(sentence, profile, excess, literal):
    if "monday" in sentence:
        day = "monday"
    elif "tuesday" in sentence:
        day = 'tuesday'
    elif 'wednesday' in sentence:
        day = 'wednesday'
    elif 'thursday' in sentence:
        day = 'thursday'
    elif 'friday' in sentence:
        day = 'friday'
    elif 'saturday' in sentence:
        day = 'saturday'
    elif 'sunday' in sentence:
        day = 'sunday'
    elif 'tomorrow' in sentence:
        today = datetime.now()
        today = today.strftime("%A").lower()
        if "monday" in today:
            day = "tuesday"
        elif "tuesday" in today:
            day = 'wednesday'
        elif 'wednesday' in today:
            day = 'thursday'
        elif 'thursday' in today:
            day = 'friday'
        elif 'friday' in today:
            day = 'saturday'
        elif 'saturday' in today:
            day = 'sunday'
        elif 'sunday' in today:
            day = 'monday'
    elif "current" in sentence or "currently" in sentence:
        day = 'current'
    elif "week" in sentence:
        day = "week"
    else:
        day = 'today'

    result = await forecast.grabdetail(sentence, day)
    return {'result': 'completed', 'text': result, 'profile': profile, 'excess': None}

async def preciseday(sentence, profile, excess, literal):
    if "monday" in sentence:
        day = "monday"
    elif "tuesday" in sentence:
        day = 'tuesday'
    elif 'wednesday' in sentence:
        day = 'wednesday'
    elif 'thursday' in sentence:
        day = 'thursday'
    elif 'friday' in sentence:
        day = 'friday'
    elif 'saturday' in sentence:
        day = 'saturday'
    elif 'sunday' in sentence:
        day = 'sunday'
    elif 'tomorrow' in sentence:
        today = datetime.now()
        today = today.strftime("%A").lower()
        if "monday" in today:
            day = "tuesday"
        elif "tuesday" in today:
            day = 'wednesday'
        elif 'wednesday' in today:
            day = 'thursday'
        elif 'thursday' in today:
            day = 'friday'
        elif 'friday' in today:
            day = 'saturday'
        elif 'saturday' in today:
            day = 'sunday'
        elif 'sunday' in today:
            day = 'monday'
    else:
        day = 'today'
    result = await forecast.dayfull(day)
    return {'result': 'completed', 'text': result['message'], 'profile': profile, 'excess': None}

async def weekconditions(sentence, profile, excess, literal):
    
    condition = ""

    if "rain" in sentence or "rainy" in sentence:
        condition = "rain"
    elif "clear" in sentence or "calm" in sentence:
        condition = "clear"
    elif "snow" in sentence or "ice" in sentence or "icy" in sentence or "snowy" in sentence:
        condition = 'snow'
    elif 'cloudy' in sentence or 'cloud' in sentence or 'clouds' in sentence or 'overcast' in sentence:
        condition = 'cloudy'
    else:
        condition = 'storm'

    result = await forecast.weekconditions(condition)

    return {'result': 'completed', 'text': result, 'profile': profile, 'excess': None}

async def alertcheck(sentence, profile, excess, literal):
    
    result = await forecast.alertcheck()

    return {'result': 'completed', 'text': result, 'profile': profile, 'excess': None}

async def settingchange(sentence, profile, excess, literal):

    if "unit" in sentence or "units" in sentence:
        if "metric" in sentence:
            settings.settings['unit'] = 'metric'
            phrase = "I have now updated your weather settings to forecast weather using the metric system."
        elif "imperial" in sentence or "us" in sentence or "usa" in sentence:
            settings.settings['unit'] = 'us'
            phrase = "I have now updated your weather settings to forecast weather using the imperial system."
        else:
            phrase = "I was not able to successfully change your weather unit settings. Please specify if you'd like to change your unit to metric or imperial."
    elif "zipcode" in sentence or ("zip" in sentence and "code" in sentence):
        zipcode = "".join(sentence)
        whitelist = set('1234567890')
        zipcode = ''.join(filter(whitelist.__contains__, zipcode))
        zipcoderes = zipcodes.is_real(zipcode)
        if zipcoderes:
            settings.settings['zipcodes'] = zipcode
            phrase = f"I have now changed your weather settings to forecast weather for {zipcode}."
        else:
            phrase = f"I was not able to validate {zipcode} as a zipcode."
    else:
        phrase = "I was not able to successfully change your weather settings. I can change your units of measurement or your zipcode." 

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

    
skills = {
    'todayweather': {
        'function': todayweather,
        'keys': ['what is the weather today', 'whats the weather today', 'what should i expect today', 'what is todays weather', 'what is it like today'],
        'require': ['weather', 'today'],
        'blacklist': ['remember', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "week", 'pressure', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions', 'severe', 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar'],
    },
    'currentconditions': {
        'function': currentconditions,
        'keys': ['what is the weather currently', 'whats the weather currently', 'what should i expect currently', 'what is the current weather', 'what is it like outside', 'what should i expect outside', 'what is happening outside', 'what is the weather'],
        'require': ['weather', 'current', 'currently'],
        'blacklist': ['remember', 'today', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "week", 'pressure', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions', 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar'],
    },
    'sevendayweather': {
        'function': sevendayweather,
        'keys': ['what is the weather this week', 'whats the weather this week', 'what is the weather like this week', 'whats is it like outside this week', 'what is this weeks weather'],
        'require': ['weather', 'week', 'seven'],
        'blacklist': ['remember', 'highs', 'lows', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "today", 'pressure', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions' , 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar'],
    },
    'fivedayweather': {
        'function': fivedayweather,
        'keys': ['what is the five day forecast', 'whats the five day forecast', 'what is the five day outlook', 'what is the five day forecast this week', 'what is this weeks five day forecast'],
        'require': ['forecast', 'week', 'five'],
        'blacklist': ['remember', 'highs', 'lows', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "today", 'pressure', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions' , 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar'],
    },
    'precise': {
        'function': precise,
        'keys': [],
        'require': ['current', 'currently', 'this week', 'week', 'today', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', "today", 'pressure', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'severe', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions' , 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar'],
        'blacklist': ['remember', 'forecast', 'weather', 'snow', 'icy', 'ice', 'times', 'how', 'many', 'clear'],
    },
    'preciseday':{
        'function': preciseday,
        'keys':[],
        'require': ['weather'],
        'blacklist': ['remember', 'today', 'week', 'pressure', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'severe', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions' , 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar', 'clear']
    },
    'weekconditions':{
        'function': weekconditions,
        'keys':[],
        'require':['storm', 'stormy', 'stormy weather', 'severe weather', 'rain', 'rainy weather', 'rainy', 'clear', 'clear weather', 'calm', 'calm skies', 'clear skies', 'snow', 'snowy', 'icy', 'ice', 'cloudy', 'clouds', 'cloud', 'cloudy skies', 'weather', 'week'],
        'blacklist': ['remember', 'severe'],
    },
    'alertcheck':{
        'function': alertcheck,
        'keys':["are there any alerts", "are there any weather alerts", "what are the active weather alerts", "what are the active alerts", "are there any active alerts"],
        'require': ['alert', 'alerts', 'weather', 'active'],
        'blacklist': ['remember'],
    },
    "changesettings":{
        'function': settingchange,
        'keys':['change my unit to imperial', 'change my unit to us', 'change my unit to usa', 'change my unit to metric', 'change my weather unit to metric',
                'change my weather unit to imperial', 'change my weather unit to us', 'change my weather unit to usa', 'change my weather unit to metric',
                'change my zipcode to', 'change my weather zipcode to', 'change my zip code to', 'change my weather zip code to'],
        'require': ['zipcode', 'zip', 'code', 'metric', 'imperial', 'unit', 'usa', 'us', 'change'],
        'blacklist':[]
    }
}


details = ['pressure', 'highs', 'lows', 'rain', 'dew', 'feels like', 'feelslike', 'high', 'low', 'temperature', 'temp', 'cloud', 'cloud cover', 'uv index', 'uvi', 'sunrise' ,'sunset', 'sunrise time', 'sunset time', 'wind speed', 'wind gust', 'severe risk', 'severe chance', 'risk chance', 'conditions' , 'moon', 'moon phase', 'moonphase', 'lunar phase', 'lunar']
days = ['currently', 'current', 'today', 'week', 'this week', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
secondarydetails = ['storm', 'stormy', 'stormy weather', 'severe weather', 'rain', 'rainy weather', 'rainy', 'clear', 'clear weather', 'calm', 'calm skies', 'clear skies', 'snow', 'snowy', 'icy', 'ice', 'cloudy', 'clouds', 'cloud', 'cloudy skies']

for detail in secondarydetails:
    skills['weekconditions']['keys'].append(f"when can i expect {detail}")
    skills['weekconditions']['keys'].append(f"when can i expect {detail} this week")
    skills['weekconditions']['keys'].append(f"when will it {detail} this week")
    skills['weekconditions']['keys'].append(f"when will it {detail}")
    skills['weekconditions']['keys'].append(f"how many times will it {detail} this week")
    skills['weekconditions']['keys'].append(f"how many times will it {detail}")
for word in details:
    for day in days:
        if day != "week" and day != "this week": 
            skills['precise']['keys'].append(f"what is the {word} for {day}")
            skills['precise']['keys'].append(f"whats the {word} for {day}")
            skills['precise']['keys'].append(f"what is {word} for {day}")
            skills['precise']['keys'].append(f"what is the {word} on {day}")
            skills['precise']['keys'].append(f"whats the {word} on {day}")
            skills['precise']['keys'].append(f"whats {day}s {word}")
            skills['precise']['keys'].append(f"what is {day}s {word}")
        else:
            skills['precise']['keys'].append(f"what are the {word} for {day}")
            skills['precise']['keys'].append(f"whats the {word} for {day}")
            skills['precise']['keys'].append(f"what are {word} for {day}")
            skills['precise']['keys'].append(f"what are the {word} {day}")
            skills['precise']['keys'].append(f"whats the {word} {day}")
            skills['precise']['keys'].append(f"whats is {word} like {day} ")
            skills['precise']['keys'].append(f"what are {day}s {word}")
for day in days:
    if day != "today" and day != "this week" and day != "week" and day != "current" and day != "currently":
        skills['preciseday']['keys'].append(f"what is the weather on {day}")
        skills['preciseday']['keys'].append(f"whats the weather on {day}")
        skills['preciseday']['keys'].append(f"what is the weather like on {day}")
        skills['preciseday']['keys'].append(f"whats {day}s weather ")
        skills['preciseday']['keys'].append(f"what is {day}s weather")
        skills['preciseday']['keys'].append(f"what is the forecast on {day}")
        skills['preciseday']['keys'].append(f"whats the forecast on {day}")
        skills['preciseday']['keys'].append(f"what is the forecast like on {day}")
        skills['preciseday']['keys'].append(f"whats {day}s forecast ")
        skills['preciseday']['keys'].append(f"what is {day}s forecast")

for function in skills:
    for key in skills[function]['keys']:
        keywords.append(key)