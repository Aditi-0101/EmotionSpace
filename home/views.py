from django.shortcuts import render, redirect
from confession.models import Confession
from django.contrib.auth.decorators import login_required
from dashboard.models import Activity
from confession.models import Comment
from django.urls import reverse

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

            Activity.objects.create(
                user=request.user,
                activity_type='like',
                description='Liked a confession'
            )
    return redirect('home')

@login_required
def add_comment(request, confession_id):
    if request.method == 'POST':
        confession = Confession.objects.get(id=confession_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(confession=confession, user=request.user, content=content)
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