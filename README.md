# ChatBot
It's a Discord bot that you can talk to if you are bored.

## Usage
You will be able to configure the personality of the bot by editing the file `/src/resources/personality.txt`.\
After setting his personality you can use these **commands** to start a conversation with the bot: 
#### /listen_to_me
The bot starts to listen to you.

#### /stop_listening
The bot stops listening to you and starts generating a response.\
It needs to be called after the `/listen_to_me`-command.

#### /leave
The bot leaves the current voice channel.\
It needs to be called after you finished using him.

## Requirements
- At least [Python](https://www.python.org/downloads/) v1.10
- FFmpeg (with winget: `winget install id=Gyan.FFmpeg -e` or [manually](https://www.youtube.com/watch?v=jZLqNocSQDM))
- [OpenAI](https://platform.openai.com/docs/overview) account and an API-Key ([How to create an OpenAI API Key](https://www.youtube.com/watch?v=nafDyRsVnXU))
- [Discord](https://discord.com/) account
- [Elevenlabs](https://elevenlabs.io/) account (_optional_)

## Installation
1. Create a Discord app on https://discord.com/developers.
1. Generate an OAuth2 URL in the OAuth2 section by selecting the scope `bot`. Now scroll down to the generated URL and copy it.
1. Now you have to configure the URL manually by changing the `permissions=`-section (there should be a **0** by default) to **35190851313408**.
1. Git clone the project: `git clone git@github.com:Eichhorn10/ChatBot.git`.
1. Start your CMD, go to the project folder and install the needed libraries by typing `pip install -r requirements.txt`.
1. Create a file into the project folder and name it `.env`.
1. Open and paste your API-Keys/Tokens into it. In the `.env.example`-file is descripted how to paste them.
1. (_optional_) If you want to use Elevenlabs for specific voices for your bot, you will need to copy the voice-ID of your specific voice. You can get it by pressing the ID-icon in the top right corner of the voice in the VoiceLab section.
1. Start the `bot.py`-script which is located in the `/src`-folder.

## Maybe also interesting
- [How To Host Your Bot Online 24/7](https://www.youtube.com/watch?v=2TI-tCVhe9k)

## Comment
Hey, this is my first real project, so there might be a few mistakes here and there with the script 😅. If you notice anything, feel free to report the error to me.\
Still, I hope you can find some use for it 🙂.
