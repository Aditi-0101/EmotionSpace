from django.shortcuts import render, redirect
from .models import Confession
from django.contrib.auth.decorators import login_required

@login_required
def create_confession(request):
    if request.method == "POST":
        user_name = request.POST.get("name")
        user_confession = request.POST.get("confession")


        new_confession = Confession(
            user = request.user,
            name=user_name,
            confession=user_confession
        )
        new_confession.save() 
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
        confession.name = request.POST.get("name")
        confession.confession = request.POST.get("confession")
        confession.is_edited = True
        confession.save()
        return redirect('display_confession')
    
    parameters = {'confession': confession}

    return render(request, 'confession/update_confession.html', parameters)