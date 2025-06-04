import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import os
import json
from datetime import datetime

DURATION = 10
SAMPLE_RATE = 44100
AUDIO_DIR = "audio_files"
OUTPUT_DIR = "outputs"
AUDIO_FILENAME = "audio.wav"
JSON_FILENAME = "transcription.json"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

audio_path = os.path.join(AUDIO_DIR, AUDIO_FILENAME)
json_path = os.path.join(OUTPUT_DIR, JSON_FILENAME)

print(f"\nRecording for {DURATION} seconds... Speak now!")
audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
sd.wait()
write(audio_path, SAMPLE_RATE, audio_data)
print(f"Audio saved to: {audio_path}")

recognizer = sr.Recognizer()
with sr.AudioFile(audio_path) as source:
    recorded_audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(recorded_audio)
    print(" Transcribed Text:", text)
except sr.UnknownValueError:
    text = "[Unrecognized speech]"
    print(" Could not understand the audio.")
except sr.RequestError:
    text = "[Google API unavailable]"
    print(" Could not request transcription from Google API.")

output = {
    "timestamp": datetime.now().isoformat(),
    "audio_file": audio_path,
    "transcription": text
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print(f" Transcription saved to: {json_path}")