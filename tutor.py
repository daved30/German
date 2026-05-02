import asyncio
import os
from utils.record_audio import record_audio
from utils.transcribe_german import transcribe_german
from utils.get_ai_response import get_ai_response
from utils.translate_text import translate_text
from utils.generate_speech import generate_speech

ollama_model = os.getenv("OLLAMA_MODEL", "glm4:9b")

async def conversation_loop():
    print("--- German Tutor: Modular Mode ---")
    
    while True:
        try:
            # 1. Ear
            if not record_audio(): continue
            
            # 2. Transcribe
            de_text = transcribe_german()
            if not de_text or len(de_text) < 2: continue
            
            # 3. Process & Translate
            user_en = translate_text(ollama_model, de_text)
            print(f"\nYOU (DE): {de_text}")
            print(f"YOU (EN): {user_en}")

            ai_de = get_ai_response(ollama_model, de_text)
            ai_en = translate_text(ollama_model, ai_de)
            
            print(f"AI (DE): {ai_de}")
            print(f"AI (EN): {ai_en}")

            # 4. Voice
            await generate_speech(ai_de)
            
            input("\n--- Press Enter to speak again ---")

        except KeyboardInterrupt:
            print("\nBis bald!")
            break

if __name__ == "__main__":
    asyncio.run(conversation_loop())
