import discord
import dotenv
import os
import utils
import asyncio

# Permissions
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = discord.Bot(intents=intents)

guilds = [] # Will be the cache for all connected guilds
connections = {}  # Will be the cache for all connected voice channels
dotenv.load_dotenv()  # Loads all Variables in .env
isRecording = False

# Events
@bot.event
async def on_ready():
  print("Bot is now running!")

@bot.event
async def on_voice_state_update(member, before, after):
  global connections
  global guilds
  global isRecording
  files = [
    "./src/resources/conversation.txt", 
    "./src/resources/response.mp3", 
    "./src/resources/speech.wav"
  ]

  if member.id != bot.user.id:
    return
  # When the bot disconnects from a voice channel
  if before.channel and not after.channel:
    # Deletes the complete conversation
    for file in files:
      if os.path.exists(file):
        os.remove(file)
    del connections[before.channel.id]  # Deletes the voice channel from the cache
    guilds.remove(before.channel.guild.id)  # Deletes the guild from the cache
    isRecording = False

# Commands
@bot.command(name="listen_to_me", description="Starts a conversation with the bot (don't forget to stop the listening with `/stop_listening`)")
async def chat_with_me(ctx):
  global connections
  global guilds
  global isRecording
  user_vstate = ctx.user.voice
  user_mention = ctx.user.mention

  if not isRecording:
    if not user_vstate:
      await ctx.respond(f"{user_mention}, you currently aren't in a voice channel!")
      return
    if user_vstate.channel.id in connections:
      vc = connections[user_vstate.channel.id]
    else:
      vc = await user_vstate.channel.connect()
      connections.update({user_vstate.channel.id: vc})  # Updating the cache with the voice channel
      guilds.append(ctx.guild.id)  # Updating the cache with the guild

    try:
      # Starts the listening
      vc.start_recording(
        discord.sinks.WaveSink(),
        utils.once_done,  # After '/stop_listening' got executed this callback will be executed
        ctx.channel,
        vc,
        ctx.user.id
      )
      isRecording = True
      await ctx.respond(f"I'm listening to you {user_mention}!")
    except Exception as e:
      print(e)
  else:
    await ctx.respond("I'm already listening to someone!")

@bot.command(name="stop_listening", description="The bot stops listening to you and starts generating a response")
async def stop_recording(ctx):
  global connections
  global isRecording
  user_vc = ctx.user.voice.channel

  if isRecording:
    if user_vc.id in connections:
      vc = connections[user_vc.id]
      vc.stop_recording()
      await ctx.delete()
      isRecording = False
    else:
      await ctx.respond("I'm currently not connected to the same voice channel as you!")
  else:
    await ctx.respond("I'm currently not listening to anyone!")

@bot.command(name="leave", description="The bot leaves the currently connected voice channel")
async def leave(ctx):
  global guilds

  if ctx.guild.id in guilds:
    bot_vc = ctx.guild.voice_client
    await bot_vc.disconnect()
    await ctx.respond("I'm out!")
  else:
    await ctx.respond("I'm currently not connected to a voice channel!")

async def main():
  bot.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
  asyncio.run(main())
