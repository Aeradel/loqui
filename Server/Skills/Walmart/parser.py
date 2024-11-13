from re import S
from Skills.Walmart import settings
from Core.Data import permanent
from Core.Universal import functions

from serpapi import GoogleSearch


async def fixtitle(title):

    title = title.replace("&amp;", " and ")

    return title

async def getprice():
    if not permanent.data['walmart']:
        permanent.data['walmart'] = {}
    if not permanent.data['walmart']['list']:
        permanent.data['walmart']['list'] = []
        permanent.data['walmart']['listprice'] = 0

    if len(permanent.data['walmart']['list']) == 0:
        phrase = "There is currently nothing on the grocery list."
    else:    
        phrase = await functions.choosePhrase([
            f"There are currently {len(permanent.data['walmart']['list'])} items in your grocery list with the total estimated price of ${permanent.data['walmart']['listprice']}.",
            f"The current estimated price is ${permanent.data['walmart']['listprice']}. There are {len(permanent.data['walmart']['list'])} items in your grocery list.",
            f"The current price of your list is ${permanent.data['walmart']['listprice']}. There are {len(permanent.data['walmart']['list'])} items in your list."
        ])

    return phrase

async def getlist(phrase = True):
    storelist = {}
    if not permanent.data['walmart']:
        permanent.data['walmart'] = {}
    if not permanent.data['walmart']['list']:
        permanent.data['walmart']['list'] = []
        permanent.data['walmart']['listprice'] = 0
    if len(permanent.data['walmart']['list']) == 0:
        finalphrase = "There is currently nothing on the grocery list."
        return finalphrase
    else:
        for item in permanent.data['walmart']['list']:
            if item['refcategory'] is not None:
                if item['refcategory'] in storelist:
                    if item['refname'] is not None:
                        storelist[item['refcategory']].append([item['refname'], item['price']])
                    else:
                        storelist[item['refcategory']].append([item['name'], item['price']])
                else:
                    storelist[item['refcategory']] = []
                    if item['refname'] is not None:
                        storelist[item['refcategory']].append([item['refname'], item['price']])
                    else:
                        storelist[item['refcategory']].append([item['name'], item['price']])
            else:
                if not "Uncategorized" in storelist:
                    storelist['Uncategorized'] = []
                if item['refname'] is not None:
                    storelist["Uncategorized"].append([item['refname'], item['price']])
                else:
                    storelist["Uncategorized"].append([item['name'], item['price']])                

        if phrase:
            finalphrase = ""
            for category in storelist:
                finalphrase += await functions.choosePhrase([f" In the {category} category: ", f" In {category}: ", f" For the category, {category}: "])
                for item in storelist[category]:
                    finalphrase += " " + item[0] + ","
        else:
            finalphrase = ""
            for category in storelist:
                finalprice = 0
                itemphrase = ""
                for item in storelist[category]:
                    itemphrase += "   " + item[0] + " | $" + str(item[1]) + "\n"
                    finalprice += item[1]

                finalphrase += f"{category} | ${finalprice} | {len(storelist[category])} items \n"
                finalphrase += itemphrase

        return finalphrase

async def translate(item, specific=None):
    phrase = ""
    if specific is None:
        if item['name'] is not "Unknown":
            if item['refname'] is not None:
                phrase += item['refname'] + "."
            else:
                phrase += item['name'] + "."
        else:
            phrase += item['description'] + "."

        if "Best seller" in item['excesstext']:
            phrase += await functions.choosePhrase([" This item is also considered a best seller.", " This item is a best seller.", " Walmart has attributed this item as a best seller."])
        elif "Popular pick" in item['excesstext']:
            phrase += await functions.choosePhrase([" This item is also considered a popular pick.", " This item is a popular pick.", " Walmart has attributed this item as a popular pick."])
    
    elif specific is 'more':
        phrase += await functions.choosePhrase([f"This item's current price is  ${item['price']}.", 
                                                f"This item is currently listed at ${item['price']}.", 
                                                f"The price for this item is currently listed at ${item['price']}."]) + " "

        if item['description'] is not "Unknown":
            phrase += await functions.choosePhrase([f"The description is as follows: {item['description']}.", 
                                                    f"The description describes this item as follows: {item['description']}.", 
                                                    f"The vendor has described this item as follows: {item['description']}"]) + " "

        phrase += await functions.choosePhrase([f"This item has {item['ratings']} reviews with an average rating of {item['rating']}.", 
                                                f"{item['ratings']} reviews put this item at an average rating of {item['rating']}.", 
                                                f"This item has received a rating of {item['rating']} from {item['ratings']} reviews."]) + " "

    elif specific is "price":
        phrase += await functions.choosePhrase([f"This item's current price is  ${item['price']}.", 
                                                f"This item is currently listed at ${item['price']}.", 
                                                f"The price for this item is currently listed at ${item['price']}."]) + " "      

    elif specific is "description":
        if item['description'] is not "Unknown":
            phrase += await functions.choosePhrase([f"The description is as follows: {item['description']}.", 
                                                    f"The description describes this item as follows: {item['description']}.", 
                                                    f"The vendor has described this item as follows: {item['description']}"]) + " "
        else:
            phrase += await functions.choosePhrase(["There is no description provided by the vendor for this item.", "I was not able to find a description provided by the vendor.", "There is no description provided for this item."])
    
    elif specific is "rating":
        phrase += await functions.choosePhrase([f"This item has {item['ratings']} reviews with an average rating of {item['rating']}.", 
                                                f"{item['ratings']} reviews put this item at an average rating of {item['rating']}.", 
                                                f"This item has received a rating of {item['rating']} from {item['ratings']} reviews."]) + " "
    
    elif specific is "name":

        if item['name'] != "Unknown":
            phrase += item['name']
        else:
            phrase += item['description']

        if "Best seller" in item['excesstext']:
            phrase += await functions.choosePhrase([" This item is also considered a best seller.", " This item is a best seller.", " Walmart has attributed this item as a best seller."])
        elif "Popular pick" in item['excesstext']:
            phrase += await functions.choosePhrase([" This item is also considered a popular pick.", " This item is a popular pick.", " Walmart has attributed this item as a popular pick."])

    return phrase

