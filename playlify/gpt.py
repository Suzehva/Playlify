# arguments:
'''
The results set has the song titles from crawled playlists and song titles from the context
- make a gpt prompt based on the diagram that has fewshot prompting
- in the task description, pass in the context 
- return the sentence (str), specific songs used and their ids (as JSON?)

- in the main file the return list has the context already in it so make these separate things that are passed in

- input is context (str) and results (set of tuples where tuple[0] is song title and tuple[1] is id)

'''
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI
client = OpenAI()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def create_sentence(context, results):
    # make a fewshot prompt
    # make a task description with context
    # make a .env file with api key 
    # how do I make a list of all the song titles to make a sentence but still have the id for each song <-- multiple songs can't have same title because we removed duplicates
    # return the sentence and the songs with ids 
    # update all this in the main 

    task_description = ""
    task_description += '''
        EXAMPLE: 
        Below you will find a list of words/phrases with their ID's. Your goal is to construct a brief sentence made from ONLY the song titles below and return the song IDs used in the final sentence as a list.
        Here is the user's context for the sentence: I want to propose to my girlfriend. Here is a set of tuples where each tuple[0] is the song title and the tuple[1] is the song ID. 
        {('Let Me Love You', 'spotify:track:3ibKnFDaa3GhpPGlOUj7ff'), ('For the First Time', 'spotify:track:2R4AlwtrrkMaRKojcTIzmL'),
        ("It's You", 'spotify:track:5DqdesEfbRyOlSS3Tf6c29'), ('Just the Way You Are', 'spotify:track:7BqBn9nzAq8spo5e7cZ0dJ'),
        ("I'll Stand by You", 'spotify:track:3Nf8oGn1okobzjDcFCvT6n'), ('Baby', 'spotify:track:6epn3r7S14KUqlReYr77hA'),
        ('How Am I Supposed to Live Without You', 'spotify:track:3RMeOetCdXttthQK0clPuz')}. 
        Do NOT use any other words. Do NOT break up any words/phrases used. If you can't construct a sentence
        using ONLY the song titles we provide, try again. Otherwise, return "Couldn't generate playlist. Try modifying context or mood."
        Baby It's You I'll Stand by You Let Me Love You ['spotify:track:6epn3r7S14KUqlReYr77hA', 'spotify:track:5DqdesEfbRyOlSS3Tf6c29', 'spotify:track:5DqdesEfbRyOlSS3Tf6c29', 'spotify:track:3ibKnFDaa3GhpPGlOUj7ff']. 

        EXAMPLE: 
        Below you will find a list of words/phrases with their ID's. Your goal is to construct a brief sentence made from ONLY the song titles below.
        Here is the user's context for the sentence: I want to motivate my gym partner. Here is a set of tuples where each tuple[0] is the song title and the tuple[1] is the song ID. 
        {('Hype Boy', 'spotify:track:0a4MMyCrzT0En247IhqZbD'), ('Softly', 'spotify:track:0YQJoDL6f46J0n1rOVkpxJ'), 
        ('Freed from Desire - Techno Version', 'spotify:track:5YGrHkL6mVGcefaKc3vi9z'), ('Safe And Sound', 'spotify:track:6Z8R6UsFuGXGtiIxiD8ISb'),
        ('Make It Look Easy', 'spotify:track:2g6WCOlZS7mePH81Bxxa9s'), ('BOTH', 'spotify:track:7mobUfp1aL8A6CdugCMWft'), ('Friday (feat. Mufasa & Hypeman) - Dopamine Re-Edit', 'spotify:track:4cG7HUWYHBV6R6tHn1gxrl'),
        ('Roar', 'spotify:track:27tNWlhdAryQY04Gb2ZhUI'), ('MOVE YO BODY', 'spotify:track:1FKqhy26Yyu6jeCgbVJraj'),
        ('Partner for Life', 'spotify:track:1Ud6TKFPVyWIs0dmQhg5iL'), ('MURDER IN MY MIND', 'spotify:track:6v9tjIDuN0anXNoPMytvbQ'), ('Sarkar', 'spotify:track:60suOlM8VpTVITPFeqth8r'),
        ('Forever', 'spotify:track:3NZJlJemX3mzjf56MqC5ML'), ('I Want It That Way', 'spotify:track:47BBI51FKFwOMlIiX6m8ya'), ('When Love Takes Over', 'spotify:track:6Gm4p3O6RqNXmIq3u4uyLD'),
        ('House Party', 'spotify:track:1TwLKNsCnhi1HxbIi4bAW0'), ('Make Believe', 'spotify:track:1goNZsIE8w3NQOzlP40veh'), ('Dancin’ In The Country', 'spotify:track:2KtGiBi5CrX2ERPD2PAS34'),
        ('Taras - From "Munjya"', 'spotify:track:6t9KM2EQD4H2KbrTgHGYf3'), ('Perrona Parranda', 'spotify:track:3vMNxHcGK2MwkojZY7B662'), ('Wanted', 'spotify:track:0p1BcEcYVO3uk4KDf3gzkY'),
        ("TEXAS HOLD 'EM", 'spotify:track:7cPPeSxJ1VNAzUFH3Ms4Tm'), ('Follow Me - Techno Version', 'spotify:track:64CpWUCjbhFFrwcMWCAURm'), ('Man on the Moon', 'spotify:track:22UE7ARZNnAJHq1TObXLcc'),
        ('Under Control (feat. Hurts)', 'spotify:track:4J7CKHCF3mdL4diUsmW8lq'), ('Training Season', 'spotify:track:5b5cPscqVEMChvDqscVw26'), ("Let's Get Loud", 'spotify:track:62xqG5Ft00lLHmZYKEZylO'),
        ('Energy Vampires', 'spotify:track:5jCi4osOJNbYevVMSl2Lee'), ('Alright', 'spotify:track:5JlH51YDYsGj2dyEJKKjcN'), ('Anything Goes', 'spotify:track:46ZfPS5VpSQVU5gb82hg3K'),
        ('Change Partners', 'spotify:track:5LMDR9OJOVfRAB99Vr96zn')}. 
        Do NOT use any other words. Do NOT break up any words/phrases used. If you can't construct a sentence
        using ONLY the song titles we provide, try again. Otherwise, return "Couldn't generate playlist. Try modifying context or mood."
        Hype Boy MOVE YO BODY Make It Look Easy ['spotify:track:0a4MMyCrzT0En247IhqZbD', 'spotify:track:1FKqhy26Yyu6jeCgbVJraj', 'spotify:track:2g6WCOlZS7mePH81Bxxa9s']. 

    '''

    # Also return a list of tuples where for each tuple the 0th element is the song title used and the 1st element is its ID.
    task_description += '''
        Below you will find a list of words/phrases with their ID's. Your goal is to construct a sentence made from ONLY the song titles below and return the song IDs used in the final sentence as a list..
        Here is the user's context for the sentence: '''
    task_description += f"{context}. "
    task_description += "Here is a set of tuples where each tuple[0] is the song title and the tuple[1] is the song ID. "
    results = list(results)
    task_description += f"{results[:75]}. "
    task_description += '''
        Do NOT use any other words. Do NOT break up any words/phrases used. If you can't construct a sentence
        using ONLY the song titles we provide, try again. Otherwise, return "Couldn't generate playlist. Try modifying context or mood."
    '''

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": task_description},
            {"role": "user", "content": str(results)}
        ],
        temperature = 0
    )
    msg = response.choices[0].message.content
    return msg

    