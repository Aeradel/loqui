from Core.Universal import functions as unifuncs
from Skills.Weather import settings

import requests
from datetime import datetime



cloudy = ['cloudy', 'partly-cloudy-day', 'partly-cloudy-night']
clear = ['clear', 'clear-day', 'clear-night']
rain = ['rain', 'showers-day', 'showers', 'showers-night']
snow = ['snow', 'snow-showers-day', 'snow-showers-night']
storm = ['thunder-rain', 'thunder-showers-day', 'thunder-showers-night']
misc = ['fog', 'wind']

async def alertcheck():
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"
    pulledData = requests.get(weatherData).json()
    alert = pulledData['alerts']
    alertinformation = ""
    if len(alert) > 0:
        if len(alert) == 1:
            alert = alert[0]
            alerttime = alert['ends']
            alerttime = alerttime[11:]
            alerttime = alerttime[:7]
            alerttime = datetime.strptime(alerttime, "%H:%M:%S")
            alerttime = alerttime.strftime("%I:%M %p")
            alertinformation += await unifuncs.choosePhrase([f"There is currently a {alert['event']} lasting until {alerttime}.",
                                                             f"There is a {alert['event']} lasting until {alerttime}.",
                                                             f"There is a {alert['event']} issued until {alerttime}"])
        else:
            alertinformation += await unifuncs.choosePhrase([f"There are currently {len(alerts)} active alerts.",
                                                             f"I have found {len(alerts)} issued alerts.",
                                                             f"There are {len(alerts)} alerts active."])
            for alerts in alert:
                alerttime = alerts['ends']
                alerttime = alerttime[11:]
                alerttime = alerttime[:7]
                alerttime = datetime.strptime(alerttime, "%H:%M:%S")
                alerttime = alerttime.strftime("%I:%M %p")
                additionalphrase += await unifuncs.choosePhrase([f"{alerts['event']} lasting until {alerttime}.",
                                                                 f"{alerts['event']} expiring at {alerttime}.",
                                                                 f"{alerts['event']} issued until {alerttime}."])
                if len(alert) - alert.index(alerts) == 1:
                    additionalphrase = await unifuncs.choosePhrase(["And, ", "Lastly, ", "And the last alert is, "]) + additionalphrase
                
                alertinformation += " " + additionalphrase
    else:
        alertinformation = "There are no active alerts."

    return alertinformation

async def todayfull():
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"    
    pulledData = requests.get(weatherData).json()
    pulledday = pulledData['days'][0]
    notes = {}
    unit = 'imp'

    if settings.settings['unit'] == 'metric':
        reftemp = (pulledday['feelslike'] * 9/5) + 32
        dewpoint = (pulledday['dew'] * 9/5) + 32
        unit = 'metric'
    else:
        reftemp = pulledday['feelslike']
        dewpoint = pulledday['dew']

    #pressure check
    if pulledday['pressure'] > 1018:
        notes['clouds'] = "high"
    elif pulledday['pressure'] <= 1018 and pulledday['pressure'] > 1013:
        notes['clouds'] = 'moderate'
    else:
        notes['pressure'] = 'low'

    # dew point check
    if dewpoint > 65:
        notes['dew'] = 'high'
    elif dewpoint > 55 and dewpoint <= 65:
        notes['dew'] = 'moderate'
    else:
        notes['dew'] = 'low'
    
    #feels like check
    if reftemp >= 100:
        notes['temp'] = ['very hot', 'scorching', 'blazing']
        if notes['dew'] == 'high':
            notes['temp'].append('humid')
            notes['temp'].append('muggy')
            notes['temp'].append('sticky')
        notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
    elif reftemp >= 75 and reftemp < 100:
        notes['temp'] = ['hot', 'summery', 'spicy']
        if notes['dew'] == 'high':
            notes['temp'].append('humid')
            notes['temp'].append('muggy')
            notes['temp'].append('sticky')
        notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
    elif reftemp >= 55 and reftemp < 75:
        notes['temp'] = await unifuncs.choosePhrase(['moderate', 'warm', 'cool'])
    elif reftemp >= 30 and reftemp < 55:
        notes['temp'] = await unifuncs.choosePhrase(['cold', 'chilly', 'crisp'])
    else:
        notes['temp'] = await unifuncs.choosePhrase(['very cold', 'wintry', 'frosty', 'freezing cold'])

    # conditions check
    if pulledday['icon'] in rain:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a rainy day with ', "I'm forecasting the occasional shower today with ", "Prepare for a chance of light rain with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect the occasional shower throughout the night with ', "I'm forecasting a chance of light rain tonight with ", 'Anticipate light rain throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect the occasional shower throughout the day with ', "I'm forecasting a chance of light rain today with ", 'Anticipate light rain throughout the day with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a rainy day with ', "I'm forecasting a chance of rain today with ", "Prepare for rain today with "])
    elif pulledday['icon'] in cloudy:
        notes['context'] = 'good'
        if 'partly' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a partly cloudy day with ', "I'm forecasting a partly cloudy day with ", "Prepare for clouds throughout the day with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect it to be partly cloudy throughout the night with ', "I'm forecasting a partly cloudy night with ", 'Anticipate clouds throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect it to be partly cloudy throughout the day with ', "I'm forecasting a partly cloudy day with ", 'Anticipate clouds throughout the day with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a cloudy day with ', "I'm forecasting a cloudy day with ", "Prepare for a cloudy day with "])
    elif pulledday['icon'] in clear:
        notes['context'] = 'good'
        if 'night' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect it to be clear skies throughout the night with ', "I'm forecasting a clear night with ", 'Anticipate clear skies throughout the night with '])
        elif 'day' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect it to be clear skies throughout the day with ', "I'm forecasting a day free of clouds with ", 'Anticipate no clouds throughout the day with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect clear skies today with ', "I'm forecasting clear skies today with ", "Prepare for clear skies today with "])
    elif pulledday['icon'] in storm:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a stormy day with ', "I'm forecasting the occasional storm today with ", "Prepare for a chance of a small storm with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect the occasional storm throughout the night with ', "I'm forecasting a chance of small storm tonight with ", 'Anticipate a small storm throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect the occasional storm throughout the day with ', "I'm forecasting a chance of a small storm today with ", 'Anticipate a small storm throughout the day with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a stormy day with ', "I'm forecasting a chance of a storm today with ", "Prepare for a storm today with "])
    elif pulledday['icon'] in snow:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a slightly snowy day with ', "I'm forecasting the occasional snow shower today with ", "Prepare for a chance of snow showers with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect the occasional snow throughout the night with ', "I'm forecasting a chance of snow showers tonight with ", 'Anticipate a small amount of snow throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase(['Expect the occasional snow throughout the day with ', "I'm forecasting a chance of a snow showers today with ", 'Anticipate a small amount of snow throughout the day with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a snowy day with ', "I'm forecasting a chance of snow today with ", "Prepare for snow today with "])
    elif pulledday['icon'] in misc:
        notes['context'] = 'bad'
        if 'fog' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a foggy day with ', "I'm forecasting fog today with ", "Prepare for a chance of fog with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a windy day with ', "I'm forecasting a fair amount of wind today with ", "Prepare for windy day with "])

    notes['followup'] = await unifuncs.choosePhrase([f"{notes['temp']} temperatures around {round(pulledday['feelslike'])} degrees.",
                                              f"temperatures around {round(pulledday['feelslike'])} degrees making it {notes['temp']}."])
    if notes['dew'] == "moderate":
        notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be humid outside.",
                                                    " I anticipate it being humid outside.",
                                                    " I'd expect it to be humid outside today."])
    if notes['dew'] == "high":
        notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be very humid outside.",
                                                    " I anticipate it being very humid outside.",
                                                    " I'd expect it to be very humid outside today."])
    
    alerts = await alertcheck()
    if alerts != "There are no active alerts.":
        notes['followup'] += " " + alerts

    if unit == "metric":
        notes['followup'] += await unifuncs.choosePhrase([f" The barometric pressure is {round(pulledday['pressure'])}. The cloud cover is at {round(pulledday['cloudcover'])}%. Lastly, the windspeed is {round(pulledday['windspeed'])} kilometers per hour.",
                                                    f" The barometric pressure is {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are {round(pulledday['windspeed'])} kilometers per hour.",
                                                    f" Barometric pressure is at {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are at {round(pulledday['windspeed'])} kilometers per hour."])
    else:
        notes['followup'] += await unifuncs.choosePhrase([f" The barometric pressure is {round(pulledday['pressure'])}. The cloud cover is at {round(pulledday['cloudcover'])}%. Lastly, the windspeed is {round(pulledday['windspeed'])} miles per hour.",
                                                    f" The barometric pressure is {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are {round(pulledday['windspeed'])} miles per hour.",
                                                    f" Barometric pressure is at {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are at {round(pulledday['windspeed'])} miles per hour."])


    notes['final'] = notes['cond'] + notes['followup']
    day = {'data': pulledday, 'notes': notes, 'context': notes['context'], 'message':notes['final']}

    return day