async def addtolist(item):

    if type(item) is dict:

        if "walmart" not in permanent.data:
            permanent.data['walmart'] = []

        if "list" not in permanent.data['walmart']:
            permanent.data['walmart']['list'] = []
            permanent.data['walmart']['listprice'] = 0

        permanent.data['walmart']['list'].append(item)
        
        if item['price'] is not "Unknown":
            permanent.data['walmart']['listprice'] += item['price']
        
        if item['refname'] is not None:
            phrase = f"I've added {item['refname']} to your grocery list."
        else:
            phrase = f"I've added {item['name']} to your grocery list."

    else:

        result = None
        for ritem in permanent.data['walmart']['cache']:
            if 'refname' in ritem and ritem['refname'] is not None and ritem['refname'] is item:
                permanent.data['walmart']['list'].append(ritem)
                
                if ritem['price'] is not "Unknown":
                    permanent.data['walmart']['listprice'] += ritem['price']
                result = ritem
                phrase = f"I've added {ritem['refname']} to your grocery list."
            if ritem['name'] is item:
                permanent.data['walmart']['list'].append(ritem)
                
                if ritem['price'] is not "Unknown":
                    permanent.data['walmart']['listprice'] += ritem['price']                
                result = ritem
                phrase = f"I've added {ritem['name']} to your grocery list."

        if result is None:
            phrase = f"I was not able to find {item} in your saved grocery items. Try searching using the brand name."

    return phrase

async def removefromlist(item):

    if type(item) is dict:

        if "walmart" not in permanent.data:
            permanent.data['walmart'] = []

        if "list" not in permanent.data['walmart']:
            permanent.data['walmart']['list'] = []
            permanent.data['walmart']['listprice'] = 0

        if item in permanent.data['walmart']['list']:

            permanent.data['walmart']['list'].remove(item)
            
            if item['price'] is not "Unknown":
                permanent.data['walmart']['listprice'] -= item['price']
            
            if item['refname'] is not None:
                phrase = f"I've removed {item['refname']} from your grocery list."
            else:
                phrase = f"I've removed {item['name']} from your grocery list."

    else:

        result = None
        for ritem in permanent.data['walmart']['list']:

            if ritem['refname'] is not None and (ritem['refname'].lower() is item or item in ritem['refname'].lower()):
                permanent.data['walmart']['list'].remove(ritem)
                
                if ritem['price'] is not "Unknown":
                    permanent.data['walmart']['listprice'] -= ritem['price']
                result = ritem
                phrase = f"I've removed {ritem['refname']} from your grocery list."
                
            if ritem['name'].lower() is item or item in ritem['name'].lower():
                permanent.data['walmart']['list'].remove(ritem)
                
                if ritem['price'] is not "Unknown":
                    permanent.data['walmart']['listprice'] -= ritem['price']                
                result = ritem
                phrase = f"I've removed {ritem['name']} from your grocery list."

        if result is None:
            phrase = f"I was not able to find {item} in your grocery list. Try referencing the item with a different name."

    return phrase

