import os
import openai
import discord
from elevenlabs import generate, save, set_api_key

class ChatGPT:
  def __init__(self):
    '''
    Initialize the GPT model
    '''

    # All path variables
    self.conversation = os.path.join(os.curdir, "src", "resources", "conversation.txt") # The conversation file is used to store the conversation history between the bot and the user
    self.personality = os.path.join(os.curdir, "src", "resources", "personality.txt") # The personality file is used to store the personality (prompt) that the bot has to use to chat with the user
    self.speech = os.path.join(os.curdir, "src", "resources", "speech.wav") # The speech file is used to store the user's audio input # "large" for using non-english languages
    self.response = os.path.join(os.curdir, "src", "resources", "response.mp3") # The response file is used to store the bot's response

    # Openai Set-up
    openai.api_key = os.getenv("OPENAI_TOKEN")
    self.gptmodel = "gpt-3.5-turbo"

    # Set-up the system of chatGPT
    with open(self.personality, "r") as f:
      self.prompt = f.read()

    if os.path.exists(self.conversation): # If it's not the beginning of the conversation
      with open(self.conversation, "r") as f:
        self.prompt = f"{self.prompt}\nCurrent conversation:{f.read()}"

    self.messages = [
      {"role": "system", "content": self.prompt}
    ]


  async def chat(self, channel: discord.TextChannel):
    '''
    Starts the conversation with the user.

    Arg:
      channel (`discord.TextChannel`) : The text channel where the command was executed.

    Returns:
      `AudioSource`: The audio source of the bot's response.
    '''

    user_input = self.__start_conversation()
    self.messages.append({"role": "user", "content": user_input})
    await channel.send("I could understand you! Trying to answer...")
    response = self.__get_response()

    # Update the conversation history
    with open(self.conversation, "a", encoding="utf-8") as f:
      f.write(f"\nUser: {user_input}\nMonte: {response}")

    await channel.send("Generating voice...")
    await self.__generate_voice(response)


  def __start_conversation(self) -> str:
    '''
    Gets the user's audio input and returns it as string.
    '''

    print("Transcribing...")
    transcription = openai.Audio.transcribe("whisper-1", open(self.speech, "rb"))
    print("Done transcribing.")
    return transcription["text"].encode("utf-8").decode("utf-8")  # Needs to be encoded and decoded to add the umlauts


  def __get_response(self) -> str:
    '''
    Gets the response from the GPT model.
    '''

    print("Start completion from ChatGPT...")
    completion = openai.ChatCompletion.create(
      model=self.gptmodel,
      messages=self.messages,
      temperature=0.8,
      max_tokens=200
    )
    print("Done completion.")
    answer = completion.choices[0].message.content
    return answer.encode("utf-8").decode("utf-8") # Needs to be encoded and decoded to add the umlauts


  async def __generate_voice(self, text: str):
    '''
    Generates the response audio from the text.
    '''

    set_api_key(os.getenv("EL_TOKEN"))
    audio = generate(
      text=text,
      voice="Monte",
      model="eleven_multilingual_v1"
    )
    save(audio, self.response)
    print("Done generating audio.")