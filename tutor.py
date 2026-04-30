import asyncio      # Handles the timing for the voice engine
import os           # Used to play the audio files on your Mac
import whisper      # The 'brain' that turns your German speech into text
import ollama       # Connects to your local glm4:9b model
import edge_tts     # The high-quality German voice engine
import speech_recognition as sr  # Handles your AirPods/Microphone input

def record_test_audio():
    """Records audio from the mic and saves it to a file for verification."""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[Adjusting for background noise... please wait 1 second]")
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("[Recording started: Speak German now!]")
        try:
            # timeout: how long it waits for you to start
            # phrase_time_limit: max length of your sentence
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            with open("test_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            print("[Success: 'test_input.wav' has been created!]")
            
        except sr.WaitTimeoutError:
            print("[Error: No speech detected within 5 seconds]")
        except Exception as e:
            print(f"[Error during recording]: {e}")
            
# 1. Load the model once at the top level
print("Loading Whisper 'small' model... (this may take a moment)")
WHISPER_MODEL = whisper.load_model("small")

def transcribe_german_audio(file_path="test_input.wav"):
    """Converts the recorded wav file into German text."""
    try:
        print(f"[Transcribing {file_path}...]")
        
        # 2. The critical fix: language='de' forces German mode
        result = WHISPER_MODEL.transcribe(file_path, language="de")
        
        text = result["text"].strip()
        print(f"Whisper heard: {text}")
        return text
        
    except Exception as e:
        print(f"[Transcription Error]: {e}")
        return None
    
async def generate_speech(text):
    """Converts AI text to a neural German voice and plays it."""
    if not text:
        return
        
    try:
        # 1. Clean the text (remove characters that can break the TTS)
        clean_text = text.replace('*', '').replace('_', '').strip()
        
        # 2. Select a high-quality Neural German voice
        # 'de-DE-KatjaNeural' is clear and friendly
        communicate = edge_tts.Communicate(clean_text, "de-DE-KatjaNeural")
        await communicate.save("response.mp3")
        
        # 3. Play the file using Mac's native player
        print("[Playing AI Response...]")
        os.system("afplay response.mp3")
        
    except Exception as e:
        print(f"[TTS Error]: {e}")
        
async def generate_speech(text):
    """Converts input text to a neural German voice and plays it."""
    try:
        # Clean text for the neural engine
        clean_text = text.replace('*', '').replace('_', '').strip()
        
        # We will use 'de-DE-KillianNeural' for a clear male voice 
        # or 'de-DE-KatjaNeural' for a clear female voice.
        communicate = edge_tts.Communicate(clean_text, "de-DE-KatjaNeural")
        
        print(f"[Generating voice for: {clean_text}]")
        await communicate.save("response.mp3")
        
        # Play using Mac's native 'afplay'
        os.system("afplay response.mp3")
        
    except Exception as e:
        print(f"[TTS Error]: {e}")
        
def get_ai_response(user_text):
    """Sends text to Ollama and returns the German response."""
    try:
        print(f"[Ollama is thinking...]")
        
        # This connects to your 'ollama serve' running in the other terminal
        response = ollama.chat(model='glm4:9b', messages=[
            {
                'role': 'system', 
                'content': 'You are a friendly German tutor. Respond ONLY in simple German. Keep your answers brief (1-2 sentences) so they are easy to listen to.'
            },
            {
                'role': 'user', 
                'content': user_text
            },
        ])
        
        reply = response['message']['content']
        return reply
        
    except Exception as e:
        print(f"[Ollama Error]: {e}")
        return "Entschuldigung, ich habe einen Fehler gemacht." # "Sorry, I made a mistake"

if __name__ == "__main__":
    # 1. Record your voice
    record_test_audio()
    
    # 2. Transcribe it to German text
    transcribed_text = transcribe_german_audio()
    
    if transcribed_text:
        print(f"You said: {transcribed_text}")
        
        # 3. Get the AI's thoughts
        ai_reply = get_ai_response(transcribed_text)
        print(f"AI replied: {ai_reply}")
        
        # 4. Speak the AI's thoughts
        if ai_reply:
            asyncio.run(generate_speech(ai_reply))