async def currentconditions():
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"    
    pulledData = requests.get(weatherData).json()
    pulledday = pulledData['currentConditions']
    notes = {}
    unit = 'imp'

    if settings.settings['unit'] == 'metric':
        reftemp = (pulledday['feelslike'] * 9/5) + 32
        dewpoint = (pulledday['dew'] * 9/5) + 32
        unit = 'metric'
    else:
        reftemp = pulledday['feelslike']
        dewpoint = pulledday['dew']

    #pressure check
    if pulledday['pressure'] > 1018:
        notes['clouds'] = "high"
    elif pulledday['pressure'] <= 1018 and pulledday['pressure'] > 1013:
        notes['clouds'] = 'moderate'
    else:
        notes['pressure'] = 'low'

    # dew point check
    if dewpoint > 65:
        notes['dew'] = 'high'
    elif dewpoint > 55 and dewpoint <= 65:
        notes['dew'] = 'moderate'
    else:
        notes['dew'] = 'low'
    
    #feels like check
    if reftemp >= 100:
        notes['temp'] = ['very hot', 'scorching', 'blazing']
        if notes['dew'] == 'high':
            notes['temp'].append('humid')
            notes['temp'].append('muggy')
            notes['temp'].append('sticky')
        notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
    elif reftemp >= 75 and reftemp < 100:
        notes['temp'] = ['hot', 'summery', 'spicy']
        if notes['dew'] == 'high':
            notes['temp'].append('humid')
            notes['temp'].append('muggy')
            notes['temp'].append('sticky')
        notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
    elif reftemp >= 55 and reftemp < 75:
        notes['temp'] = await unifuncs.choosePhrase(['moderate', 'warm', 'cool'])
    elif reftemp >= 30 and reftemp < 55:
        notes['temp'] = await unifuncs.choosePhrase(['cold', 'chilly', 'crisp'])
    else:
        notes['temp'] = await unifuncs.choosePhrase(['very cold', 'wintry', 'frosty', 'freezing cold'])

    # conditions check
    if pulledday['icon'] in rain:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(["It's currently lightly raining outside with " , "I'm forecasting occasional shower currently with ", "Prepare for a chance of light rain with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect rain with ', "I'm currently forecasting a chance of rain with ", "Prepare for rain with "])
    elif pulledday['icon'] in cloudy:
        notes['context'] = 'good'
        if 'partly' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect partly cloudy skies with ', "I'm forecasting partly cloudy skies currently with ", "Expect clouds currently with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a cloudy skies with ', "I'm forecasting cloudy skies currently with ", "Prepare for nothing but clouds currently with "])
    elif pulledday['icon'] in clear:
        notes['context'] = 'good'
        notes['cond'] = await unifuncs.choosePhrase(["The skies are currently clear with ", "The clouds are currently hiding, giving way to clear skies with ", 'Anticipate clear skies outside with '])
    elif pulledday['icon'] in storm:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(["I'd expect a storm within the next hour or so with ", "I'm currently forecasting the occasional storm with ", "Prepare for a small storm with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase(['Expect storms currently with ', "I'm forecasting a high chance of storms currently with ", "Prepare for storms currently with "])
    elif pulledday['icon'] in snow:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(['Expect a chance of flurries currently with ', "I'm forecasting the occasional flurry currently with ", "Prepare for a chance of flurries with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase([f"Expect more than {round(pulledday['snowdepth'])} inches snow outside with  ", "I'm forecasting a chance of snow currently with ", f"Prepare for {round(pulledday['snowdepth'])} inches of snow outside with "])
    elif pulledday['icon'] in misc:
        notes['context'] = 'bad'
        if 'fog' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase(["I'd expect fog outside currently with ", "I'm currently forecasting a high chance fog with ", "Prepare for a high chance of fog with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase(["I'd expect ferocious winds outside currently with ", "I'm currently forecasting high wind speeds with ", "Prepare for high wind speeds with "])

    notes['followup'] = await unifuncs.choosePhrase([f"{notes['temp']} temperatures around {round(pulledday['feelslike'])} degrees.",
                                              f"temperatures around {round(pulledday['feelslike'])} degrees making it {notes['temp']}."])
    if notes['dew'] == "moderate":
        notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be humid outside.",
                                                    " I anticipate it being humid outside.",
                                                    " I'd expect it to be humid outside."])
    if notes['dew'] == "high":
        notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be very humid outside.",
                                                    " I anticipate it being very humid outside.",
                                                    " I'd expect it to be very humid outside."])

    alerts = await alertcheck()
    if alerts != "There are no active alerts.":
        notes['followup'] += " " + alerts 

    if unit == "metric":
        notes['followup'] += await unifuncs.choosePhrase([f" The barometric pressure is {round(pulledday['pressure'])}. The cloud cover is at {round(pulledday['cloudcover'])}%. Lastly, the windspeed is {round(pulledday['windspeed'])} kilometers per hour.",
                                                    f" The barometric pressure is {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are {round(pulledday['windspeed'])} kilometers per hour.",
                                                    f" Barometric pressure is at {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are at {round(pulledday['windspeed'])} kilometers per hour."])
    else:
        notes['followup'] += await unifuncs.choosePhrase([f" The barometric pressure is {round(pulledday['pressure'])}. The cloud cover is at {round(pulledday['cloudcover'])}%. Lastly, the windspeed is {round(pulledday['windspeed'])} miles per hour.",
                                                    f" The barometric pressure is {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are {round(pulledday['windspeed'])} miles per hour.",
                                                    f" Barometric pressure is at {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are at {round(pulledday['windspeed'])} miles per hour."])

    notes['final'] = notes['cond'] + notes['followup']
    day = {'data': pulledday, 'notes': notes, 'context': notes['context'], 'message':notes['final']}

    return day

async def dayfull(day):
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"
    pulledData = requests.get(weatherData).json()
    pulledData = pulledData['days']
    pulledWeek = [pulledData[0], pulledData[1], pulledData[2], pulledData[3], pulledData[4], pulledData[5], pulledData[6]]
    newweek = []
    for pulledday in pulledWeek:
        newday = pulledday
        newday['day'] = datetime.strptime(pulledday['datetime'], "%Y-%m-%d")
        newday['day'] = newday['day'].strftime("%A")
        newweek.append(newday)
    for newday in newweek:
        if day == newday['day'].lower():
            day = newday

    pulledday = day
    notes = {'day': day['day']}
    unit = 'imp'

    if settings.settings['unit'] == 'metric':
        reftemp = (pulledday['feelslike'] * 9/5) + 32
        dewpoint = (pulledday['dew'] * 9/5) + 32
        unit = 'metric'
    else:
        reftemp = pulledday['feelslike']
        dewpoint = pulledday['dew']

    #pressure check
    if pulledday['pressure'] > 1018:
        notes['clouds'] = "high"
    elif pulledday['pressure'] <= 1018 and pulledday['pressure'] > 1013:
        notes['clouds'] = 'moderate'
    else:
        notes['pressure'] = 'low'

    # dew point check
    if dewpoint > 65:
        notes['dew'] = 'high'
    elif dewpoint > 55 and dewpoint <= 65:
        notes['dew'] = 'moderate'
    else:
        notes['dew'] = 'low'
    
    #feels like check
    if reftemp >= 100:
        notes['temp'] = ['very hot', 'scorching', 'blazing']
        if notes['dew'] == 'high':
            notes['temp'].append('humid')
            notes['temp'].append('muggy')
            notes['temp'].append('sticky')
        notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
    elif reftemp >= 75 and reftemp < 100:
        notes['temp'] = ['hot', 'summery', 'spicy']
        if notes['dew'] == 'high':
            notes['temp'].append('humid')
            notes['temp'].append('muggy')
            notes['temp'].append('sticky')
        notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
    elif reftemp >= 55 and reftemp < 75:
        notes['temp'] = await unifuncs.choosePhrase(['moderate', 'warm', 'cool'])
    elif reftemp >= 30 and reftemp < 55:
        notes['temp'] = await unifuncs.choosePhrase(['cold', 'chilly', 'crisp'])
    else:
        notes['temp'] = await unifuncs.choosePhrase(['very cold', 'wintry', 'frosty', 'freezing cold'])

    # conditions check
    if pulledday['icon'] in rain:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'On {notes["day"]} expect a rainy day with ', f"For {notes['day']}, I'm forecasting the occasional shower with ", f"Prepare for a chance of light rain on {notes['day']} with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional shower throughout {notes["day"]} night with ', f"I'm forecasting a chance of light rain {notes['day']} night with ", f'On {notes["day"]}, anticipate light rain throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional shower throughout {notes["day"]} with ', f"I'm forecasting a chance of light rain {notes['day']} with ", f'On {notes["day"]}, anticipate light rain throughout the day with '])            
        else:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a rainy {notes["day"]} with ', f"I'm forecasting a chance of rain on {notes['day']} with ", f"Prepare for rain on {notes['day']} with "])
    elif pulledday['icon'] in cloudy:
        notes['context'] = 'good'
        if 'partly' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a partly cloudy day on {notes["day"]} with ', f"I'm forecasting a partly cloudy {notes['day']} with ", f"Prepare for clouds throughout the day on {notes['day']} with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be partly cloudy throughout the night on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a partly cloudy night with ", f"On {notes['day']}, anticipate clouds throughout the night with "])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be partly cloudy throughout the day on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a partly cloudy day with ", f"On {notes['day']}, anticipate clouds throughout the day with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a cloudy {notes["day"]} with ', f"I'm forecasting a cloudy {notes['day']} with ", f"Prepare for a cloudy {notes['day']} with "])
    elif pulledday['icon'] in clear:
        notes['context'] = 'good'
        if 'night' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be clear skies throughout the night on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a clear night with ", f'On {notes["day"]}, Anticipate clear skies throughout the night with '])
        elif 'day' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be clear skies throughout the day on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a clear day with ", f'On {notes["day"]}, Anticipate clear skies throughout the day with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect clear skies {notes["day"]} with ', f"I'm forecasting clear skies {notes['day']} with ", f"Prepare for clear skies {notes['day']} with "])
    elif pulledday['icon'] in storm:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a stormy {notes["day"]} with ', f"I'm forecasting the occasional storm {notes['day']} with ", f"On {notes['day']}, Prepare for a chance of a small storm with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional storm throughout the night on {notes["day"]} with ', f"I'm forecasting a chance of small storm {notes['day']} night with ", f'Anticipate a small storm throughout the night on {notes["day"]} with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional storm throughout {notes["day"]} with ', f"I'm forecasting a chance of a small storm {notes['day']} with ", f'Anticipate a small storm throughout {notes["day"]} with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a stormy {notes["day"]} with ', f"I'm forecasting a chance of a storm on {notes['day']} with ", f"Prepare for a storm {notes['day']} with "])
    elif pulledday['icon'] in snow:
        notes['context'] = 'bad'
        if 'showers' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a slightly snowy {notes["day"]} with ', f"I'm forecasting the occasional snow shower {notes['day']} with ", f"Prepare for a chance of snow showers {notes['day']} with "])
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional snow throughout {notes["day"]} night with ', f"I'm forecasting a chance of snow showers {notes['day']} night with ", f'Anticipate a small amount of snow throughout the night on {notes["day"]} with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional snow on {notes["day"]} with ', f"I'm forecasting a chance of a snow showers {notes['day']} with ", f'Anticipate a small amount of snow {notes["day"]} with '])
        else:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a snowy {notes["day"]} with ', f"I'm forecasting a chance of a snow on {notes['day']} with ", f"Prepare for a snowy {notes['day']} with "])
    elif pulledday['icon'] in misc:
        notes['context'] = 'bad'
        if 'fog' in pulledday['icon']:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a foggy {notes["day"]} with ', f"I'm forecasting fog {notes['day']} with ", f"Prepare for a chance of fog on {notes['day']} with "])
        else:
            notes['cond'] = await unifuncs.choosePhrase([f'Expect a windy {notes["day"]} with ', f"I'm forecasting a fair amount of wind {notes['day']} with ", f"Prepare for windy {notes['day']} with "])

    notes['followup'] = await unifuncs.choosePhrase([f"{notes['temp']} temperatures around {round(pulledday['feelslike'])} degrees.",
                                            f"temperatures around {round(pulledday['feelslike'])} degrees making it {notes['temp']}."])
    if notes['dew'] == "moderate":
        notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be humid outside.",
                                                    " I anticipate it being humid outside.",
                                                    " I'd expect it to be humid outside."])
    if notes['dew'] == "high":
        notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be very humid.",
                                                    " I anticipate it being very humid.",
                                                    " I'd expect it to be very humid."])

    if unit == "metric":
        notes['followup'] += await unifuncs.choosePhrase([f" The barometric pressure is {round(pulledday['pressure'])}. The cloud cover is at {round(pulledday['cloudcover'])}%. Lastly, the windspeed is {round(pulledday['windspeed'])} kilometers per hour.",
                                                    f" The barometric pressure is {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are {round(pulledday['windspeed'])} kilometers per hour.",
                                                    f" Barometric pressure is at {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are at {round(pulledday['windspeed'])} kilometers per hour."])
    else:
        notes['followup'] += await unifuncs.choosePhrase([f" The barometric pressure is {round(pulledday['pressure'])}. The cloud cover is at {round(pulledday['cloudcover'])}%. Lastly, the windspeed is {round(pulledday['windspeed'])} miles per hour.",
                                                    f" The barometric pressure is {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are {round(pulledday['windspeed'])} miles per hour.",
                                                    f" Barometric pressure is at {round(pulledday['pressure'])}, cloud cover is at {round(pulledday['cloudcover'])}%, and windspeeds are at {round(pulledday['windspeed'])} miles per hour."])

    notes['final'] = notes['cond'] + notes['followup']

    day = {'data': pulledday, 'notes': notes, 'context': notes['context'], 'message':notes['final']}
    
    print(day)

    print(day['message'])

    return day

