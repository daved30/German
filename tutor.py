import asyncio
import os
from utils.record_audio import record_audio
from utils.transcribe_german import transcribe_german
from utils.get_ai_response import get_ai_response
from utils.translate_text import translate_text
from utils.generate_speech import generate_speech

ollama_model = os.getenv("OLLAMA_MODEL", "glm4:9b")


async def conversation_loop():
    print("--- German Tutor: V2 Seamless Mode ---")

    while True:
        try:
            # 1. Ear (RAM-based)
            audio_ram = record_audio()
            if not audio_ram:
                continue

            # 2. Transcribe (RAM-based)
            de_text = transcribe_german(audio_ram)
            if not de_text or len(de_text) < 2:
                continue

            # Translate YOUR speech immediately
            user_en = translate_text(ollama_model, de_text)
            print(f"\nYOU (DE): {de_text}")
            print(f"YOU (EN): {user_en}")

            # 3. Brain (Streaming Tokens)
            print("AI (DE): ", end="", flush=True)

            full_reply_de = ""
            # We loop through the generator tokens
            for token in get_ai_response(ollama_model, de_text):
                print(token, end="", flush=True)  # Words appear live!
                full_reply_de += token

            # 4. Translation & Voice (Sequential for now)
            # Once the stream finishes, we handle the translation and voice
            ai_en = translate_text(ollama_model, full_reply_de)
            print(f"\nAI (EN): {ai_en}")

            await generate_speech(full_reply_de)

            input("\n--- Press Enter to speak again ---")

        except KeyboardInterrupt:
            print("\nBis bald!")
            break


if __name__ == "__main__":
    asyncio.run(conversation_loop())
