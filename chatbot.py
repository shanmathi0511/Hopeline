import requests

API_KEY = "gsk_dummy_key_1234567890abcdef"
API_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_response(query):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful legal assistant named HopeLine. Keep answers short, clear, and professional. If the query is legal-related, give a concise explanation."},
                {"role": "user", "content": query}
            ],
            "temperature": 0.5
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            return reply.strip()
        else:
            return f"❌ API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"⚠️ Exception: {str(e)}"
