import asyncio
import os
import pygame
import warnings
from asyncio import Queue
from utils.record_audio import record_audio
from utils.transcribe_german import transcribe_german
from utils.get_ai_response import get_ai_response
from utils.translate_text import translate_text
from utils.generate_speech import generate_speech

# 1. Setup
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
ollama_model = os.getenv("OLLAMA_MODEL", "glm4:9b")
pygame.mixer.init()


async def ainput(prompt: str) -> str:
    """Non-blocking input for async loops."""
    return await asyncio.to_thread(input, prompt)


async def audio_player(queue):
    """Background task: Plays audio files from the queue in strict order."""
    while True:
        filename = await queue.get()
        if filename is None:
            break

        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"[Player Error]: {e}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            queue.task_done()


async def conversation_loop():
    print("--- German Tutor: V2 Seamless (Fixed Order) ---")
    audio_queue = Queue()
    player_task = asyncio.create_task(audio_player(audio_queue))

    while True:
        try:
            # 1. Ear & Transcribe
            audio_ram = record_audio()
            if not audio_ram:
                continue

            de_text = transcribe_german(audio_ram)
            if not de_text or len(de_text) < 2:
                continue

            print(f"\nYOU (DE): {de_text}")
            print("AI (DE): ", end="", flush=True)

            # 2. Streaming Response + Ordered Queuing
            full_reply_de = ""
            sentence_buffer = ""

            for token in get_ai_response(ollama_model, de_text):
                print(token, end="", flush=True)
                full_reply_de += token
                sentence_buffer += token

                # If sentence ends, generate and enqueue immediately
                if any(p in token for p in ['.', '!', '?']):
                    text_to_speak = sentence_buffer.strip()
                    sentence_buffer = ""
                    # This 'await' ensures Sentence 1 is ready before Sentence 2 starts
                    fname = await generate_speech(text_to_speak)
                    if fname:
                        await audio_queue.put(fname)

            # Handle any leftover text without punctuation
            if sentence_buffer.strip():
                fname = await generate_speech(sentence_buffer.strip())
                if fname:
                    await audio_queue.put(fname)

            # 3. Wait for Katja to finish talking
            await audio_queue.join()

            # 4. Translations
            ai_en = translate_text(ollama_model, full_reply_de)
            print(f"\nAI (EN): {ai_en}")

            await ainput("\n--- Press Enter to speak again ---")

        except KeyboardInterrupt:
            player_task.cancel()
            print("\nBis bald!")
            break

if __name__ == "__main__":
    asyncio.run(conversation_loop())
