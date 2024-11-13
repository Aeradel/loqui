from Skills.Walmart import settings
from Skills.Walmart import parser as exe
from Core.Data import temporary as temp
from Core.Data import permanent as perm
from Core.Universal import functions as unifuncs

keywords = []

lastsinglesearch = None

async def walmartforget(sentence):
    pass

## FORGET REFERENCE NAME FOR ITEM
## FORGET CATEGORY NAME FOR ITEM

## ADD REFERENCE NAME FOR ITEM
## ADD CATEGORY NAME FOR ITEM

async def edititem(sentence, profile, excess, literal):
    if ("reference" in sentence and "name" in sentence) or ("saved" in sentence and "name" in sentence) or "name" in sentence:
        if "for" in sentence:
            if "to" in sentence:
                noun = sentence[sentence.index('for')+1:sentence.index('to')]

        if noun and ("remove" in sentence or "delete" in sentence or "forget" in sentence or "erase" in sentence):
                pass
        elif noun and ("change" in sentence or "edit" in sentence or "alter" in sentence or "add" in sentence or "set" in sentence):
                pass
    
    if ("reference" in sentence and "category" in sentence) or ("saved" in sentence and "category" in sentence) or "name" in sentence:
                pass
            
async def removecache(sentence, profile, excess, literal):
    if "remove" in sentence:
        if "from" in sentence:
            noun = sentence[sentence.index('remove')+1:sentence.index('from')]
        else:
            noun = sentence[sentence.index('remove')+1:]
    elif "delete" in sentence:
        if "from" in sentence:
            noun = sentence[sentence.index('delete')+1:sentence.index('from')]
        else:
            noun = sentence[sentence.index('delete')+1:]
    elif "erase" in sentence:
        if "from" in sentence:
            noun = sentence[sentence.index('erase')+1:sentence.index('from')]
        else:
            noun = sentence[sentence.index('erase')+1:]  

    if not noun:
        phrase = "I was not able to understand what you want me to remove from the Walmart cache. Please rephrase your request."
    else:
        noun = " ".join(noun)
        phrase = await exe.removefromcache(noun)

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def removelist(sentence, profile, excess, literal):
    if "remove" in sentence:
        if "from" in sentence:
            noun = sentence[sentence.index('remove')+1:sentence.index('from')]
        else:
            noun = sentence[sentence.index('remove')+1:]
    elif "delete" in sentence:
        if "from" in sentence:
            noun = sentence[sentence.index('delete')+1:sentence.index('from')]
        else:
            noun = sentence[sentence.index('delete')+1:]
    elif "erase" in sentence:
        if "from" in sentence:
            noun = sentence[sentence.index('erase')+1:sentence.index('from')]
        else:
            noun = sentence[sentence.index('erase')+1:]  

    if not noun:
        phrase = "I was not able to understand what you want me to remove from the grocery list. Please rephrase your request."
    else:
        noun = " ".join(noun)
        phrase = await exe.removefromlist(noun)

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def grablist(sentence, profile, excess, literal):

    if "full" in sentence:

        result = await exe.getlist(phrase=False)

    else:

        result = await exe.getlist()

    return {'result': 'completed', 'text': result, 'profile': profile, 'excess': None}

async def grabprice(sentence, profile, excess, literal):

    result = await exe.getprice()

    return {'result': 'completed', 'text': result, 'profile': profile, 'excess': None}

