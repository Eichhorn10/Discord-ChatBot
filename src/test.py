# import openai
# import os
# import dotenv
# from elevenlabs import generate, set_api_key, save

# # dotenv.load_dotenv()
# # openai.api_key = os.getenv("OPENAI_TOKEN")
# # audio_file = open("./src/resources/speech.wav", "rb")
# # transcription = openai.Audio.transcribe("whisper-1", audio_file)
# # decoded_transcription = transcription["text"].encode("utf-8").decode("utf-8")
# # print(decoded_transcription)

# set_api_key(os.getenv("EL_TOKEN"))
# audio = generate(
#   text="Kleiner Test",
#   voice="Monte", # Gerade Patrick, später Monte
#   model="eleven_multilingual_v1"
# )
# save(audio, "./src/resources/response.mp3")

import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "resources", "speech.wav")
print(filename)