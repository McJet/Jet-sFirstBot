import discord
import os
import requests
import json
import random

# gets a quote from zen quotes api - https://zenquotes.io/
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    joke = json_data[0]['q'] + "\n- " + json_data[0]['a']
    return joke


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

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragement))

client.run(os.environ['TOKEN'])  # runs the bot