async def sevenday():
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"    
    pulledData = requests.get(weatherData).json()
    pulledData = pulledData['days']
    pulledWeek = [pulledData[0], pulledData[1], pulledData[2], pulledData[3], pulledData[4], pulledData[5], pulledData[6]]
    week = []

    raincount = 0
    clearcount = 0
    snowcount = 0 
    cloudycount = 0
    stormcount = 0

    goodtempcount = 0
    coldtempcount = 0
    hottempcount = 0 
    verycoldtempcount = 0
    veryhottempcount = 0 

    pressurerising = 0
    pressurelowering = 0
    pressurestagnant = 0

    lastpressure = 0
    for pulledday in pulledWeek:
        notes = {}
        notes['day'] = datetime.strptime(pulledday['datetime'], "%Y-%m-%d")
        notes['day'] = notes['day'].strftime("%A")
        unit = 'imp'

        if settings.settings['unit'] == 'metric':
            reftemp = (pulledday['feelslike'] * 9/5) + 32
            dewpoint = (pulledday['dew'] * 9/5) + 32
            unit = 'metric'
        else:
            reftemp = pulledday['feelslike']
            dewpoint = pulledday['dew']

        #pressure check
        if pulledday['pressure'] > 1018:
            notes['clouds'] = "high"
        elif pulledday['pressure'] <= 1018 and pulledday['pressure'] > 1013:
            notes['clouds'] = 'moderate'
        else:
            notes['pressure'] = 'low'

        if lastpressure == 0:
            lastpressure = pulledday['pressure']
        else:
            if (lastpressure - pulledday['pressure']) >= 1:
                print(lastpressure, pulledday['pressure'], "lowering")
                pressurelowering += 1
                lastpressure = pulledday['pressure']
            elif (lastpressure - pulledday['pressure']) <= -1:
                print(lastpressure, pulledday['pressure'], "rising")
                pressurerising += 1
                lastpressure = pulledday['pressure']
            else:
                print(lastpressure, pulledday['pressure'], "stagnant")
                pressurestagnant += 1
                lastpressure = pulledday['pressure']


        # dew point check
        if dewpoint > 65:
            notes['dew'] = 'high'
        elif dewpoint > 55 and dewpoint <= 65:
            notes['dew'] = 'moderate'
        else:
            notes['dew'] = 'low'
        
        #feels like check
        if reftemp >= 100:
            notes['temp'] = ['very hot', 'scorching', 'blazing']
            veryhottempcount += 1
            if notes['dew'] == 'high':
                notes['temp'].append('humid')
                notes['temp'].append('muggy')
                notes['temp'].append('sticky')
            notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
        elif reftemp >= 75 and reftemp < 100:
            hottempcount += 1
            notes['temp'] = ['hot', 'summery', 'spicy']
            if notes['dew'] == 'high':
                notes['temp'].append('humid')
                notes['temp'].append('muggy')
                notes['temp'].append('sticky')
            notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
        elif reftemp >= 55 and reftemp < 75:
            goodtempcount += 1
            notes['temp'] = await unifuncs.choosePhrase(['moderate', 'warm', 'cool'])
        elif reftemp >= 30 and reftemp < 55:
            coldtempcount += 1
            notes['temp'] = await unifuncs.choosePhrase(['cold', 'chilly', 'crisp'])
        else:
            verycoldtempcount += 1
            notes['temp'] = await unifuncs.choosePhrase(['very cold', 'wintry', 'frosty', 'freezing cold'])

        # conditions check
        if pulledday['icon'] in rain:
            raincount += 1 
            notes['context'] = 'bad'
            if 'showers' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'On {notes["day"]} expect a rainy day with ', f"For {notes['day']}, I'm forecasting the occasional shower with ", f"Prepare for a chance of light rain on {notes['day']} with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional shower throughout {notes["day"]} night with ', f"I'm forecasting a chance of light rain {notes['day']} night with ", f'On {notes["day"]}, anticipate light rain throughout the night with '])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional shower throughout {notes["day"]} with ', f"I'm forecasting a chance of light rain {notes['day']} with ", f'On {notes["day"]}, anticipate light rain throughout the day with '])            
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a rainy {notes["day"]} with ', f"I'm forecasting a chance of rain on {notes['day']} with ", f"Prepare for rain on {notes['day']} with "])
        elif pulledday['icon'] in cloudy:
            cloudycount += 1
            notes['context'] = 'good'
            if 'partly' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a partly cloudy day on {notes["day"]} with ', f"I'm forecasting a partly cloudy {notes['day']} with ", f"Prepare for clouds throughout the day on {notes['day']} with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be partly cloudy throughout the night on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a partly cloudy night with ", f"On {notes['day']}, anticipate clouds throughout the night with "])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be partly cloudy throughout the day on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a partly cloudy day with ", f"On {notes['day']}, anticipate clouds throughout the day with "])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a cloudy {notes["day"]} with ', f"I'm forecasting a cloudy {notes['day']} with ", f"Prepare for a cloudy {notes['day']} with "])
        elif pulledday['icon'] in clear:
            clearcount += 1
            notes['context'] = 'good'
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be clear skies throughout the night on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a clear night with ", f'On {notes["day"]}, Anticipate clear skies throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be clear skies throughout the day on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a clear day with ", f'On {notes["day"]}, Anticipate clear skies throughout the day with '])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect clear skies {notes["day"]} with ', f"I'm forecasting clear skies {notes['day']} with ", f"Prepare for clear skies {notes['day']} with "])
        elif pulledday['icon'] in storm:
            stormcount += 1
            notes['context'] = 'bad'
            if 'showers' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a stormy {notes["day"]} with ', f"I'm forecasting the occasional storm {notes['day']} with ", f"On {notes['day']}, Prepare for a chance of a small storm with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional storm throughout the night on {notes["day"]} with ', f"I'm forecasting a chance of small storm {notes['day']} night with ", f'Anticipate a small storm throughout the night on {notes["day"]} with '])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional storm throughout {notes["day"]} with ', f"I'm forecasting a chance of a small storm {notes['day']} with ", f'Anticipate a small storm throughout {notes["day"]} with '])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a stormy {notes["day"]} with ', f"I'm forecasting a chance of a storm on {notes['day']} with ", f"Prepare for a storm {notes['day']} with "])
        elif pulledday['icon'] in snow:
            snowcount += 1
            notes['context'] = 'bad'
            if 'showers' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a slightly snowy {notes["day"]} with ', f"I'm forecasting the occasional snow shower {notes['day']} with ", f"Prepare for a chance of snow showers {notes['day']} with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional snow throughout {notes["day"]} night with ', f"I'm forecasting a chance of snow showers {notes['day']} night with ", f'Anticipate a small amount of snow throughout the night on {notes["day"]} with '])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional snow on {notes["day"]} with ', f"I'm forecasting a chance of a snow showers {notes['day']} with ", f'Anticipate a small amount of snow {notes["day"]} with '])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a snowy {notes["day"]} with ', f"I'm forecasting a chance of a snow on {notes['day']} with ", f"Prepare for a snowy {notes['day']} with "])
        elif pulledday['icon'] in misc:
            notes['context'] = 'bad'
            if 'fog' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a foggy {notes["day"]} with ', f"I'm forecasting fog {notes['day']} with ", f"Prepare for a chance of fog on {notes['day']} with "])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a windy {notes["day"]} with ', f"I'm forecasting a fair amount of wind {notes['day']} with ", f"Prepare for windy {notes['day']} with "])

        notes['followup'] = await unifuncs.choosePhrase([f"{notes['temp']} temperatures around {round(pulledday['feelslike'])} degrees.",
                                                f"temperatures around {round(pulledday['feelslike'])} degrees making it {notes['temp']}."])
        if notes['dew'] == "moderate":
            notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be humid outside.",
                                                        " I anticipate it being humid outside.",
                                                        " I'd expect it to be humid outside."])
        if notes['dew'] == "high":
            notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be very humid.",
                                                        " I anticipate it being very humid.",
                                                        " I'd expect it to be very humid."])
        
        notes['final'] = notes['cond'] + notes['followup']
        day = {'data': pulledday, 'notes': notes, 'context': notes['context'], 'message':notes['final']}
        week.append(day)

    finalphrase = ""
    
    conds = [raincount, stormcount, clearcount, snowcount, cloudycount]
    conds.sort(reverse=True)
    condsmost = ""
    if conds[0] == raincount:
        context = "good"
        condsmost = await unifuncs.choosePhrase(["I'm expecting a fair amount of rain this week.", "Seems like it will be fairly rainy this week.", f"I'm forecasting rain {conds[0]} days this week."])
    elif conds[0] == stormcount:
        context = "bad"
        condsmost = await unifuncs.choosePhrase(["I'm expecting frequent storms this week.", "Seems like it will be fairly stormy this week.", f"I'm forecasting storm {conds[0]} days this week."])
    elif conds[0] == clearcount:
        context = "good"
        condsmost = await unifuncs.choosePhrase(["This week seems pretty tame, with clear weather almost all week.", "Seems like it will be fairly tame this week.", f"I'm forecasting clear weather {conds[0]} days this week."])
    elif conds[0] == snowcount:
        context = "bad"
        condsmost = await unifuncs.choosePhrase(["I'm expecting lots of snow this week.", "Seems like it will be fairly snowy this week.", f"I'm forecasting snow {conds[0]} days this week."])
    else:
        context = "good"
        condsmost = await unifuncs.choosePhrase(["This week seems pretty tame, with cloudy weather almost all week.", "Seems like it will be fairly tame this week, with clouds almost everyday.", f"I'm forecasting cloudy weather {conds[0]} days this week."])

    conds = [pressurerising, pressurelowering, pressurestagnant]
    conds.sort(reverse=True)
    temps = [verycoldtempcount, veryhottempcount, coldtempcount, hottempcount, goodtempcount]
    temps.sort(reverse=True)

    tempsandpressuremost = ""
    if temps[0] == verycoldtempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures rising.", "Seems like temperatures will be cold and barometric pressure will be rising.", "I expect it to be fairly cold, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of cold temperatures every day.", "Seems like temperatures will stay fairly cold.", "I expect temperatures to be very cold every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures lowering.", "Seems like temperatures will be cold and barometric pressure will be lowering.", "I expect it to be fairly cold with atmospheric pressure lowering every day."]) 
    elif temps[0] == veryhottempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of very hot temperatures and pressures rising.", "Seems like temperatures will be very hot and barometric pressure will be rising.", "I expect it to be fairly hot, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of hot temperatures every day.", "Seems like temperatures will stay very hot.", "I expect temperatures to be very hot every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of hot temperatures and pressures lowering.", "Seems like temperatures will be hot and barometric pressure will be lowering.", "I expect it to be very hot with atmospheric pressure lowering every day."])    
    elif temps[0] == coldtempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures rising.", "Seems like temperatures will be cold and barometric pressure will be rising.", "I expect it to be cold, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of cold temperatures every day.", "Seems like temperatures will stay cold.", "I expect temperatures to be very cold every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures lowering.", "Seems like temperatures will be cold and barometric pressure will be lowering.", "I expect it to be cold with atmospheric pressure lowering every day."])        
    elif temps[0] == hottempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of hot temperatures and pressures rising.", "Seems like temperatures will be hot and barometric pressure will be rising.", "I expect it to be hot, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of hot temperatures every day.", "Seems like temperatures will stay hot.", "I expect temperatures to be hot every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of hot temperatures and pressures lowering.", "Seems like temperatures will be hot and barometric pressure will be lowering.", "I expect it to be hot with atmospheric pressure lowering every day."])    
    elif temps[0] == goodtempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of fair temperatures and pressures rising.", "Seems like temperatures will be moderate and barometric pressure will be rising.", "I expect fairly nice temperatures and tame weather with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of fair temperatures every day.", "Seems like temperatures will stay moderate.", "I expect temperatures to be moderate every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of fair temperatures and pressures lowering.", "Seems like temperatures will be moderate and barometric pressure will be lowering.", "I expect fairly nice temperatures with atmospheric pressure lowering every day."])   

    finalphrase = condsmost + " " + tempsandpressuremost
    for day in week:
        finalphrase += " " + day['message']

    week = {'message': finalphrase, 'weather': week, 'context': context}

    return week

