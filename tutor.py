import ollama
import os
from whisper_mic import WhisperMic

# english=False forces it to look for German; model="base" is fast on M5
mic = WhisperMic(model="base", english=False)

def chat():
    print("--- German Tutor Active (Press Ctrl+C to stop) ---")
    print("Tip: Speak clearly in German or English.")
    
    while True:
        try:
            print("\n[Listening... Speak now]")
            # Forces the engine to interpret speech as German
            user_text = mic.listen() 
            print(f"You said: {user_text}")

            if not user_text or len(user_text.strip()) < 2:
                continue

            # Send to your local Ollama instance
            response = ollama.chat(model='glm4:9b', messages=[
                {'role': 'system', 'content': 'You are a patient German tutor. Respond in simple German and provide an English translation in brackets.'},
                {'role': 'user', 'content': user_text},
            ])

            reply = response['message']['content']
            print(f"AI: {reply}")

            # Speak the German part using Mac's native 'Anna'
            # Strip the English bracketed part so the Mac only speaks German
            speech_text = reply.split('[')[0].strip().replace('"', '').replace("'", "")

            os.system(f'say -v Anna -r 160 "{speech_text}"')

        except KeyboardInterrupt:
            print("\nBis bald! (Closing...)")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat()