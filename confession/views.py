from django.shortcuts import render, redirect
from .models import Confession
from django.contrib.auth.decorators import login_required
from dashboard.models import Activity

@login_required
def create_confession(request):
    if request.method == "POST":
        user_confession = request.POST.get("confession")


        new_confession = Confession(
            user = request.user,
            confession=user_confession
        )
        new_confession.save()
        Activity.objects.create(
            user=request.user, 
            activity_type='confession', 
            description='Posted a new confession'
        )
        print("New confession added successfully!")
        return redirect("display_confession")

    return render(request, "confession/create_confession.html")

@login_required
def display_confession(request):
    confessions = Confession.objects.filter(user=request.user).order_by("-id")
    parameters = {
        "confessions": confessions
    }
    return render(request, "confession/display_confession.html", parameters)

@login_required
def delete_confession(request, id):
    confession = Confession.objects.get(id=id)
    confession.delete()
    return redirect('display_confession')

@login_required
def update_confession(request, id):
    confession = Confession.objects.get(id=id)

    if request.method == "POST":
        confession.confession = request.POST.get("confession")
        confession.is_edited = True
        confession.save()
        Activity.objects.create(
            user=request.user, 
            activity_type='confession', 
            description='Updated a confession'
        )
        return redirect('display_confession')
    
    parameters = {'confession': confession}

    return render(request, 'confession/update_confession.html', parameters)