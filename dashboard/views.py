from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from journal.models import Journal
from confession.models import Confession
from .models import Activity
import requests
import json
from django.conf import settings

@login_required
def dashboard(request):
    user = request.user

    journals = Journal.objects.filter(user=user)
    confessions = Confession.objects.filter(user=user)

    journal_count = journals.count()
    confession_count = confessions.count()

    journal_dates = [journal.created_at.date() for journal in journals]
    # Assuming Confession model has 'date_created'
    confession_dates = [confession.date_created.date() for confession in confessions] 

    active_days = set(journal_dates + confession_dates)
    days_active = len(active_days)

    user_confessions = Confession.objects.filter(user=request.user)
    total_likes = sum(confession.hearts.count() for confession in user_confessions)

    recent_activities = Activity.objects.filter(user=request.user).order_by('-timestamp')[:5]

    parameters = {
        "journal_count": journal_count,
        "confession_count": confession_count,
        "days_active": days_active,
        "total_likes": total_likes,
        "recent_activities": recent_activities,
    }

    return render(request, "dashboard/dashboard.html", parameters)