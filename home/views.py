from django.shortcuts import render, redirect
from confession.models import Confession
from django.contrib.auth.decorators import login_required

def main(request):
    return render(request, "home/main.html", )

@login_required
def home(request):
    confessions = Confession.objects.all().order_by("-id")
    parameters = {
        "confessions": confessions
    }
    return render(request, "home/home.html", parameters)

@login_required
def toggle_heart(request, confession_id):
    confession = Confession.objects.filter(id=confession_id).first()
    if confession:
        if request.user in confession.hearts.all():
            confession.hearts.remove(request.user)
        else:
            confession.hearts.add(request.user)
    return redirect('home')

def about(request):
    return render(request, "home/about.html")

def privacy(request):
    return render(request, "home/privacy.html")

def tos(request):
    return render(request, "home/tos.html")

def cg(request):
    return render(request, "home/cg.html")

def contact(request):
    return render(request, "home/contact.html")