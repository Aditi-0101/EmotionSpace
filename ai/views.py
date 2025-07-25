from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
# Create your views here.

@login_required
def ask_ai(request):
    if request.method == "POST":
        query = request.POST.get("query")
        response = generate_response(query)
        
        parameters = {
            "query": query,
            "response" : response
        }

        return render(request, "ai/ask_ai.html", parameters)
    return render(request, "ai/ask_ai.html")

def generate_response(query):

    prompt = (
        "You are EmotionSpace, a gentle and emotionally supportive AI companion. "
    "Your role is to make users feel safe, heard, and validated. "
    "If someone simply greets you (e.g., says 'hi', 'hey', or 'hello'), respond casually with warmth and friendliness. "
    "If someone shares personal emotions or thoughts, respond with empathy, comfort, and gentle reflection. "
    "You are not a therapist and do not give medical advice. Always speak like a trusted friend who is here to listen and care. "
    "Respond appropriately to the message below:" + query
    )

    api = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"


    payload = {
        "contents": [
            {"parts": [
                {"text": prompt}
            ]}
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api, json=payload, headers=headers)

    print(response.status_code)

    data = response.json()
    response_text = data["candidates"][0]["content"]["parts"][0]["text"]

    return response_text