async def walmartquery(sentence, profile, excess, literal):

    global lastsinglesearch

    if excess and 'query' in excess and excess['query'] == "itemconfirmation":
        answer = await unifuncs.checkforyesorno(excess['queryanswer'])
        if answer == "yes":

            item = temp.data['walmart'][0][temp.data['walmart'][1]]
            result = await exe.addtolist(item)
            if item['refname'] is None:
                phrase = result + " I was not able to find a reference name for this item. A reference name can make it easier for you to add this item to your grocery list. Would you like to add a reference name for this item?"
                retexcess = {'queried': 'true', 'query': 'refnameconfirmation', 'possiblekeys': 'confirmation'}
                temp.data['walmart'] = item
            else:
                phrase = result
                retexcess = None
        else:
            itemnumber = temp.data['walmart'][1] + 1
            
            if itemnumber > len(temp.data['walmart'][0])-1:

                phrase = "There are no more listed items. Try adding again using more specific details, like a brand name or another descriptor."
                retexcess = None

            else:
                item = temp.data['walmart'][0][itemnumber]

                phrase = f"The next item is {await exe.translate(item)} Would you like to add this item to your grocery list?"
                temp.data['walmart'][1] = itemnumber

                retexcess = {'queried': 'true', 'query': 'itemconfirmation', 'possiblekeys': 'confirmation', 'excess': temp.data['walmart'][0], 'currentquery': item}            
    elif excess and 'query' in excess and excess['query'] == 'refnameconfirmation':  
        answer = await unifuncs.checkforyesorno(excess['queryanswer'])

        if answer == "yes":
            phrase = f"What would you like to refer to {temp.data['walmart']['name']} as?"
            retexcess = {'queried': 'true', 'query': 'refnamequery', 'possiblekeys': None}
        else:
            phrase = "Understood."
            retexcess = None
    elif excess and 'query' in excess and excess['query'] == "refnamequery":
        for item in perm.data['walmart']['cache']:
            if 'id' in item and item['id'] == temp.data['walmart']['id']:
                item['refname'] = " ".join(excess['queryanswer'])
                phrase = f"I will now remember the item as {item['refname']}. Next time, just ask to add {item['refname']} to the list."

        phrase += " Naming a category for this item could make it easier for you to organize your grocery list when exported. Would you like categorize to this item?"
        retexcess = {'queried': 'true', 'query': 'categoryconfirmation', 'possiblekeys': 'confirmation'}
    elif excess and 'query' in excess and excess['query'] == 'categoryconfirmation':

        answer = await unifuncs.checkforyesorno(excess['queryanswer'])
        
        item = temp.data['walmart']

        if answer == "yes":
            if item['refname'] is not None:
                phrase = f"What category would you like to put {item['refname']} into?"
            else:
                phrase = f"What category would you like to put {item['name']} into?"

            retexcess = {'queried': 'true', 'query': 'categoryquery', 'possiblekeys': None}

        else:
            phrase = "Understood"
            retexcess = None
    elif excess and 'query' in excess and excess['query'] == "categoryquery":
        for item in perm.data['walmart']['cache']:
            if 'id' in item and item['id'] == temp.data['walmart']['id']:
                item['refcategory'] = " ".join(excess['queryanswer'])
                phrase = f"I will now categorize {item['refname']} into {item['refcategory']}. When you export the item, it will be grouped with other items in the {item['refcategory']} category."
                retexcess = None 
    elif excess and 'query' in excess and excess['query'] == 'singleitemconfirmation':

        answer = await unifuncs.checkforyesorno(excess['queryanswer'])

        item = temp.data['walmart']

        if answer == "yes":
            phrase = await exe.addtolist(item)
            retexcess = None
        else:
            
            noun = lastsinglesearch
            
            params1 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey1'],
                'store_id': settings.settings['store_id']    }

            params2 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey2'],
                'store_id': settings.settings['store_id']    }

            params3 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey3'],
                'store_id': settings.settings['store_id']    }

            params4 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey4'],
                'store_id': settings.settings['store_id']    }

            params5 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey5'],
                'store_id': settings.settings['store_id']    }

            params = [params1, params2, params3, params4, params5]

            stop = False

            for param in params:
                if not stop:
                    result = await exe.pull(param, forcesearch=True)
                    if result:
                        stop = True

            phrase = "I will start a new search using the same query."

            if not result:
                phrase += " There was an error with the Walmart search engine. Please try again later."
                retexcess = None
            else:
                if len(result) == 1:
                    temp.data['walmart'] = result[0]
                    phrase += f" I was able to find one item for your search for {noun}."
                    phrase += f" {await exe.translate(result[0])} Would you like to add this item to your grocery list?"

                    lastsinglesearch = noun 

                    retexcess = {'queried': 'true', 'query': 'singleitemconfirmation', 'possiblekeys': 'confirmation'}
                else:
                    phrase += f" I found multiple items for your search for {noun} "
                    phrase += f"The first product is {await exe.translate(result[0])} Would you like to add this item to your grocery list?"

                    if 'walmart' not in temp.data:
                        temp.data['walmart'] = []

                    temp.data['walmart'] = [result, 0]

                    retexcess = {'queried': 'true', 'query': 'itemconfirmation', 'possiblekeys': 'confirmation', 'excess': result, 'currentquery': result[0]}            
    else:
        if "add" in sentence or "get" in sentence:
            if "add" in sentence and "to" in sentence:
                noun = sentence[sentence.index('add')+1:sentence.index('to')]

            elif "get" in sentence:
                if "from" in sentence:
                    noun = sentence[sentence.index('get')+1:sentence.index('from')]
                else:
                    noun = sentence[sentence.index('get')+1:]

            noun = " ".join(noun)

            params1 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey1'],
                'store_id': settings.settings['store_id']    }

            params2 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey2'],
                'store_id': settings.settings['store_id']    }

            params3 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey3'],
                'store_id': settings.settings['store_id']    }

            params4 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey4'],
                'store_id': settings.settings['store_id']    }

            params5 = {
                'engine': 'walmart',
                'query': noun,
                'q': noun,
                'api_key': settings.settings['walmartkey5'],
                'store_id': settings.settings['store_id']    }

            params = [params1, params2, params3, params4, params5]

            stop = False

            for param in params:
                if not stop:
                    result = await exe.pull(param)
                    if result:
                        stop = True
    
            if not result:
                phrase = "There was an error with the Walmart search engine. Please try again later."
                retexcess = None
            else:
                if len(result) == 1:
                    temp.data['walmart'] = result[0]
                    phrase = f"I was able to find one item for your search for {noun}."
                    phrase += f" {await exe.translate(result[0])} Would you like to add this item to your grocery list?"  

                    lastsinglesearch = noun 

                    retexcess = {'queried': 'true', 'query': 'singleitemconfirmation', 'possiblekeys': 'confirmation'}
                    
                else:
                    phrase = f"I found multiple items for your search for {noun} "
                    phrase += f"The first product is {await exe.translate(result[0])} Would you like to add this item to your grocery list?"

                    if 'walmart' not in temp.data:
                        temp.data['walmart'] = []

                    temp.data['walmart'] = [result, 0]

                    retexcess = {'queried': 'true', 'query': 'itemconfirmation', 'possiblekeys': 'confirmation', 'excess': result, 'currentquery': result[0]}


    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': retexcess}

