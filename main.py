import discord
import os
import requests
import json
import random
from replit import db


# gets a quote from zen quotes api - https://zenquotes.io/
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    joke = json_data[0]['q'] + "\n- " + json_data[0]['a']
    return joke

def update_encouragements(encouragementMsg):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouragementMsg)
        db["encouragement"] = encouragements
    else:
        db["encouragements"] = [encouragementMsg]

def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
starter_encouragement = [
    "Cheer up!",
    "You got this!",
    "You are a great person!"
]
client = discord.Client()  # create an instance of a client; the connection to discord


@client.event  # register an event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message): # triggers every time a message is recieved
    msg = message.content
    if message.author == client.user:  # ignores if message is from itself
        return

    if msg.startswith('$inspire'): 
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragement
    if "encouragements" in db.keys():
        options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouragingMsg = msg.split("$new ", 1) [1]
        update_encouragements(encouragingMsg)
        await message.channel.send("New encouragement added.")
    
    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del ", 1) [1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

        update_encouragements(encouragingMsg)
        await message.channel.send("New encouragement added.")
    
    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

client.run(os.environ['TOKEN'])  # runs the bot
