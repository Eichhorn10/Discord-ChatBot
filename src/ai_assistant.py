import os
from openai import OpenAI
import discord
from elevenlabs import save, Voice
from elevenlabs.client import ElevenLabs

class ChatAI:
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
    self.gpt_client = OpenAI(api_key=os.getenv("OPENAI_TOKEN"))
    self.gpt_model = "gpt-3.5-turbo"

    self.wh_model = "whisper-1"

    self.tts_model = "tts-1"
    self.tts_voice = "onyx"

    # ElevenLabs Set-up
    self.el_client = None
    el_api_key = os.getenv("EL_TOKEN")

    if el_api_key: # If the Elevenlabs API key is provided
      self.el_client = ElevenLabs(api_key=el_api_key)
      self.el_voice = Voice(voice_id=os.getenv("EL_VOICE_ID"))
      self.el_model = "eleven_multilingual_v2"

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
      f.write(f"\nUser: {user_input}\nBot: {response}")

    await channel.send("Generating voice...")
    await self.__generate_voice(response)


  def __start_conversation(self) -> str:
    '''
    Gets the user's audio input and returns it as string.
    '''

    print("Transcribing...")
    transcription = self.gpt_client.audio.transcriptions.create(
      model=self.wh_model, file=open(self.speech, "rb"))
    print("Done transcribing.")
    return transcription["text"].encode("utf-8").decode("utf-8")  # Needs to be encoded and decoded to add the umlauts


  def __get_response(self) -> str:
    '''
    Gets the response from the GPT model.
    '''

    print("Start completion from ChatGPT...")
    completion = self.gpt_client.chat.completions.create(
      model=self.gpt_model,
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
    if self.el_client:
      audio = self.el_client.generate(
        text=text,
        voice=self.el_voice,
        model=self.el_model
      )
      save(audio, self.response)
    else: # Uses OpenAI's TTS when the Elevenlabs API key is not provided
      audio = self.gpt_client.audio.speech.with_streaming_response.create(
        model=self.tts_model,
        voice=self.tts_voice,
        input=text
      )
      audio.stream_to_file(self.response)
    print("Done generating audio.")