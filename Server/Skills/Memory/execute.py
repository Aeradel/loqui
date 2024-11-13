from Core.Client import profiles

import asyncio

keywords = []


async def remember(sentence, profile, excess, literal):
    global skills
    global keywords

    if sentence[sentence.index("remember") + 1] == "my":
        if "favorite" in sentence:
            noun = sentence[sentence.index("favorite") + 1]
            placement = sentence.index(sentence[sentence.index(noun) + 1])
            if sentence[sentence.index(noun) + 1] != 'is' and sentence[sentence.index(noun) + 1] != 'are':
                placement = sentence.index(sentence[sentence.index(noun) + 2])
                noun += " " + sentence[sentence.index(noun) + 1]
            if sentence[placement] == "is" or sentence[placement] == "are":
                item = " ".join(sentence[(placement + 1):])
            else:
                if "is" in sentence:
                    item = " ".join(sentence[(sentence.index("is") + 1):])
                elif "are" in sentence:
                    item = " ".join(sentence[(sentence.index("is") + 1):])

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    await profiles.profiles.addattribute(sprofile, "favorites", noun, item)

            phrase = f"I have now remembered your favorite {noun} is {item}."

            await init()

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    profile = await profiles.profiles.convertprofile(sprofile)
        else:
            noun = sentence[sentence.index("my") + 1]
            placement = sentence.index(sentence[sentence.index(noun) + 1])
            if sentence[sentence.index(noun) + 1] != 'is' and sentence[sentence.index(noun) + 1] != 'are':
                placement = sentence.index(sentence[sentence.index(noun) + 2])
                noun += " " + sentence[sentence.index(noun) + 1]
            if sentence[placement] == "is" or sentence[placement] == "are":
                item = " ".join(sentence[(placement + 1):])
            else:
                if "is" in sentence:
                    item = " ".join(sentence[(sentence.index("is") + 1):])
                elif "are" in sentence:
                    item = " ".join(sentence[(sentence.index("is") + 1):])

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    await profiles.profiles.addattribute(sprofile, "details", noun, item)

            phrase = f"I have now remembered your {noun} is {item}."

            await init()

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    profile = await profiles.profiles.convertprofile(sprofile)

    elif sentence[sentence.index("remember") + 1] != "my":
        name = ""
        refprofile = None
        for sprofile in profiles.savedprofiles:
            if sprofile.name.lower() in sentence:
                name = sprofile.name.lower()
                refname = name
                refprofile = sprofile
            elif sprofile.name.lower() + "s" in sentence:
                name = sprofile.name.lower()
                refname = name + "s"
                refprofile = sprofile
        
        if refprofile is not None:
            if "favorite" in sentence:
                noun = sentence[sentence.index("favorite") + 1]
                placement = sentence.index(sentence[sentence.index(noun) + 1])
                if sentence[sentence.index(noun) + 1] != 'is' and sentence[sentence.index(noun) + 1] != 'are':
                    placement = sentence.index(sentence[sentence.index(noun) + 2])
                    noun += " " + sentence[sentence.index(noun) + 1]
                if sentence[placement] == "is" or sentence[placement] == "are":
                    item = " ".join(sentence[(placement + 1):])
                else:
                    if "is" in sentence:
                        item = " ".join(sentence[(sentence.index("is") + 1):])
                    elif "are" in sentence:
                        item = " ".join(sentence[(sentence.index("is") + 1):])

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name:
                        await profiles.profiles.addattribute(sprofile, "favorites", noun, item)


                if 'pronouns' in sprofile.details:
                    phrase = f"I have now remembered {sprofile.details['pronouns'][1]} favorite {noun} is {item}."
                else:
                    phrase = f"I have now remembered {name}s favorite {noun} is {item}."

                await init()

            else:
                noun = sentence[sentence.index(refname) + 1]
                placement = sentence.index(sentence[sentence.index(noun) + 1])
                if sentence[sentence.index(noun) + 1] != 'is' and sentence[sentence.index(noun) + 1] != 'are':
                    placement = sentence.index(sentence[sentence.index(noun) + 2])
                    noun += " " + sentence[sentence.index(noun) + 1]
                if sentence[placement] == "is" or sentence[placement] == "are":
                    item = " ".join(sentence[(placement + 1):])
                else:
                    if "is" in sentence:
                        item = " ".join(sentence[(sentence.index("is") + 1):])
                    elif "are" in sentence:
                        item = " ".join(sentence[(sentence.index("is") + 1):])

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name:
                        await profiles.profiles.addattribute(sprofile, "details", noun, item)

                if 'pronouns' in sprofile.details:
                    phrase = f"I have now remembered {sprofile.details['pronouns'][1]} {noun} is {item}."
                else:
                    phrase = f"I have now remembered {name}s {noun} is {item}."

                await init()
                            
        else:
            phrase = "I was not able to find a profile under that name."

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def queryremember(sentence, profile, excess, literal):
    if "my" in sentence:
        if "favorite" in sentence:
            noun = " ".join(sentence[(sentence.index('favorite') + 1):])
            if " is" in noun: 
                noun = noun.replace(" is", "")            
            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    profile = await profiles.profiles.convertprofile(sprofile)

            if noun in profile['favorites']:
                phrase = f"I've remembered your favorite {noun} is {profile['favorites'][noun]}."
            else:
                phrase = f"I don't think I remember your favorite {noun}."
        else:
            noun = " ".join(sentence[(sentence.index('my') + 1):])
            if " is" in noun: 
                noun = noun.replace(" is", "")
            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    profile = await profiles.profiles.convertprofile(sprofile)

            if noun in profile['details']:
                phrase = f"I've remembered your {noun} is {profile['details'][noun]}."
            else:
                phrase = f"I don't think I remember your {noun}."            
    else:
        name = ""
        refprofile = None
        for sprofile in profiles.savedprofiles:
            if sprofile.name.lower() in sentence:
                name = sprofile.name.lower()
                refname = name
                refprofile = sprofile
            elif sprofile.name.lower() + "s" in sentence:
                name = sprofile.name.lower()
                refname = name + "s"
                refprofile = sprofile
        
        if refprofile is not None:
            if "favorite" in sentence:
                noun = " ".join(sentence[(sentence.index('favorite') + 1):])
                if " is" in noun: 
                    noun = noun.replace(" is", "")               
                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name or sprofile.name.lower() + "s" == name:
                        refprofile = await profiles.profiles.convertprofile(sprofile)

                if noun in refprofile['favorites']:
                    if 'pronouns' in refprofile['details']:
                        phrase = f"I remembered {refprofile['details']['pronouns'][1]} favorite {noun} is {refprofile['favorites'][noun]}."
                    else:
                        phrase = f"I remembered {name}'s favorite {noun} is {refprofile['favorites'][noun]}."                    
                else:
                    phrase = f"I don't think I remember {name}'s favorite {noun}."
            else:
                noun = " ".join(sentence[(sentence.index(refname) + 1):])
                if " is" in noun: 
                    noun = noun.replace(" is", "")
                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name or sprofile.name.lower() + "s" == name:
                        refprofile = await profiles.profiles.convertprofile(sprofile)

                if noun in refprofile['details']:
                    if 'pronouns' in refprofile['details']:
                        phrase = f"I remembered {refprofile['details']['pronouns'][1]} {noun} is {refprofile['details'][noun]}."
                    else:
                        phrase = f"I remembered {name}'s {noun} is {refprofile['details'][noun]}."                    
                else:
                    phrase = f"I don't think I remember {name}'s {noun}."                              
        else:
            phrase = "I do not remember that name saved in the profiles."   

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def change(sentence, profile, excess, literal):
    global skills
    global keywords

    if sentence[sentence.index("change") + 1] == "my":
        if "favorite" in sentence:
            noun = sentence[sentence.index("favorite") + 1]
            placement = sentence.index(sentence[sentence.index(noun) + 1])
            if sentence[sentence.index(noun) + 1] != 'to':
                placement = sentence.index(sentence[sentence.index(noun) + 2])
                noun += " " + sentence[sentence.index(noun) + 1]
            if sentence[placement] == "to":
                item = " ".join(sentence[(placement + 1):])
            else:
                if "to" in sentence:
                    item = " ".join(sentence[(sentence.index("to") + 1):])

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    refprofile = sprofile
                
            if noun not in sprofile.favorites:
                phrase = f"I was not able to find {noun} in your remembered favorites."
            else:
                await profiles.profiles.addattribute(refprofile, "favorites", noun, item)

                phrase = f"I have now changed your favorite {noun} to {item}."

                await init()

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == profile['name']:
                        profile = await profiles.profiles.convertprofile(sprofile)
        else:
            noun = sentence[sentence.index("my") + 1]
            placement = sentence.index(sentence[sentence.index(noun) + 1])
            if sentence[sentence.index(noun) + 1] != 'to':
                placement = sentence.index(sentence[sentence.index(noun) + 2])
                noun += " " + sentence[sentence.index(noun) + 1]
            if sentence[placement] == "to":
                item = " ".join(sentence[(placement + 1):])
            else:
                if "to" in sentence:
                    item = " ".join(sentence[(sentence.index("to") + 1):])

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                        refprofile = sprofile
                
            if noun not in sprofile.favorites:
                phrase = f"I was not able to find {noun} in your remembered details."
            else:
                await profiles.profiles.addattribute(refprofile, "details", noun, item)

                phrase = f"I have now changed your {noun} to {item}."

                await init()

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == profile['name']:
                        profile = await profiles.profiles.convertprofile(sprofile)

    elif sentence[sentence.index("change") + 1] != "my":
        name = ""
        refprofile = None
        for sprofile in profiles.savedprofiles:
            if sprofile.name.lower() in sentence:
                name = sprofile.name.lower()
                refname = name
                refprofile = sprofile
            elif sprofile.name.lower() + "s" in sentence:
                name = sprofile.name.lower()
                refname = name + "s"
                refprofile = sprofile
        
        if refprofile is not None:
            if "favorite" in sentence:
                noun = sentence[sentence.index(refname) + 1]
                placement = sentence.index(sentence[sentence.index(noun) + 1])
                if sentence[sentence.index(noun) + 1] != 'to':
                    placement = sentence.index(sentence[sentence.index(noun) + 2])
                    noun += " " + sentence[sentence.index(noun) + 1]
                if sentence[placement] == "to":
                    item = " ".join(sentence[(placement + 1):])
                else:
                    if "to" in sentence:
                        item = " ".join(sentence[(sentence.index("to") + 1):])

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name:
                        rprofile = sprofile
                
                if noun not in sprofile.favorites:
                    phrase = f"I was not able to find {noun} in {name}'s remembered favorites."
                else:
                    await profiles.profiles.addattribute(rprofile, "favorites", noun, item)


                    if 'pronouns' in sprofile.details:
                        phrase = f"I have now changed {sprofile.details['pronouns'][1]} favorite {noun} to {item}."
                    else:
                        phrase = f"I have now changed {name}'s favorite {noun} to {item}."

                    await init()

            else:
                noun = sentence[sentence.index(refname) + 1]
                placement = sentence.index(sentence[sentence.index(noun) + 1])
                if sentence[sentence.index(noun) + 1] != 'to':
                    placement = sentence.index(sentence[sentence.index(noun) + 2])
                    noun += " " + sentence[sentence.index(noun) + 1]
                if sentence[placement] == "to":
                    item = " ".join(sentence[(placement + 1):])
                else:
                    if "to" in sentence:
                        item = " ".join(sentence[(sentence.index("to") + 1):])


                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name:
                        rprofile = sprofile
                
                if noun not in sprofile.favorites:
                    phrase = f"I was not able to find {noun} in {name}'s remembered details."
                else:
                    await profiles.profiles.addattribute(sprofile, "details", noun, item)

                    if 'pronouns' in sprofile.details:
                        phrase = f"I have now changed {sprofile.details['pronouns'][1]} {noun} to {item}."
                    else:
                        phrase = f"I have now changed {name}'s {noun} to {item}."


                    await init()
                             
        else:
            phrase = "I was not able to find a profile under that name."

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def forget(sentence, profile, excess, literal):

    if sentence[sentence.index("forget") + 1] == "my":
        if "favorite" in sentence:
            noun = sentence[sentence.index("favorite") + 1:]
            noun = " ".join(noun)
            
            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    refprofile = sprofile
            
            if noun not in sprofile.favorites:
                phrase = f"I was not able to find {noun} in your remembered favorites."
            else:
                await profiles.profiles.forgetattribute(refprofile, "favorites", noun)

                phrase = f"I have now forgotten your favorite {noun}."

                await init()
               
                for sprofile in profiles.savedprofiles:
                    if sprofile.name == profile['name']:
                        profile = await profiles.profiles.convertprofile(sprofile)
        else:
            noun = sentence[sentence.index("my") + 1:]
            noun = " ".join(noun)

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    refprofile = sprofile

            if noun not in sprofile.details:
                phrase = f"I was not able to find {noun} in your remembered details."
            else:
                await profiles.profiles.forgetattribute(refprofile, "details", noun)

                phrase = f"I have now forgotten your {noun}."
                
                await init()

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == profile['name']:
                        profile = await profiles.profiles.convertprofile(sprofile)

    elif sentence[sentence.index("forget") + 1] != "my":
        name = ""
        refprofile = None
        for sprofile in profiles.savedprofiles:
            if sprofile.name.lower() in sentence:
                name = sprofile.name.lower()
                refname = name
                refprofile = sprofile
            elif sprofile.name.lower() + "s" in sentence:
                name = sprofile.name.lower()
                refname = name + "s"
                refprofile = sprofile
        
        if refprofile is not None:
            if "favorite" in sentence:
                noun = sentence[sentence.index(refname) + 1:]
                noun = " ".join(noun)

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name:
                        rprofile = sprofile
                
                if noun not in sprofile.favorites:
                    phrase = f"I was not able to find {noun} in {name}'s remembered favorites."
                else:
                    await profiles.profiles.forgetattribute(rprofile, "favorites", noun)


                    if 'pronouns' in sprofile.details:
                        phrase = f"I have now forgotten {sprofile.details['pronouns'][1]} favorite {noun}."
                    else:
                        phrase = f"I have now forgotten {name}'s favorite {noun}."

                    await init()
            else:

                noun = sentence[sentence.index(refname) + 1:]
                noun = " ".join(noun)

                for sprofile in profiles.savedprofiles:
                    if sprofile.name == name:
                        rprofile = sprofile
                
                if noun not in sprofile.details:
                    phrase = f"I was not able to find {noun} in {name}'s remembered details."
                else:
                    await profiles.profiles.forgetattribute(rprofile, "details", noun)

                    if 'pronouns' in sprofile.details:
                        phrase = f"I have now forgotten {sprofile.details['pronouns'][1]} {noun}."
                    else:
                        phrase = f"I have now forgotten {name}'s {noun}."

                    await init()      
        else:
            phrase = "I was not able to find a profile under that name."

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

