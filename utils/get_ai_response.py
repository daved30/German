import ollama


def get_ai_response(model, user_text):
    """Sends text to Ollama and returns the German response."""
    try:
        print(f"[Ollama is thinking...]")
        response = ollama.chat(model=model, messages=[
            {
                'role': 'system',
                'content': 'You are a friendly German tutor. Respond ONLY in simple German. Keep your answers brief (1-2 sentences).'
            },
            {
                'role': 'user',
                'content': user_text
            },
        ])
        return response['message']['content']
    except Exception as e:
        print(f"[Ollama Error]: {e}")
        return "Entschuldigung, ich habe einen Fehler gemacht."
