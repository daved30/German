import asyncio
import os
import whisper
import ollama
import edge_tts
import speech_recognition as sr
import warnings

# Suppress the FP16 CPU warning for a cleaner terminal
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# --- Configuration ---
MODEL_NAME = "llama3.1:8b"
WHISPER_SIZE = "medium"  # You can change this to "medium" if you want higher accuracy
VOICE_NAME = "de-DE-KatjaNeural"

# --- Initialization ---
print(f"Loading Whisper '{WHISPER_SIZE}' model...")
WHISPER_MODEL = whisper.load_model(WHISPER_SIZE)


def record_audio(filename="test_input.wav"):
    """Records audio from the mic and saves to a local file."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Adjusting for noise...]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("[Listening... Speak German now]")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            return True
        except sr.WaitTimeoutError:
            print("[Error: No speech detected]")
            return False


def transcribe_german(file_path="test_input.wav"):
    """Transcribes audio file to text, forced to German."""
    try:
        # Forced language 'de' prevents the Arabic/English hallucinations
        result = WHISPER_MODEL.transcribe(file_path, language="de")
        return result["text"].strip()
    except Exception as e:
        print(f"[Transcription Error]: {e}")
        return None


def ollama_call(text, system_prompt):
    """Generic helper for Ollama requests (Chat or Translation)."""
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': text}
        ])
        return response['message']['content'].strip()
    except Exception as e:
        print(f"[Ollama Error]: {e}")
        return None


async def play_voice(text):
    """Converts text to speech and plays it locally."""
    if not text:
        return
    try:
        # Clean text of emojis and markdown for the TTS engine
        clean_text = text.encode('ascii', 'ignore').decode(
            'ascii').replace('*', '').strip()

        communicate = edge_tts.Communicate(clean_text, VOICE_NAME)
        await communicate.save("response.mp3")

        print(f"[Playing AI Voice...]")
        os.system("afplay response.mp3")
    except Exception as e:
        print(f"[TTS Error]: {e}")


async def conversation_loop():
    print("--- German Tutor Ready ---")

    while True:
        try:
            # 1. Capture speech
            if not record_audio():
                continue

            # 2. Convert sound to German text
            de_text = transcribe_german()
            if not de_text or len(de_text) < 2:
                continue

            # 3. Handle Translation & AI in parallel (Visual Logic)
            # You see your translation while the AI is "thinking"
            en_translation = ollama_call(
                de_text, "Translate this German to English. Only the translation.")
            print(f"\nYOU (DE): {de_text}")
            print(f"YOU (EN): {en_translation}")

            # 4. Get the AI's German response
            ai_reply_de = ollama_call(
                de_text, "You are a friendly German tutor. Simple German only. 1-2 sentences.")
            if ai_reply_de:
                # 5. Translate AI response and Speak
                ai_reply_en = ollama_call(
                    ai_reply_de, "Translate this German to English. Only the translation.")
                print(f"AI (DE): {ai_reply_de}")
                print(f"AI (EN): {ai_reply_en}")

                await play_voice(ai_reply_de)

            input("\n--- Press Enter to speak again ---")

        except KeyboardInterrupt:
            print("\nBis bald!")
            break

if __name__ == "__main__":
    asyncio.run(conversation_loop())
