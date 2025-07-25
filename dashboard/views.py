from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from journal.models import Journal
from confession.models import Confession
from .models import Activity
import requests
import json

def get_mood_analysis_from_ai(user_journals):
    combined_text = "\n".join([journal.ai_analysis for journal in user_journals if journal.ai_analysis])

    if not combined_text:
        return None 
    prompt = (
        "Analyze the following collection of thoughts and emotional summaries. "
        "Based ONLY on this text, calculate the percentage breakdown for 'Joy', 'Sadness', and 'Neutral' emotions. "
        "Also, provide a single, gentle, one-sentence insight summarizing the overall tone. "
        "Your response MUST be a valid JSON object with no other text before or after it. "
        "Example format: {\"joy\": 75, \"sadness\": 10, \"neutral\": 15, \"insight\": \"The overall tone of these entries is hopefully optimistic.\"}"
        f"\n\nText to analyze:\n{combined_text}"
    )

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        raw_data = response.json()
        json_text = raw_data["candidates"][0]["content"]["parts"][0]["text"].strip().replace("```json", "").replace("```", "")
        
        analysis_data = json.loads(json_text)
        return analysis_data
        
    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error getting AI analysis: {e}")
        return None


@login_required
def dashboard(request):
    user = request.user

    journals = Journal.objects.filter(user=user)
    confessions = Confession.objects.filter(user=user)

    journal_count = journals.count()
    confession_count = confessions.count()

    journal_dates = [journal.created_at.date() for journal in journals]
    confession_dates = [confession.date_created.date() for confession in confessions]

    active_days = set(journal_dates + confession_dates)
    days_active = len(active_days)

    user_confessions = Confession.objects.filter(user=request.user)
    total_likes = sum(confession.hearts.count() for confession in user_confessions)

    recent_activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:5]

    recent_journals_for_analysis = Journal.objects.filter(
        user=request.user, 
        ai_analysis__isnull=False
    ).order_by('-date')[:10]

    mood_analysis_data = get_mood_analysis_from_ai(recent_journals_for_analysis)

    parameters = {
        "journal_count": journal_count,
        "confession_count": confession_count,
        "days_active": days_active,
        "total_likes": total_likes,
        "recent_activities": recent_activities,
        "mood_analysis": mood_analysis_data,
    }

    return render(request, "dashboard/dashboard.html", parameters)
