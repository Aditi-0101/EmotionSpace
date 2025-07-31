from django.shortcuts import render, redirect
from .models import Journal
from django.contrib.auth.decorators import login_required
from dashboard.models import Activity
from django.utils import timezone
import requests
import json
from django.urls import reverse
# Create your views here.


api_key="AIzaSyBSE3-kehpQQkPge64skKx8HB2AJI4EgF0"

def generate_response(entry_text):
    
    print("--- Attempting to generate AI response ---")


    prompt = (
        "You are an expert sentiment-analysis AI. Analyze the following journal entry and "
        "provide a structured JSON response. The JSON object must contain: "
        "1. An 'insight' key with a gentle, one-sentence reflection on the user's feelings. "
        "2. A 'joy' key with a percentage (0-100) of joy detected. "
        "3. A 'sadness' key with a percentage (0-100) of sadness detected. "
        "4. A 'neutral' key with a percentage (0-100) of neutral emotion detected. "
        "5. 'user_preferences': list of keywords or activities the user might enjoy or find comforting, inferred from the journal (e.g., 'listening to music', 'painting', 'going for a walk')\n"
        "6. 'personal_suggestion': if sadness is dominant, give a comforting suggestion using one or more of the detected preferences. Else return an empty string.\n"
        "Ensure the percentages add up to 100. Do not include any text outside of the JSON object. "
        "\n\nJournal Entry:\n\"" + entry_text + "\""
    )

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    payload = { "contents": [{"parts": [{"text": prompt}]}] }
    headers = { "Content-Type": "application/json" }

    try:
        api_response = requests.post(api_url, json=payload, headers=headers)
        api_response.raise_for_status()
        
        data = api_response.json()
        
        # Extract the text content which should be a JSON string
        response_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean the response to ensure it's valid JSON
        # Sometimes the model wraps the JSON in ```json ... ```
        if response_text.strip().startswith("```json"):
            response_text = response_text.strip()[7:-3]

        # Parse the JSON string into a Python dictionary
        analysis_data = json.loads(response_text)
        
        print("--- Successfully Parsed AI Analysis ---")
        print(analysis_data)
        
        return analysis_data
        
    except requests.exceptions.RequestException as e:
        print(f"!!! API REQUEST FAILED: {e}")
        return None
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"!!! FAILED TO PARSE JSON RESPONSE: {e}")
        print(f"!!! Raw response text was: {response_text}")
        return None

@login_required
def create_journal(request):
    if request.method == "POST":
        topic = request.POST.get("topic")
        entry = request.POST.get("entry")

        if topic and entry:
            ai_data = generate_response(entry)

            joy = float(ai_data.get("joy", 0)) if ai_data else None
            sad = float(ai_data.get("sadness", 0)) if ai_data else None
            neutral = float(ai_data.get("neutral", 0)) if ai_data else None
            preferences = ai_data.get("user_preferences", [])
            suggestion = ai_data.get("personal_suggestion", "")

            journal = Journal.objects.create(
                user=request.user,
                date=timezone.now().date(),
                topic=topic,
                entry=entry,
                joy=joy,
                sad=sad,
                neutral=neutral,
                ai_insight=ai_data
            )

            Activity.objects.create(
                user=request.user,
                activity_type='journal',
                description='Wrote a new journal entry'
            )

            # Redirect to the analysis page for the newly created journal
            return redirect(reverse('journal_analysis', args=[journal.id]))

    return render(request, "journal/create_journal.html")


@login_required
def journal_analysis(request, id):
    journal = Journal.objects.filter(id=id, user=request.user).first()

    if not journal:
        return redirect("create_journal")

    ai_insight = journal.ai_insight if journal.ai_insight else {}
    suggestion = ai_insight.get("personal_suggestion", "")
    preferences = ai_insight.get("user_preferences", [])
    insight = ai_insight.get("insight", "")

    emotions = {
        'joy': ai_insight.get("joy", 0),
        'sadness': ai_insight.get("sadness", 0),
        'neutral': ai_insight.get("neutral", 0),
    }

    dominant_emotion = max(emotions, key=emotions.get)

    emotion_icon_map = {
        'joy': '😊',
        'sadness': '😢',
        'neutral': '😐'
    }

    mood_icon = emotion_icon_map.get(dominant_emotion, '😐')

    parameters = {
        "ai_insight": ai_insight,
        "suggestion": suggestion,
        "preferences": preferences,
        "insight": insight,
        "mood_icon": mood_icon,
    }
    return render(request, "journal/journal_analysis.html", parameters)

@login_required
def read_journal(request,entry_id=None):
    all_journals = Journal.objects.filter(user=request.user).order_by('-created_at')
    selected_entry = None

    if entry_id:
        selected_entry = Journal.objects.get(id=entry_id, user=request.user)
    elif all_journals.exists():
        selected_entry = all_journals[0]

    return render(request, 'journal/read_journal.html', {'all_journals': all_journals,'selected_entry': selected_entry})

@login_required
def edit_journal(request, id):
    journal = Journal.objects.get(id=id)

    if request.method == "POST":
        date = request.POST.get("date")
        topic = request.POST.get("topic")
        entry = request.POST.get("entry")

        journal.date = date
        journal.topic = topic
        journal.entry = entry



        journal.is_edited = True

        journal.save()
        Activity.objects.create(
            user=request.user,
            activity_type='journal',
            description='Updated a journal entry'
        )
        return redirect('read_journal', entry_id=journal.id)
    
    parameters = {'selected_entry': journal}

    return render(request, 'journal/edit_journal.html', parameters)

@login_required
def delete_journal(request, id):
    try:
        journal = Journal.objects.get(id=id)
        journal.delete()
    except Journal.DoesNotExist:
        pass 
    
    return redirect("read_journal")