async def fiveday():
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"    
    pulledData = requests.get(weatherData).json()
    pulledData = pulledData['days']
    pulledWeek = [pulledData[0], pulledData[1], pulledData[2], pulledData[3], pulledData[4]]
    week = []

    raincount = 0
    clearcount = 0
    snowcount = 0 
    cloudycount = 0
    stormcount = 0

    goodtempcount = 0
    coldtempcount = 0
    hottempcount = 0 
    verycoldtempcount = 0
    veryhottempcount = 0 

    pressurerising = 0
    pressurelowering = 0
    pressurestagnant = 0

    lastpressure = 0
    for pulledday in pulledWeek:
        notes = {}
        notes['day'] = datetime.strptime(pulledday['datetime'], "%Y-%m-%d")
        notes['day'] = notes['day'].strftime("%A")
        unit = 'imp'

        if settings.settings['unit'] == 'metric':
            reftemp = (pulledday['feelslike'] * 9/5) + 32
            dewpoint = (pulledday['dew'] * 9/5) + 32
            unit = 'metric'
        else:
            reftemp = pulledday['feelslike']
            dewpoint = pulledday['dew']

        #pressure check
        if pulledday['pressure'] > 1018:
            notes['clouds'] = "high"
        elif pulledday['pressure'] <= 1018 and pulledday['pressure'] > 1013:
            notes['clouds'] = 'moderate'
        else:
            notes['pressure'] = 'low'

        if lastpressure == 0:
            lastpressure = pulledday['pressure']
        else:
            if (lastpressure - pulledday['pressure']) >= 1:
                print(lastpressure, pulledday['pressure'], "lowering")
                pressurelowering += 1
                lastpressure = pulledday['pressure']
            elif (lastpressure - pulledday['pressure']) <= -1:
                print(lastpressure, pulledday['pressure'], "rising")
                pressurerising += 1
                lastpressure = pulledday['pressure']
            else:
                print(lastpressure, pulledday['pressure'], "stagnant")
                pressurestagnant += 1
                lastpressure = pulledday['pressure']


        # dew point check
        if dewpoint > 65:
            notes['dew'] = 'high'
        elif dewpoint > 55 and dewpoint <= 65:
            notes['dew'] = 'moderate'
        else:
            notes['dew'] = 'low'
        
        #feels like check
        if reftemp >= 100:
            notes['temp'] = ['very hot', 'scorching', 'blazing']
            veryhottempcount += 1
            if notes['dew'] == 'high':
                notes['temp'].append('humid')
                notes['temp'].append('muggy')
                notes['temp'].append('sticky')
            notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
        elif reftemp >= 75 and reftemp < 100:
            hottempcount += 1
            notes['temp'] = ['hot', 'summery', 'spicy']
            if notes['dew'] == 'high':
                notes['temp'].append('humid')
                notes['temp'].append('muggy')
                notes['temp'].append('sticky')
            notes['temp'] = await unifuncs.choosePhrase(notes['temp'])
        elif reftemp >= 55 and reftemp < 75:
            goodtempcount += 1
            notes['temp'] = await unifuncs.choosePhrase(['moderate', 'warm', 'cool'])
        elif reftemp >= 30 and reftemp < 55:
            coldtempcount += 1
            notes['temp'] = await unifuncs.choosePhrase(['cold', 'chilly', 'crisp'])
        else:
            verycoldtempcount += 1
            notes['temp'] = await unifuncs.choosePhrase(['very cold', 'wintry', 'frosty', 'freezing cold'])

        # conditions check
        if pulledday['icon'] in rain:
            raincount += 1 
            notes['context'] = 'bad'
            if 'showers' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'On {notes["day"]} expect a rainy day with ', f"For {notes['day']}, I'm forecasting the occasional shower with ", f"Prepare for a chance of light rain on {notes['day']} with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional shower throughout {notes["day"]} night with ', f"I'm forecasting a chance of light rain {notes['day']} night with ", f'On {notes["day"]}, anticipate light rain throughout the night with '])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional shower throughout {notes["day"]} with ', f"I'm forecasting a chance of light rain {notes['day']} with ", f'On {notes["day"]}, anticipate light rain throughout the day with '])            
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a rainy {notes["day"]} with ', f"I'm forecasting a chance of rain on {notes['day']} with ", f"Prepare for rain on {notes['day']} with "])
        elif pulledday['icon'] in cloudy:
            cloudycount += 1
            notes['context'] = 'good'
            if 'partly' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a partly cloudy day on {notes["day"]} with ', f"I'm forecasting a partly cloudy {notes['day']} with ", f"Prepare for clouds throughout the day on {notes['day']} with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be partly cloudy throughout the night on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a partly cloudy night with ", f"On {notes['day']}, anticipate clouds throughout the night with "])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be partly cloudy throughout the day on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a partly cloudy day with ", f"On {notes['day']}, anticipate clouds throughout the day with "])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a cloudy {notes["day"]} with ', f"I'm forecasting a cloudy {notes['day']} with ", f"Prepare for a cloudy {notes['day']} with "])
        elif pulledday['icon'] in clear:
            clearcount += 1
            notes['context'] = 'good'
            if 'night' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be clear skies throughout the night on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a clear night with ", f'On {notes["day"]}, Anticipate clear skies throughout the night with '])
            elif 'day' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect it to be clear skies throughout the day on {notes["day"]} with ', f"For {notes['day']}, I'm forecasting a clear day with ", f'On {notes["day"]}, Anticipate clear skies throughout the day with '])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect clear skies {notes["day"]} with ', f"I'm forecasting clear skies {notes['day']} with ", f"Prepare for clear skies {notes['day']} with "])
        elif pulledday['icon'] in storm:
            stormcount += 1
            notes['context'] = 'bad'
            if 'showers' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a stormy {notes["day"]} with ', f"I'm forecasting the occasional storm {notes['day']} with ", f"On {notes['day']}, Prepare for a chance of a small storm with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional storm throughout the night on {notes["day"]} with ', f"I'm forecasting a chance of small storm {notes['day']} night with ", f'Anticipate a small storm throughout the night on {notes["day"]} with '])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional storm throughout {notes["day"]} with ', f"I'm forecasting a chance of a small storm {notes['day']} with ", f'Anticipate a small storm throughout {notes["day"]} with '])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a stormy {notes["day"]} with ', f"I'm forecasting a chance of a storm on {notes['day']} with ", f"Prepare for a storm {notes['day']} with "])
        elif pulledday['icon'] in snow:
            snowcount += 1
            notes['context'] = 'bad'
            if 'showers' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a slightly snowy {notes["day"]} with ', f"I'm forecasting the occasional snow shower {notes['day']} with ", f"Prepare for a chance of snow showers {notes['day']} with "])
                if 'night' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional snow throughout {notes["day"]} night with ', f"I'm forecasting a chance of snow showers {notes['day']} night with ", f'Anticipate a small amount of snow throughout the night on {notes["day"]} with '])
                elif 'day' in pulledday['icon']:
                    notes['cond'] = await unifuncs.choosePhrase([f'Expect the occasional snow on {notes["day"]} with ', f"I'm forecasting a chance of a snow showers {notes['day']} with ", f'Anticipate a small amount of snow {notes["day"]} with '])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a snowy {notes["day"]} with ', f"I'm forecasting a chance of a snow on {notes['day']} with ", f"Prepare for a snowy {notes['day']} with "])
        elif pulledday['icon'] in misc:
            notes['context'] = 'bad'
            if 'fog' in pulledday['icon']:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a foggy {notes["day"]} with ', f"I'm forecasting fog {notes['day']} with ", f"Prepare for a chance of fog on {notes['day']} with "])
            else:
                notes['cond'] = await unifuncs.choosePhrase([f'Expect a windy {notes["day"]} with ', f"I'm forecasting a fair amount of wind {notes['day']} with ", f"Prepare for windy {notes['day']} with "])

        notes['followup'] = await unifuncs.choosePhrase([f"{notes['temp']} temperatures around {round(pulledday['feelslike'])} degrees.",
                                                f"temperatures around {round(pulledday['feelslike'])} degrees making it {notes['temp']}."])
        if notes['dew'] == "moderate":
            notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be humid outside.",
                                                        " I anticipate it being humid outside.",
                                                        " I'd expect it to be humid outside."])
        if notes['dew'] == "high":
            notes['followup'] += await unifuncs.choosePhrase([" I'm also expecting it to be very humid.",
                                                        " I anticipate it being very humid.",
                                                        " I'd expect it to be very humid."])
        
        notes['final'] = notes['cond'] + notes['followup']
        day = {'data': pulledday, 'notes': notes, 'context': notes['context'], 'message':notes['final']}
        week.append(day)

    finalphrase = ""
    
    conds = [raincount, stormcount, clearcount, snowcount, cloudycount]
    conds.sort(reverse=True)
    condsmost = ""
    if conds[0] == raincount:
        context = "good"
        condsmost = await unifuncs.choosePhrase(["I'm expecting a fair amount of rain this week.", "Seems like it will be fairly rainy this week.", f"I'm forecasting rain {conds[0]} days this week."])
    elif conds[0] == stormcount:
        context = "bad"
        condsmost = await unifuncs.choosePhrase(["I'm expecting frequent storms this week.", "Seems like it will be fairly stormy this week.", f"I'm forecasting storm {conds[0]} days this week."])
    elif conds[0] == clearcount:
        context = "good"
        condsmost = await unifuncs.choosePhrase(["This week seems pretty tame, with clear weather almost all week.", "Seems like it will be fairly tame this week.", f"I'm forecasting clear weather {conds[0]} days this week."])
    elif conds[0] == snowcount:
        context = "bad"
        condsmost = await unifuncs.choosePhrase(["I'm expecting lots of snow this week.", "Seems like it will be fairly snowy this week.", f"I'm forecasting snow {conds[0]} days this week."])
    else:
        context = "good"
        condsmost = await unifuncs.choosePhrase(["This week seems pretty tame, with cloudy weather almost all week.", "Seems like it will be fairly tame this week, with clouds almost everyday.", f"I'm forecasting cloudy weather {conds[0]} days this week."])

    conds = [pressurerising, pressurelowering, pressurestagnant]
    conds.sort(reverse=True)
    temps = [verycoldtempcount, veryhottempcount, coldtempcount, hottempcount, goodtempcount]
    temps.sort(reverse=True)

    tempsandpressuremost = ""
    if temps[0] == verycoldtempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures rising.", "Seems like temperatures will be cold and barometric pressure will be rising.", "I expect it to be fairly cold, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of cold temperatures every day.", "Seems like temperatures will stay fairly cold.", "I expect temperatures to be very cold every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures lowering.", "Seems like temperatures will be cold and barometric pressure will be lowering.", "I expect it to be fairly cold with atmospheric pressure lowering every day."]) 
    elif temps[0] == veryhottempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of very hot temperatures and pressures rising.", "Seems like temperatures will be very hot and barometric pressure will be rising.", "I expect it to be fairly hot, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of hot temperatures every day.", "Seems like temperatures will stay very hot.", "I expect temperatures to be very hot every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of hot temperatures and pressures lowering.", "Seems like temperatures will be hot and barometric pressure will be lowering.", "I expect it to be very hot with atmospheric pressure lowering every day."])    
    elif temps[0] == coldtempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures rising.", "Seems like temperatures will be cold and barometric pressure will be rising.", "I expect it to be cold, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of cold temperatures every day.", "Seems like temperatures will stay cold.", "I expect temperatures to be very cold every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of cold temperatures and pressures lowering.", "Seems like temperatures will be cold and barometric pressure will be lowering.", "I expect it to be cold with atmospheric pressure lowering every day."])        
    elif temps[0] == hottempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of hot temperatures and pressures rising.", "Seems like temperatures will be hot and barometric pressure will be rising.", "I expect it to be hot, but tame - with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of hot temperatures every day.", "Seems like temperatures will stay hot.", "I expect temperatures to be hot every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of hot temperatures and pressures lowering.", "Seems like temperatures will be hot and barometric pressure will be lowering.", "I expect it to be hot with atmospheric pressure lowering every day."])    
    elif temps[0] == goodtempcount:
        if conds[0] == pressurerising:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of fair temperatures and pressures rising.", "Seems like temperatures will be moderate and barometric pressure will be rising.", "I expect fairly nice temperatures and tame weather with atmospheric pressure rising every day."])
        elif conds[0] == pressurestagnant:
            tempsandpressuremost = await unifuncs.choosePhrase(["I've noticed a trend of fair temperatures every day.", "Seems like temperatures will stay moderate.", "I expect temperatures to be moderate every day."])
        else:
            tempsandpressuremost = await unifuncs.choosePhrase(["I'm noticing a trend of fair temperatures and pressures lowering.", "Seems like temperatures will be moderate and barometric pressure will be lowering.", "I expect fairly nice temperatures with atmospheric pressure lowering every day."])   

    finalphrase = condsmost + " " + tempsandpressuremost
    for day in week:
        finalphrase += " " + day['message']

    week = {'message': finalphrase, 'weather': week, 'context': context}

    return week