async def clearcache(sentence, profile, excess, literal):

    if excess and 'query' in excess and excess['query'] == 'cacheconfirmation':

        result = await unifuncs.checkforyesorno(excess['queryanswer'])

        if result == "yes":
            perm.data['walmart']['cache'] = []

            phrase = "I have now cleared your walmart cache. This will effect previously saved items or reference names given to items."
        else:
            phrase = "I have canceled the operation."

        return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}
    else:
        phrase = "Are you sure you would like to clear your Walmart cache? This operation will lead to longer wait times and deleted previously saved items or reference names given to items."
        
        return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': {'queried': 'true', 'query':'cacheconfirmation'}}

async def clearmylist(sentence, profile, excess, literal):
    if excess and 'query' in excess and excess['query'] == 'listconfirmation':
        result = await unifuncs.checkforyesorno(excess['queryanswer'])

        if result == "yes":
            perm.data['walmart']['list'] = []

            phrase = "I have now cleared your grocery list."
        else:
            phrase = "I have canceled the operation."

        return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

    else:
        phrase = "Are you sure you would like to clear your grocery list?"

        return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': {'queried': 'true', 'query':'listconfirmation'}}
  

skills = {
    'walmartquery': {
        'function': walmartquery,
        'keys': ['add to grocery list', 'add to list', 'remind me to get from walmart', 'remind me to get from the store', 'add to shopping list'],
        'require': ['add', 'to', 'grocery', 'walmart', 'store', 'get', 'shopping'],
        'blacklist': [],
    },
    'listquery': {
        'function': grablist,
        'keys': ['what is in my walmart list', 'what is on my grocery list', 'check', 'what is on my list', 'what is on the walmart list', 'read me my list', 'read me my walmart list', 'read me my grocery list', 'what is my list', 'what is my grocery list', 'what is my walmart list'],
        'require': ['list', 'read', 'walmart', 'grocery', 'check'],
        'blacklist': ['add', 'get'],
    },
    'pricelistquery': {
        'function': grabprice,
        'keys': ['what is my grocery list price', 'what is the cost of my groceries', 'how much do my groceries cost', 'what is my grocery list cost', 'what is the total price of my groceries', 'what is the total cost of my groceries', 'what is the cost of the list', 'what is the price of the list'],
        'require': ['cost', 'price', 'list', 'grocery'],
        'blacklist': ['add', 'get'],
    },
    'clearcache': {
        'function': clearcache,
        'keys': ['clear my walmart cache', 'clear my cache'],
        'require': ['clear', 'cache'],
        'blacklist': [],
    },
    'clearmylist': {
        'function': clearmylist,
        'keys': ['clear my walmart list', 'clear my list', 'clear my grocery list', 'restart my list', 'restart my grocery list', 'restart my walmart list'],
        'require': ['clear', 'restart', 'list'],
        'blacklist': [],
    },
    'removeitem': {
        'function': removelist,
        'keys': ['remove from my walmart list', 'remove from my grocery list', 'remove from my list', 'remove from the walmart list', 'remove from the grocery list', 'remove from the list', 
                 'delete from my walmart list', 'delete from my grocery list', 'delete from my list', 'delete from the walmart list', 'delete from the grocery list', 'delete from the list', 
                 'erase from my walmart list', 'erase from my grocery list', 'erase from my list', 'erase from the walmart list', 'erase from the grocery list', 'erase from the list', ],
        'require': ['remove', 'delete', 'erase', 'list'],
        'blacklist': [],
    },
    'removecache': {
        'function': removecache,
        'keys': ['remove from my walmart cache', 'remove from my grocery cache', 'remove from my cache', 'remove from the walmart cache', 'remove from the grocery cache', 'remove from the cache', 
                 'delete from my walmart cache', 'delete from my grocery cache', 'delete from my cache', 'delete from the walmart cache', 'delete from the grocery cache', 'delete from the cache', 
                 'erase from my walmart cache', 'erase from my grocery cache', 'erase from my cache', 'erase from the walmart cache', 'erase from the grocery cache', 'erase from the cache', ],
        'require': ['remove', 'delete', 'erase', 'cache'],
        'blacklist': [],
    },

}

for function in skills:
    for key in skills[function]['keys']:
        keywords.append(key)