skills = {

    'remember': {
        'function': remember,
        'keys': ['remember favorite is', 'remember favorite are'],
        'require': ['remember', 'favorite', 'is'],
        'blacklist': ['do', 'you', 'add', 'grocery'],
    },
    'queryremember': {
        'function': queryremember,
        'keys': [],
        'require': ['remember', 'favorite', 'is'],
        'blacklist': ['add', 'grocery'],
    },
    'change': {
        'function': change,
        'keys': [],
        'require': ['change', 'to'],
        'blacklist': ['remember', 'add', 'grocery'],
    },   
    'forget': {
        'function': forget,
        'keys': [],
        'require': ['forget'],
        'blacklist': ['remember', 'change', 'add', 'grocery'],
    },   
}

async def init():
    global keywords
    global skills
    
    for profile in profiles.savedprofiles:
        if len(profile.favorites) > 0:
            for item in profile.favorites:
                skills['queryremember']['keys'].append(f"do you remember {profile.name}s favorite {item}")
                skills['queryremember']['keys'].append(f"what is {profile.name}s favorite {item}")
                skills['queryremember']['keys'].append(f"what are {profile.name}s favorite {item}")
                skills['queryremember']['keys'].append(f"does {profile.name}s like {item}")
                skills['queryremember']['keys'].append(f"do you remember my favorite {item}")
                skills['queryremember']['keys'].append(f"what is my favorite {item}")
                skills['queryremember']['keys'].append(f"what are my favorite {item}")
                skills['change']['keys'].append(f"change {profile.name}s favorite {item} to")
                skills['change']['keys'].append(f"modify {profile.name}s favorite {item} to")
                skills['change']['keys'].append(f"switch {profile.name}s favorite {item} to")
                skills['change']['keys'].append(f"alter {profile.name}s favorite {item} to")
                skills['change']['keys'].append(f"change my favorite {item} to")
                skills['change']['keys'].append(f"modify my favorite {item} to")
                skills['change']['keys'].append(f"switch my favorite {item} to")
                skills['change']['keys'].append(f"alter my favorite {item} to")
                skills['forget']['keys'].append(f"forget my favorite {item}")
                skills['forget']['keys'].append(f"forget {profile.name}s favorite {item}")

        if len(profile.details) > 0:
            for item in profile.details:
                skills['queryremember']['keys'].append(f"do you remember {profile.name}s {item}")
                skills['queryremember']['keys'].append(f"what is {profile.name}s {item}")
                skills['queryremember']['keys'].append(f"what are {profile.name}s {item}")
                skills['queryremember']['keys'].append(f"does {profile.name}s like {item}")
                skills['queryremember']['keys'].append(f"do you remember my {item}")
                skills['queryremember']['keys'].append(f"what is my {item}")
                skills['queryremember']['keys'].append(f"what are my {item}")
                skills['change']['keys'].append(f"change {profile.name}s {item} to")
                skills['change']['keys'].append(f"modify {profile.name}s {item} to")
                skills['change']['keys'].append(f"switch {profile.name}s {item} to")
                skills['change']['keys'].append(f"alter {profile.name}s {item} to")
                skills['change']['keys'].append(f"change my {item} to")
                skills['change']['keys'].append(f"modify my {item} to")
                skills['change']['keys'].append(f"switch my {item} to")
                skills['change']['keys'].append(f"alter my {item} to")    
                skills['forget']['keys'].append(f"forget my {item}")
                skills['forget']['keys'].append(f"forget {profile.name}s {item}") 

    for function in skills:
        for key in skills[function]['keys']:
            keywords.append(key)