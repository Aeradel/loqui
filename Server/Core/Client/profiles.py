savedprofiles = []

class profiles():
    def __init__(self, profilename, clientregistered, basickey):
            '''self, profilename, clientregistered, basickey'''

            self.name = profilename.lower()
            self.mainclient = clientregistered
            self.key = basickey.lower()
            self.favorites = {}
            self.details = {}
            self.clients = [clientregistered]

    async def addfavoriteitem(self, item, itemid, price, noun, excess):
        '''self, item, itemid, price, descriptive-noun, excess'''
        if 'walmart' not in self.favorites:
            self.favorites['walmart'] = {}
        
        self.favorites['walmart'][noun] = {'price': price, 'name': item, 'id': itemid, 'excess': excess}

    async def addattribute(self, category, attribute, value=None):
        '''self, category, attribute, value || details (dict), favorites (dict), clients (list)'''

        if category == "details":

            if attribute == 'pronouns':

                self.details[attribute] = []

                newval = value.split(" ")
                self.details[attribute].append(newval[0])
                self.details[attribute].append(newval[1])

            else:

                self.details[attribute] = value

        elif category == "favorites":

            self.favorites[attribute] = value

        elif category == "clients":

            self.clients.append(attribute)

    async def forgetattribute(self, category, attribute):

        if category == 'details':

            self.details.pop(attribute, None)    

        if category == 'favorites':

            self.favorites.pop(attribute, None)    

        if category == 'clients':

            self.clients.pop(attribute, None)

    async def convertprofile(self):
        newprofile = {
            "name": self.name,
            "mainclient": self.mainclient,
            "key": self.key,
            "favorites": self.favorites,
            "details": self.details,
            "clients": self.clients,
        }
        return newprofile
        
async def checkprofile(name, key=None):
    
    for profile in savedprofiles:
        if (profile.name == name.lower() or profile.name in name.lower()) and (not key or (key.lower() and profile.key == key.lower())):
            return True, profile
            
    return False