async def weekconditions(condition):
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"    
    pulledData = requests.get(weatherData).json()
    pulledData = pulledData['days']
    pulledWeek = [pulledData[0], pulledData[1], pulledData[2], pulledData[3], pulledData[4], pulledData[5], pulledData[6]]

    raincount = 0
    raindays = []
    clearcount = 0
    cleardays = []
    snowcount = 0 
    snowdays = []
    cloudycount = 0
    cloudydays = []
    stormcount = 0
    stormdays = []

    for day in pulledWeek:
        if day['icon'] in rain:
            raincount += 1
            day['day'] = datetime.strptime(day['datetime'], "%Y-%m-%d")
            day['day'] = day['day'].strftime("%A")

            phrasing = await unifuncs.choosePhrase([f"There is a {round(day['precipprob'])}% chance on {day['day']}.",
                                                    f"A {round(day['precipprob'])}% chance on {day['day']}.",
                                                    f"It may rain on {day['day']} with a {round(day['precipprob'])}% chance."])
            raindays.append(phrasing)
        elif day['icon'] in clear:
            clearcount += 1
            day['day'] = datetime.strptime(day['datetime'], "%Y-%m-%d")
            day['day'] = day['day'].strftime("%A")
            cleardays.append(day['day'])
        elif day['icon'] in snow:
            snowcount += 1
            day['day'] = datetime.strptime(day['datetime'], "%Y-%m-%d")
            day['day'] = day['day'].strftime("%A")

            phrasing = await unifuncs.choosePhrase([f"There is a {round(day['precipprob'])}% chance on {day['day']}.",
                                                    f"A {round(day['precipprob'])}% chance on {day['day']}.",
                                                    f"It may rain on {day['day']} with a {round(day['precipprob'])}% chance."])
            snowdays.append(phrasing)
        elif day['icon'] in cloudy:
            cloudycount += 1
            day['day'] = datetime.strptime(day['datetime'], "%Y-%m-%d")
            day['day'] = day['day'].strftime("%A")
            cloudydays.append(day['day'])    
        elif day['icon'] in snow:
            stormcount += 1
            day['day'] = datetime.strptime(day['datetime'], "%Y-%m-%d")
            day['day'] = day['day'].strftime("%A")

            phrasing = await unifuncs.choosePhrase([f"There is a {round(day['precipprob'])}% chance on {day['day']} with a {day['severerisk']}% severe risk.",
                                                    f"A {round(day['precipprob'])}% chance on {day['day']} with a {day['severerisk']}% severe risk.",
                                                    f"It may rain on {day['day']} with a {round(day['precipprob'])}% chance with a {day['severerisk']}% severe risk."])
            stormdays.append(phrasing)

    if condition == 'rain':
        if raincount == 0:
            return f"I've not forecasted any rain this week."
        else:
            return f"I've forecasted {raincount} days of rain this week. {' '.join(raindays)}"
    elif condition == "clear":
        if clearcount == 0:
            return f"I've not forecasted any clear skies this week."
        else:
            phrase = f"I've forecasted clear skies for {clearcount} days this week. On "
            for day in cleardays:
                if (cleardays.index(day) == len(cleardays) - 1) and (len(cleardays) != 1):
                    phrase += " and " + day + "."
                else:
                    phrase += day
            return phrase
    elif condition == 'snow':
        if snowcount == 0:
            return f"I've not forecasted any snow this week."
        else:
            return f"I've forecasted {snowcount} days of snow this week. {' '.join(snowdays)}"
    elif condition == "cloudy":
        if cloudycount == 0:
            return f"I've not forecasted any cloudy skies this week."
        else:
            phrase = f"I've forecasted cloudy skies for {cloudycount} days this week. On "
            for day in cloudydays:
                if (cloudydays.index(day) == len(cloudydays) - 1) and (len(cloudydays) != 1):
                    phrase += " and " + day + "."
                else:
                    phrase += day
            return phrase
    elif condition == 'storm':
        if stormcount == 0:
            if raincount > 0:
                phrase = f"I haven't forecasted any storms this week, but I am expecting rain."
                for day in raindays:
                    if (raindays.index(day) == len(raindays) - 1) and (len(raindays) != 1):
                        phrase += " and " + day
                    else:
                        phrase += " " + day
                return phrase
            else:
                return f"I've not forecasted any storms this week."
        else:
            return f"I've forecasted {stormcount} days of snow this week. {' '.join(stormdays)}"

