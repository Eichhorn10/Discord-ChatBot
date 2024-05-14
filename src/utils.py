import discord
from ai_assistant import ChatAI
import os

async def once_done(sink: discord.sinks, channel: discord.TextChannel, vc: discord.VoiceClient, user_id: int):
  """
  It's a callback-function which gets executed as soon as the bot stops recording the user.

  Zusatzarg:
    user_id (`int`) : The users id which started the conversation.
  """

  message = None
  created_file = False
  filename = "speech.wav"
  filepath = os.path.join(os.curdir, "src", "resources", filename)

  if len(sink.audio_data) == 0:
    await channel.send("I couldn't hear you. Try the `/listen_to_me`-command again.")
    return
  for id, user_audio in sink.audio_data.items():
    # Gets just the audio from the user who executed the command
    if id == user_id:
      discordFile = discord.File(user_audio.file, filename)
      message = await channel.send("I could hear you!", file=discordFile)
      break
  if message:
    # Gets the audio file from the message
    for attachment in message.attachments:
      if attachment.filename == filename:
        await attachment.save(fp=filepath)
        created_file = True
        # Deletes the message after saving into file
        await message.delete()
        break
    if created_file:
      try:
        await channel.send("I'm trying to understand what you just said, wait a sec...")
        chatAI = ChatAI()
        # Takes the input from user and generates response
        await chatAI.chat(channel)
        vc.play(discord.FFmpegPCMAudio(chatAI.response))
        await channel.send("I answered you!")
      except Exception as e:
        print(e)
        await channel.send("Something went wrong. Try the `/listen_to_me`-command again.")