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

client = discord.Client()  # create an instance of a client; the connection to discord

@client.event  # register an event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message): # triggers every time a message is recieved
    if message.author == client.user:  # ignores if message is from itself
        return

    if message.content.startswith('$inspire'): 
        quote = get_quote()
        await message.channel.send(quote)

client.run(os.environ['TOKEN'])  # runs the bot
