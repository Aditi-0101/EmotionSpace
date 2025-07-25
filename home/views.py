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
    confession = Confession.objects.get(id=confession_id)
    
    
    if request.method == 'POST':
        # Get the text from the form's input field
        comment_body = request.POST.get('comment_body')
        
        # Make sure the comment isn't empty
        if comment_body:
            # Create and save the new Comment in the database
            Comment.objects.create(
                confession=confession,
                user=request.user,
                body=comment_body
            )
            
            # Also create an Activity record for the feed
            Activity.objects.create(
                user=request.user,
                activity_type='comment',
                description='Commented on a confession'
            )

    # Redirect the user back to the home page, scrolling to the post they commented on
    return redirect(f"{reverse('home')}#confession-{confession_id}")

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