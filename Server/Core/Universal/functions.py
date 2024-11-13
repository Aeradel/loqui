import json
import random 
import asyncio 

async def makerequest(type, title, result, excess=None):
    result = json.dumps({'type':type, 'title':title, 'result':result, 'excess':excess})
    result = result.encode('utf-8')
    return result

async def parserequest(request):
    '''
    type, message, profile, excess
    '''
    request = request.decode('utf-8')
    result = json.loads(request)
    return result

async def choosePhrase(phrases):
    phrase1 = random.choice(phrases)
    phrase2 = random.choice(phrases)
    phrase3 = random.choice(phrases)
    final = random.choice([phrase1, phrase2, phrase3])
    return final

async def checkforyesorno(sentence):
    confirmations = ["yes", "yea", "yeah", "ok", "okay", "okeydoke", "okeydokey", "aye", "ay", "alright", "yep", "exactly", "sure", 'roger', 'affirmative', 'indeed', 'certainly', 'course', 'absolutely', 'yup', 'yah']
    declines = ['quit', 'exit', 'no', 'nope', 'not', 'never', 'nah', 'nope', 'nae', 'naw', 'nay', 'nix', 'stop']

    answer = ""

    for confirmation in confirmations:
        if confirmation in sentence:
            answer = "yes"
    
    for decline in declines:
        if decline in sentence:
            answer = "no"
    
    return answer
