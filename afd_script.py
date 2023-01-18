import discord
import json
import openai
import os
from io import BytesIO
import requests
from discord.ext import commands

with open("config.json") as json_file:
    data = json.load(json_file)

tkn = data["token"]
openai.api_key = data["key"]

client = discord.Client(intents=discord.Intents.all())

def process_command(message):
    '''
    Processes user commands that begin with "!d"

    Args: 
        message.content (str): full command

    Returns:
        ret (list): ret[0] == 0: no prompt, message ret[1]
                    ret[0] == 1: has prompt, prompt ret[1]
                    ret[0] == 2: has image, image ret[1]
        
    '''
    content = message.content
    command = content.lstrip("!d ")
    ret = [0]

    if command in ("help", "?"):
        # ret.append(EMBED)
        embed = discord.Embed(title="Commands",
        color=0xeee657)
        commands = [("!d help", "Displays all my secrets"), ("!d gen-p [prompt]",
            "Generates an image based on prompt input (check !d rules) for guidelines"),
            ("!d gen-u", "Generates a special image just for your mom."),
            ("!d caption [image]", "Generates a caption for your oh-so-precious picture.")]
        for name, value in commands:
            embed.add_field(name=name, value=value, inline=False)
        ret.append(embed)


    elif command == "gen-u": # generate random art image - returns a unique prompt
        ret[0] = 1
        ret.append(openai.Completion.create(model="text-davinci-003", prompt="Generate a short, extremely unique and creative image \
            generation prompt", temperature=0.5, max_tokens=100).choices[0].text)

    elif command.startswith("gen-p"): # generate img based on prompt - returns user prompt
        ret[0] = 1
        ret.append(command.lstrip("gen-p "))
        
    elif command.startswith("caption"):
        ret[0] = 2
        image_url = message.attachments[0].url
        ret.append(image_url)
      
    else: # command not recognized
        ret.append("Sorry, I couldn't recognize your command. Please check your message or enter \"!d help\" for a list of all commands.")
    
    return ret


def get_image(prompt):
    '''
    Prompts GPT for an image

    Args:
        prompt (str): image generation prompt

    Returns:
        image (discord.File): the image file
    '''
    
    response = openai.Image.create(
        prompt=prompt,
        size="1024x1024", 
        response_format="url",
        )
    
    image_url = response['data'][0]["url"]

    return image_url


def get_caption(image_url):
    '''
    Generates a caption for an image

    Args:
        image_url (str): Discord URL for image
    
    Returns:
        caption (str): Caption for image
    
    '''

    response = openai.Completion.create(
        model = "text-davinci-002",
        prompt=("Generate a caption for this image" + image_url),
        temperature=0.5,
        max_tokens = 100
    )
    caption = response.choices[0].text
    return caption


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("AFD LIVE")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!d"): # command listener
        ret = process_command(message)
        ###
        if ret[0] == 0:
            await message.channel.send(embed=ret[1])
        elif ret[0] == 2:
            await message.channel.send(get_caption(ret[1]))
        else:
            image_url = get_image(ret[1])
            image_data = requests.get(image_url).content
            image = discord.File(BytesIO(image_data), filename='image.jpg')
            await message.channel.send(get_caption(image_url),file=image)


client.run(tkn)
