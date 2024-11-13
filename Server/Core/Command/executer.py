from Skills.Automation import execute as autoexe
from Skills.Client import execute as clientexe
from Skills.Conversational import execute as converexe
from Skills.Google import execute as googleexe
from Skills.Memory import execute as memoryexe
from Skills.Walmart import execute as walmartexe
from Skills.Weather import execute as weatherexe

tables = [autoexe, clientexe, converexe, googleexe, memoryexe, walmartexe, weatherexe]


async def grade(gradedkey, gradingkeys):
    highestconfidence = 0
    for key in gradingkeys:
        totalpoints = 0
        pointspossible = 0
        newkey = key.split(" ")
        for newword in newkey:
            pointspossible += 1
            for word in gradedkey:
                if word in newword or word == newword:
                    totalpoints += 1
                if word is "remember" and "remember" in newkey:
                    totalpoints += 100        
                if word is "add" and "add" in newkey:
                    totalpoints += 100
                if word is "remind" and "remind" in newkey:
                    totalpoints += 100
        confidence = round((totalpoints / pointspossible) * 100)
        if highestconfidence < confidence:
            highestconfidence = confidence
    return highestconfidence

async def truegrade(gradedkey, gradingkeys, require, blacklist):

    highestconfidence = 0

    for key in gradingkeys:
        totalpoints = 0
        pointspossible = 0
        newkey = key.split(" ")
        for newword in newkey:
            pointspossible += 1
            for word in gradedkey:
                if word in newword.lower():
                    totalpoints += 1
                if word in require:
                    totalpoints += 5
                if word in blacklist:
                    totalpoints -= 1000
                if word is "remember" and "remember" in newkey:
                    totalpoints += 100
        confidence = round((totalpoints / pointspossible) * 100)
        if highestconfidence < confidence:
            highestconfidence = confidence
    return highestconfidence

async def exe(sentence, profile, excess):
    sentence = sentence.lower()
    whitelist = set('abcdefghijklmnopqrstuvwxyz 1234567890')
    sentence = ''.join(filter(whitelist.__contains__, sentence))
    literal = sentence 
    sentence = sentence.split(" ")

    bestResult = [1,1]
    secondBestResult = [1,1]

    for table in tables:
        if len(table.keywords) > 0:
            confidence = await grade(sentence, table.keywords)
            if bestResult is None or confidence > bestResult[0]:
                if secondBestResult is None or bestResult[0] > secondBestResult[0]:
                    secondBestResult = bestResult
                bestResult = [confidence, table]
            elif secondBestResult is None or confidence > secondBestResult[0]:
                secondBestResult = [confidence, table]

    bestSkillResult = [1,1]
    secondBestSkillResult = [1,1]

    for skill in bestResult[1].skills:
        skill = bestResult[1].skills[skill]
        confidence = await truegrade(sentence, skill['keys'], skill['require'], skill['blacklist'])
        if confidence > bestSkillResult[0]:
            secondBestSkillResult = bestSkillResult
            bestSkillResult = [confidence, skill]
        elif confidence > secondBestSkillResult[0]:
            secondBestSkillResult = [confidence, skill]

    if bestResult[0] < 60 or bestSkillResult == [1, 1]:
        for table in tables:
            if len(table.keywords) > 0: 
                if len(table.skills) > 0:
                    for skill in table.skills:
                        skill = table.skills[skill]
                        confidence = await truegrade(sentence, skill['keys'], skill['require'], skill['blacklist'])
                        if confidence > bestSkillResult[0]:
                            secondBestSkillResult = bestSkillResult
                            bestSkillResult = [confidence, skill]
                        elif confidence > secondBestSkillResult[0]:
                            secondBestSkillResult = [confidence, skill]
    
    result = await bestSkillResult[1]['function'](sentence, profile, excess, literal)
    if result['result'] == "completed":
        return result
    else:
        raise Exception(repr(result))