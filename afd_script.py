import discord
import openai
from io import BytesIO
import requests
from discord.ext import commands

tkn = "tkn"
openai.api_key = "key"
client = discord.Client(intents=discord.Intents.all())
commands = {
    "help": "shows all commands",
    "gu" : "generates unique image with GPT based prompt",
    "gp [prompt]" : "generates image based on user prompt" 
}

def process_command(content):
    '''
    Processes user commands that begin with "!afd"

    Args: 
        message.content (str): full command

    Returns:
        ret (list): ret[0] == 0: no prompt, message ret[1]
                    ret[0] ==1: has prompt, prompt ret[1]
        
    '''
    command = content.lstrip("!afd ")
    ret = [0]

    if command in ("help", "?"):
        ret.append("Apollo DALL-E Commands (!afd [command]):")

    elif command == "gu": # generate random art image - returns a unique prompt
        ret[0] = 1
        ret.append(openai.Prompt.create(model="text-davinci-002", temperature=1.0).choices[0].text)

    elif command.startswith("gp"): # generate img based on prompt - returns user prompt
        ret[0] = 1
        ret.append(command.lstrip("gp "))
        
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

    
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("AFD has connected to Discord")


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
