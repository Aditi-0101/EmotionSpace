from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages

# Create your views here.
def join(request):
    if request.method == "POST":
        action = request.POST.get("action")                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        if action == "register":
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is already taken. Please choose another.")
                return redirect('/accounts/join?form=register')
            User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user = auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            
            return redirect('home')
        
        if action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = auth.authenticate(request,username=username,password=password)
            
            if user is not None:
                auth.login(request,user)
                return redirect("home")
            
            messages.error(request, "Invalid username or password!")
            return redirect('join')
                
    return render(request,'accounts/join.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect("main")