import discord
import openai
from discord.ext import commands

tkn = "token"
openai.api_key = "key"
client = discord.Client(intents=discord.Intents.all())
commands = {
    "help": "shows all commands",
    "gu" : "generates unique image with GPT based prompt",
    "gp [prompt]" : "generates image based on user prompt" 
}

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
            await message.channel.send(image)


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

    if command == "help" or "?":
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

client.run(tkn)
