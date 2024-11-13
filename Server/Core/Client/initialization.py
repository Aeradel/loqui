from Core.Client import profiles as profs

import random
import asyncio 

words = ['thought', 'city', 'tree', 'cross', 'farm', 'hard', 'start', 'might', 'story', 'saw', 'far', 'sea', 'draw', 'left', 'late', 'run', 'while', 'press', 'close', 'night', 'real', 'life', 'few', 'north', 'open', 'seem', 'together', 'next', 'white', 'children', 'begin', 'got', 'walk', 'example', 'ease', 'paper', 'group', 'always', 'music', 'those', 'both', 'mark', 'often', 'letter', 'until', 'mile', 'river', 'car', 'feet']


async def init(name, clientaddr):
    """name, client, key"""
    if await profs.checkprofile(name):
        result, profile = await profs.checkprofile(name)
        return "Found existing profile", profile
    else:
        chosenword = random.choice(words)
        profile = profs.profiles(name, clientaddr, chosenword)
        profs.savedprofiles.append(profile)
        return "Created new profile", profile

async def initstart():
    print("""
    
        ──────────────────────────────────────────────────────────────────────────
        ─██████─────────██████████████─██████████████───██████──██████─██████████─
        ─██░░██─────────██░░░░░░░░░░██─██░░░░░░░░░░██───██░░██──██░░██─██░░░░░░██─
        ─██░░██─────────██░░██████░░██─██░░██████░░██───██░░██──██░░██─████░░████─
        ─██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██──██░░██───██░░██───
        ─██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██──██░░██───██░░██───
        ─██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██──██░░██───██░░██───
        ─██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██──██░░██───██░░██───
        ─██░░██─────────██░░██──██░░██─██░░██──██░░██───██░░██──██░░██───██░░██───
        ─██░░██████████─██░░██████░░██─██░░██████░░████─██░░██████░░██─████░░████─
        ─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░██─
        ─██████████████─██████████████─████████████████─██████████████─██████████─
        ──────────────────────────────────────────────────────────────────────────
                by nate                                 started: 4/15/2022                                     
    
    """)