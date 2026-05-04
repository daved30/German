import ollama


def translate_text(model, german_text):
    """Translates German text to English using Ollama."""
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'system',
                'content': 'Translate the following German text into English. Provide ONLY the translation.'
            },
            {'role': 'user', 'content': german_text},
        ])
        return response['message']['content'].strip()
    except Exception as e:
        print(f"[Translation Error]: {e}")
        return "[Translation Error]"
