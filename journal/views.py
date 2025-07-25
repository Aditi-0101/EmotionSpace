from django.shortcuts import render, redirect
from .models import Journal
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create_journal(request):
    if request.method == "POST":
        date = request.POST.get("date")
        topic = request.POST.get("topic")
        entry = request.POST.get("entry")
    
        Journal.objects.create(
            user=request.user,
            date=date,
            topic=topic,
            entry=entry
        )
        
        return redirect('read_journals')
        
    return render(request,"journal/create_journal.html")

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