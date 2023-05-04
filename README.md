## Discord AI Art Bot

This is a Discord bot that generates art using OpenAI's GPT-3 API. 

### Features

- Generate art based on user input prompt.
- Generate a unique prompt to generate art.
- Get help using the `!help` command.


### Technologies Used

- `discord` and `discord.ext` packages to interact with the Discord API
- `json` package to load and parse a configuration file containing bot credentials.
- `openai` package to interact with the GPT-3 API
- `os` package to handle environmental variables containing bot credentials
- `requests` package to download the generated image
- `BytesIO` package to handle the image in memory

### Installation

To install and run the bot, follow these steps:

1. Clone the repository and navigate to the project directory.
2. Install the dependencies by running `pip install -r requirements.txt`.
3. Create a configuration file named `config.json` in the root directory. The file should contain the following:

```
{
"token": "your_bot_token_here",
"key": "your_openai_api_key_here"
}
```


4. Replace `your_bot_token_here` with your bot's Discord token and `your_openai_api_key_here` with your OpenAI API key.
5. Run the bot by running `python main.py`.

### Usage

Once the bot is running, you can interact with it on Discord by typing a command starting with `!`.

#### Commands

- `!gen-p [prompt]`: Generates an image based on the provided prompt. Replace `[prompt]` with your prompt text.
- `!gen-u`: Generates a unique prompt to generate art.
- `!help`: Displays a list of available commands and their descriptions.

### Contributing

If you'd like to contribute to this project, feel free to submit a pull request.

### License

This project is licensed under the MIT License.
