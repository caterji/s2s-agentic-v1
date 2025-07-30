import os
import subprocess
import json

# Uncomment if you want to use OpenAI
try:
    import openai
except ImportError:
    openai = None

# Old Ollama function (commented out for reference)
# def call_ollama(prompt, model='mistral'):
#     """
#     Calls Ollama with a prompt and returns the generated text.
#     Assumes Ollama is already running locally.
#     """
#     try:
#         result = subprocess.run(
#             ["ollama", "run", model],
#             input=prompt.encode('utf-8'),
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             timeout=60
#         )
#
#         output = result.stdout.decode('utf-8')
#         return output.strip()
#
#     except Exception as e:
#         return f"Error: {str(e)}"

def call_llm(prompt, backend='ollama', model=None):
    """
    Calls either Ollama or OpenAI with a prompt and returns the generated text.
    backend: 'ollama' or 'openai'
    model: model name for the backend (default: 'mistral' for ollama, 'gpt-3.5-turbo' for openai)
    """
    if backend == 'ollama':
        if model is None:
            model = 'mistral'
        try:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )
            output = result.stdout.decode('utf-8')
            return output.strip()
        except Exception as e:
            return f"Ollama Error: {str(e)}"
    elif backend == 'openai':
        if openai is None:
            return "OpenAI package not installed. Run 'pip install openai' to use this backend."
        if model is None:
            model = 'gpt-3.5-turbo'
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Error: OPENAI_API_KEY environment variable not set."
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            if content is not None:
                return content.strip()
            else:
                return "OpenAI Error: No content in response."
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    else:
        return "Invalid backend specified. Use 'ollama' or 'openai'."