async def finddetail(sentence, day, current=False):
    unit = 'imp'

    if settings.settings['unit'] == 'metric':
        unit = 'metric'

    if 'pressure' in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a barometic pressure of {round(day['pressure'])} currently.",
                                                f"There is currently a barometric pressure of {round(day['pressure'])}.",
                                                f"Expect an atmospheric pressure of {round(day['pressure'])} outside."])   
        else:        
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a barometic pressure of {round(day['pressure'])} on {day['dayname']}.",
                                                f"{day['dayname']} has a barometric pressure of {round(day['pressure'])}.",
                                                f"Expect an atmospheric pressure of {round(day['pressure'])} on {day['dayname']}."])
        return phrase
    elif 'rain' in sentence or 'rainy' in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a precipitation chance of {round(day['precipprob'])}% currently.",
                                                f"There is currently a precipitation chance of {round(day['precipprob'])}%.",
                                                f"Expect a precipitation chance of {round(day['precipprob'])}%."])        
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a precipitation chance of {round(day['precipprob'])}% on {day['dayname']}.",
                                                f"{day['dayname']} has a precipitation chance of {round(day['precipprob'])}%.",
                                                f"Expect a precipitation chance of {round(day['precipprob'])}% on {day['dayname']}."])
        return phrase
    elif 'dew' in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a dew point of {round(day['dew'])} degrees currently.",
                                                f"There is currently a dew point of {round(day['dew'])} degrees.",
                                                f"Expect a dew point of {round(day['dew'])} degrees."])
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a dew point of {round(day['dew'])} degrees on {day['dayname']}.",
                                                f"{day['dayname']} has a dew point of {round(day['dew'])} degrees.",
                                                f"Expect a dew point of {round(day['dew'])} degrees on {day['dayname']}."])
        return phrase
    elif 'feels' in sentence or 'feelslike' in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a feels like temperature of {round(day['feelslike'])} degrees currently.",
                                                f"There is currently a feels like temperature of {round(day['feelslike'])} degrees.",
                                                f"Expect a feels like temperature of {round(day['feelslike'])}."])            
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a feels like temperature of {round(day['feelslike'])} degrees on {day['dayname']}.",
                                                f"{day['dayname']} has a feels like temperature of {round(day['feelslike'])} degrees.",
                                                f"Expect a feels like temperature of {round(day['feelslike'])} degrees on {day['dayname']}."])
        return phrase
    elif 'high' in sentence or "highs" in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a high of {round(day['tempmax'])} degrees currently.",
                                                f"There is currently a high of {round(day['tempmax'])} degrees.",
                                                f"Expect a high of {round(day['tempmax'])} degrees."])
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a high of {round(day['tempmax'])} degrees on {day['dayname']}.",
                                                f"{day['dayname']} has a high of {round(day['tempmax'])} degrees.",
                                                f"Expect a high of {round(day['tempmax'])} degrees on {day['dayname']}."])
        return phrase   
    elif 'low' in sentence or "lows" in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a low of {round(day['tempmin'])} degrees currently.",
                                                f"There is currently a low of {round(day['tempmin'])} degrees.",
                                                f"Expect a low of {round(day['tempmin'])} degrees."])            
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a low of {round(day['tempmin'])} degrees on {day['dayname']}.",
                                                f"{day['dayname']} has a low of {round(day['tempmin'])} degrees.",
                                                f"Expect a low of {round(day['tempmin'])} degrees on {day['dayname']}."])
        return phrase    
    elif 'temperature' in sentence or 'temp' in sentence or "temps" in sentence or "temperatures" in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting an average temperature of {round(day['temp'])} degrees currently.",
                                                f"There is currently a temperature of {round(day['temp'])} degrees.",
                                                f"Expect an average temperature of {round(day['temp'])} degrees."])            
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting an average temperature of {round(day['temp'])} degrees on {day['dayname']}.",
                                                f"{day['dayname']} has a temperature of {round(day['temp'])} degrees.",
                                                f"Expect an average temperature of {round(day['temp'])} degrees on {day['dayname']}."])
        return phrase
    elif 'cloud' in sentence and 'cover' in sentence or "cloud" in sentence and "coverage" in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting {round(day['cloudcover'])}% cloud coverage currently.",
                                                f"There is currently a cloud coverage of {round(day['cloudcover'])}%.",
                                                f"Expect a {round(day['temp'])}% cloud coverage."])

        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting {round(day['cloudcover'])}% cloud coverage on {day['dayname']}.",
                                                f"{day['dayname']} has a cloud coverage of {round(day['cloudcover'])}%.",
                                                f"Expect a {round(day['temp'])}% cloud coverage on {day['dayname']}."])
        return phrase
    elif ('uv' in sentence and 'index' in sentence) or 'uvi' in sentence or "uv" in sentence:
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a U V index of {round(day['uvindex'])} currently.",
                                                  f"There is currently a U V index of {round(day['uvindex'])}.",
                                                  f"Expect a U V index of {round(day['uvindex'])}."])
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a U V index of {round(day['uvindex'])} on {day['dayname']}.",
                                                  f"{day['dayname']} has a U V index of {round(day['uvindex'])}.",
                                                  f"Expect a U V index of {round(day['uvindex'])} on {day['dayname']}."])
        return phrase
    elif 'sunrise' in sentence or 'rise' in sentence:
        returntime = datetime.strptime(day['sunrise'], "%H:%M:%S")
        returntime = returntime.strftime("%I:%M %p")
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a sunrise time around {returntime}.",
                                                f"The sun is expected to rise around {returntime}.",
                                                f"Expect the sun to rise around {returntime}."])        
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a sunrise time around {returntime} on {day['dayname']}.",
                                                f"{day['dayname']} has a sunrise time of {returntime}.",
                                                f"Expect the sun to rise around {returntime} on {day['dayname']}."])
        return phrase
    elif 'sunset' in sentence or 'sun' in sentence:
        returntime = datetime.strptime(day['sunset'], "%H:%M:%S")
        returntime = returntime.strftime("%I:%M %p")
        if current == True:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a sunset time around {returntime}.",
                                                f"The sun is expected to set around {returntime}.",
                                                f"Expect the sun to set around {returntime}."])        
        else:
            phrase = await unifuncs.choosePhrase([f"I'm forecasting a sunset time around {returntime} on {day['dayname']}.",
                                                f"{day['dayname']} has a sunset time of {returntime}.",
                                                f"Expect the sun to set around {returntime} on {day['dayname']}."])
        return phrase
    elif ("wind" in sentence and "speed" in sentence) or ("winds" in sentence or "speeds" in sentence) or 'windy' in sentence:
        if unit == 'metric':
            if current == True:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind speeds around {round(day['windspeed'])} kilometers per hour currently.",
                                                    f"The current wind speeds are around {round(day['windspeed'])} kilometers per hour.",
                                                    f"Expect wind speeds around {round(day['windspeed'])} kilometers per hour."]) 
            else:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind speeds around {round(day['windspeed'])} kilometers per hour on {day['dayname']}.",
                                                    f"{day['dayname']} has wind speeds around {round(day['windspeed'])} kilometers per hour.",
                                                    f"Expect wind speeds around {round(day['windspeed'])} kilometers per hour on {day['dayname']}."])    
        else:
            if current == True:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind speeds around {round(day['windspeed'])} miles per hour currently.",
                                                    f"The current wind speeds are around {round(day['windspeed'])} miles per hour.",
                                                    f"Expect wind speeds around {round(day['windspeed'])} miles per hour."]) 
            else:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind speeds around {round(day['windspeed'])} miles per hour on {day['dayname']}.",
                                                    f"{day['dayname']} has wind speeds around {round(day['windspeed'])} miles per hour.",
                                                    f"Expect wind speeds around {round(day['windspeed'])} miles per hour on {day['dayname']}."])        
        return phrase
    elif ("wind" in sentence and "gust" in sentence) or ("winds" in sentence or "gusts" in sentence):
        if unit == 'metric':
            if current == True:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind gusts around {round(day['windspeed'])} kilometers per hour currently.",
                                                    f"The current wind gusts are around {round(day['windspeed'])} kilometers per hour.",
                                                    f"Expect wind gusts around {round(day['windspeed'])} kilometers per hour."]) 
            else:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind gusts around {round(day['windspeed'])} kilometers per hour on {day['dayname']}.",
                                                    f"{day['dayname']} has wind gusts around {round(day['windspeed'])} kilometers per hour.",
                                                    f"Expect wind gusts around {round(day['windspeed'])} kilometers per hour on {day['dayname']}."])    
        else:
            if current == True:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind gusts around {round(day['windspeed'])} miles per hour currently.",
                                                    f"The current wind gusts are around {round(day['windspeed'])} miles per hour.",
                                                    f"Expect wind gusts around {round(day['windspeed'])} miles per hour."]) 
            else:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting wind gusts around {round(day['windspeed'])} miles per hour on {day['dayname']}.",
                                                    f"{day['dayname']} has wind gusts around {round(day['windspeed'])} miles per hour.",
                                                    f"Expect wind gusts around {round(day['windspeed'])} miles per hour on {day['dayname']}."])        
        return phrase
    elif 'severe' in sentence or 'risk' in sentence:
        if 'severerisk' in day:
            if current == True:
                if day['severerisk'] <= 15:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting no chance of severe weather currently.",
                                                        f"Currently, there is no chance of severe weather.",
                                                        f"Expect no chance of severe weather."])        
                    return phrase
                elif day['severerisk'] > 15 and day['severerisk'] < 30:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting a low risk of severe weather currently.",
                                                        f"Currently, there is a low risk of severe weather.",
                                                        f"Expect a low risk of severe weather."])        
                    return phrase
                elif day['severerisk'] > 29 and day['severerisk'] < 60:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting a moderate risk of severe weather currently.",
                                                        f"Currently, there is a moderate risk of severe weather.",
                                                        f"Expect a moderate risk of severe weather."])         
                    return phrase
                else:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting a high risk of severe weather currently.",
                                                        f"Currently, there is a high risk of severe weather.",
                                                        f"Expect a high risk of severe weather."])          
                    return phrase                
            else:
                if day['severerisk'] <= 15:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting no chance of severe weather on {day['dayname']}.",
                                                        f"{day['dayname']} has no chance of severe weather.",
                                                        f"Expect no chance of severe weather on {day['dayname']}."])        
                    return phrase
                elif day['severerisk'] > 15 and day['severerisk'] < 30:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting a low risk of severe weather on {day['dayname']}.",
                                                        f"{day['dayname']} has a low risk of severe weather.",
                                                        f"Expect a low risk of severe weather on {day['dayname']}."])        
                    return phrase
                elif day['severerisk'] > 29 and day['severerisk'] < 60:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting a moderate risk of severe weather on {day['dayname']}.",
                                                        f"{day['dayname']} has a moderate risk of severe weather.",
                                                        f"Expect a moderate risk of severe weather on {day['dayname']}."])        
                    return phrase
                else:
                    phrase = await unifuncs.choosePhrase([f"I'm forecasting a high risk of severe weather on {day['dayname']}.",
                                                        f"{day['dayname']} has a high risk of severe weather.",
                                                        f"Expect a high risk of severe weather on {day['dayname']}."])        
                    return phrase
        else: 
            return "There is no chance of severe weather."
    elif "moon" in sentence or ("moon" in sentence and "phase" in sentence) or "lunar" in sentence:
        if current == True:
            if day['moonphase'] == 0:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a new moon.",
                                                    f"The moon phase is new moon.",
                                                    f"Expect a new moon."])        
                return phrase
            elif day['moonphase'] < 0.25 and day['moonphase'] > 0:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waxing crescent.",
                                                    f"The moon phase is waxing crescent.",
                                                    f"Expect a waxing crescent."])        
                return phrase
            elif day['moonphase'] == .25:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting the first quarter.",
                                                    f"The moon phase is first quarter.",
                                                    f"Expect the first quarter."])        
                return phrase
            elif day['moonphase'] < 0.5 and day['moonphase'] > 0.25:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waxing gibbous.",
                                                    f"The moon phase is waxing gibbous.",
                                                    f"Expect a waxing gibbous on."])        
                return phrase
            elif day['moonphase'] == .5:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a full moon.",
                                                    f"The moon phase is full moon.",
                                                    f"Expect a full moon."])        
                return phrase        
            elif day['moonphase'] < 0.75 and day['moonphase'] > 0.5:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waning gibbous.",
                                                    f"The moon phase is waning gibbous.",
                                                    f"Expect a waning gibbous."])        
                return phrase
            elif day['moonphase'] == .75:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting the last quarter.",
                                                    f"The moon phase on is last quarter.",
                                                    f"Expect the last quarter on."])        
                return phrase                
            elif day['moonphase'] < 1 and day['moonphase'] > 0.75:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waning crescent.",
                                                    f"The moon phase is waning crescent.",
                                                    f"Expect a waning crescent."])        
                return phrase
        else:
            if day['moonphase'] == 0:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a new moon on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is new moon.",
                                                    f"Expect a new moon on {day['dayname']}."])        
                return phrase
            elif day['moonphase'] < 0.25 and day['moonphase'] > 0:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waxing crescent on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is waxing crescent.",
                                                    f"Expect a waxing crescent on {day['dayname']}."])        
                return phrase
            elif day['moonphase'] == .25:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting the first quarter on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is first quarter.",
                                                    f"Expect the first quarter on {day['dayname']}."])        
                return phrase
            elif day['moonphase'] < 0.5 and day['moonphase'] > 0.25:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waxing gibbous on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is waxing gibbous.",
                                                    f"Expect a waxing gibbous on {day['dayname']}."])        
                return phrase
            elif day['moonphase'] == .5:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a full moon on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is full moon.",
                                                    f"Expect a full moon on {day['dayname']}."])        
                return phrase        
            elif day['moonphase'] < 0.75 and day['moonphase'] > 0.5:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waning gibbous on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is waning gibbous.",
                                                    f"Expect a waning gibbous on {day['dayname']}."])        
                return phrase
            elif day['moonphase'] == .75:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting the last quarter on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is last quarter.",
                                                    f"Expect the last quarter on {day['dayname']}."])        
                return phrase                
            elif day['moonphase'] < 1 and day['moonphase'] > 0.75:
                phrase = await unifuncs.choosePhrase([f"I'm forecasting a waning crescent on {day['dayname']}.",
                                                    f"The moon phase on {day['dayname']} is waning crescent.",
                                                    f"Expect a waning crescent on {day['dayname']}."])        
                return phrase
    else:
        return "error?"

