import discord
import openai
import os
from io import BytesIO
import requests
from discord.ext import commands

tkn = os.environ.get('bot_token')
openai.api_key = os.environ.get('openai_key')
client = discord.Client(intents=discord.Intents.all())

def process_command(content):
    '''
    Processes user commands that begin with "!afd"

    Args: 
        message.content (str): full command

    Returns:
        ret (list): ret[0] == 0: no prompt, message ret[1]
                    ret[0] == 1: has prompt, prompt ret[1]
                    ret[0] == 2: has image, image ret[1]
        
    '''
    command = content.lstrip("!afd ")
    ret = [0]

    if command in ("help", "?"):
        ret.append("Apollo DALL-E Commands (!afd [command]):\n\t\"gen-u\" : Generates a unique image using an AI generated prompt\
            \n\t\"gen-p [prompt]\" : Creates an image based on an entered prompt.\
                \n\tcaption [image]: Generates a caption for an image.")

    elif command == "gen-u": # generate random art image - returns a unique prompt
        ret[0] = 1
        ret.append(openai.Completion.create(model="text-davinci-003", prompt="Generate a short, extremely unique and creative image caption \
            that doubles as a DALLE prompt", temperature=1.0, max_tokens=100).choices[0].text)

    elif command.startswith("gen-p"): # generate img based on prompt - returns user prompt
        ret[0] = 1
        ret.append(command.lstrip("gen-p "))
        
    elif command.startswith("caption"):
        
      
    else: # command not recognized
        ret.append("Sorry, I couldn't recognize your command. Please check your message or enter \"!afd help\" for a list of all commands.")
    
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
        response_format="url"
        )
    
    image_url = response['data'][0]["url"]
    image_data = requests.get(image_url).content
    image = discord.File(BytesIO(image_data), filename='image.jpg')
    return image
j

def get_caption(image_url):
    '''
    Generates a caption for an image
    
    '''
    response = openai.Completion.create(
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
    if message.content.startswith("!afd"): # command listener
        ret = process_command(message.content)
        if ret[0] == 0:
            await message.channel.send(ret[1])
        else:
            image = get_image(ret[1])
            await message.channel.send(ret[1],file=image)


client.run(tkn)
