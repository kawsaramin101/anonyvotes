from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from voting.models import Poll


@login_required
def user_polls(request):
    polls = Poll.objects.filter(created_by=request.user)
    open_polls = Poll.objects.filter(created_by=request.user, is_open=True).count()
    closed_polls = Poll.objects.filter(created_by=request.user, is_open=False).count()
    
    context = {
        "polls": polls,
        "open_polls": open_polls,
        "closed_polls": closed_polls
    }
    return render(request, "users/user-polls.html", context=context)
    

@login_required
def close_poll(request, secondary_id):
    if request.method == "POST":
        try:
            poll = Poll.objects.prefetch_related('options', 'votes').get(secondary_id=secondary_id)
        except:
            response = "Poll doesn’t exist."
        if not request.user == poll.created_by:
            response = "Not allowed"
        else:
            poll.is_open = False
            poll.save()
            response = "Closed"
        return HttpResponse(response)
  
  
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username or not password:
            return HttpResponse("Username or Password can't be empty")

        user = authenticate(request, username=username, password=password)
        if user is None:
            response = "Username or Password is incorrect"
            return HttpResponse(response)
        else:
            auth_login(request, user)
            response = HttpResponse()
            response.headers['HX-Redirect'] = reverse('users:user_polls')
            return response
            
    return render(request, "users/login.html")
    

def signup(request):
    if not request.user.is_authenticated:
        
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                messages.success(request, f"Signed up as {user.username}")
                response = HttpResponse()
                response.headers['HX-Redirect'] = reverse('users:user_polls')
                return response 
            print(form.as_p())
            return HttpResponse(form.as_p())
            
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})
        
    return redirect(request.META.get('HTTP_REFERER', '/'))
    

def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out")
    return redirect("/")