async def grabdetail(sentence, day):
    weatherData = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{settings.settings['zipcode']}?unitGroup={settings.settings['unit']}&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"    
    if day != "current": 
        pulledData = requests.get(weatherData).json()
        pulledData = pulledData['days']
        pulledWeek = [pulledData[0], pulledData[1], pulledData[2], pulledData[3], pulledData[4], pulledData[5], pulledData[6]]
        trueWeek = []

        for fakeday in pulledWeek:
            new = fakeday
            dayname = datetime.strptime(fakeday['datetime'], "%Y-%m-%d")
            dayname = dayname.strftime("%A")
            new['dayname'] = dayname
            trueWeek.append(fakeday)

        result = ""

        if day != "week":
            if day.lower() == 'today':
                print(day)
                day = trueWeek[0]
                result = await finddetail(sentence, day)
                return result
            else:
                for fakeday in trueWeek:
                    if day.lower() == fakeday['dayname'].lower():
                        day = fakeday
                        result = await finddetail(sentence, day)
                        return result
        else:
            for fakeday in pulledWeek:
                result += await finddetail(sentence, fakeday) + " "
            return result
    else:
        pulledData = requests.get(weatherData).json()
        pulledday = pulledData['currentConditions']
        result = await finddetail(sentence, pulledday, current=True)
        return result