async def removefromcache(item):

    if type(item) is dict:

        if "walmart" not in permanent.data:
            permanent.data['walmart'] = []

        if "cache" not in permanent.data['walmart']:
            permanent.data['walmart']['cache'] = []

        if item in permanent.data['walmart']['cache']:

            if item['refname'] is not None:
                phrase = f"I've removed {item['refname']} from your Walmart cache."
            else:
                phrase = f"I've removed {item['name']} from your Walmart cache."

            permanent.data['walmart']['cache'].remove(item)
            
    else:

        result = None
        for ritem in permanent.data['walmart']['cache']:

            if ritem['refname'] is not None and (ritem['refname'].lower() is item or item in ritem['refname'].lower()):

                result = ritem
                phrase = f"I've removed {ritem['refname']} from your Walmart cache."
                permanent.data['walmart']['cache'].remove(ritem)

                
            if ritem['name'].lower() is item or item in ritem['name'].lower():
                result = ritem
                phrase = f"I've removed {ritem['name']} from your Walmart cache."
                permanent.data['walmart']['cache'].remove(ritem)

        if result is None:
            phrase = f"I was not able to find {item} in your Walmart cache. Try referencing the item with a different name."

    return phrase

async def checkforcorrections(sentence):

    sentence = sentence.replace("&amp;", " and ")

    secondaryphrase = sentence.split(" ")

    finalphrase = ""

    for word in secondaryphrase:
        lettercount = 0
        for letter in word:
            if letter.isupper() and word[word.index(letter) - 1].islower():
                finalphrase = finalphrase.rstrip()
                finalphrase += ". " + letter
            else:
                finalphrase += letter
            lettercount += 1
            
        finalphrase += " "		    
    
    return finalphrase

async def checkforexact(name, items):

    foundexactresult = False

    if items is not None and len(items) != 0:
        for item in items:
            if 'refname' in item and item['refname'] is not None and (item['refname'] is name or name in item['refname']):
                return True, item
        

    if not foundexactresult:
        return False, None

async def pull(query, forcesearch=False):

    if "walmart" not in permanent.data or type(permanent.data['walmart']) is list:
        permanent.data['walmart'] = {}
    
    if not 'cache' in permanent.data['walmart'] or permanent.data['walmart']['cache'] is None:
        permanent.data['walmart']['cache'] = []

    results = []

    if not forcesearch:

        foundexactresult, item = await checkforexact(query['query'], permanent.data['walmart']['cache'])
        
        print(foundexactresult)

        if not foundexactresult:
            for item in permanent.data['walmart']['cache']:
                print(item)
                if query['query'] in item['query'] or ("secondaryquery" in item and query['query'] in item['secondaryquery']) or (item['refname'] is not None and query['query'] in item['refname']) or query['query'] in item['name']:
                        results.append(item)
        else:
            results.append(item)

    if len(results) == 0:
        search = GoogleSearch(query)
        search = search.get_dict()
        errorcheck = search['search_metadata']

        if 'error' in errorcheck['status'] or 'Error' in errorcheck['status']:
            print(repr(search))
            return None

        finalresults = []

        if 'organic_results' in search:
            stop = False
            for item in search['organic_results']:
                if not stop:
                    if search['organic_results'].index(item) > 19:
                        stop = True

                    savedresult = {}

                    savedresult['query'] = query['query']

                    if 'search_parameters' in search:
                        savedresult['secondaryquery'] = search['search_parameters']['query']


                    if "title" in item:
                        savedresult['name'] = await fixtitle(item['title'])
                    else:
                        savedresult['name'] = "Unknown"

                    if "description" in item:
                        savedresult['description'] = await checkforcorrections(item['description'])
                    else:
                        savedresult['description'] = "Unknown"

                    if "us_item_id" in item:
                        savedresult['id'] = item['us_item_id']
                    else:
                        savedresult['id'] = "Unknown"

                    if "product_id" in item:
                        savedresult['productid'] = item['product_id']
                    else:
                        savedresult['productid'] = 'Unknown'
                    
                    if "special_offer_text" in item:
                        savedresult["excesstext"] = item["special_offer_text"]
                    else:
                        savedresult['excesstext'] = "None"

                    if "rating" in item:
                        savedresult["rating"] = item["rating"]
                    else:
                        savedresult['rating'] = "None"

                    if "reviews" in item:
                        savedresult["ratings"] = item["reviews"]
                    else:
                        savedresult['ratings'] = "None"

                    savedresult['refname'] = None
                    savedresult['refcategory'] = None

                    if "primary_offer" in item:
                        if item["primary_offer"]['offer_price'] == 0:
                            if "min_price" in item["primary_offer"]:
                                savedresult["price"] = round(item["primary_offer"]['min_price'])
                            else:
                                savedresult["price"] = "Unknown"
                        else:
                            savedresult["price"] = round(item["primary_offer"]['offer_price'])
                    else:
                        savedresult['price'] = "Unknown"
        
                    permanent.data['walmart']['cache'].append(savedresult)

                    finalresults.append(savedresult)
                else:
                    return finalresults   

        return finalresults

    else:

        return results