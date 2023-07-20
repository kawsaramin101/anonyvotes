from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
            #return render(request, 'users/partials/signupform.html', {'form': form})
    
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})
        
    return redirect(request.META.get('HTTP_REFERER', '/'))
    


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse 

"""
def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            next_page = request.POST.get("next", "/")
            if not username or not password:
                return HttpResponse("Username or Password can't be empty")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Logged in as {user.username}")
                response = HttpResponse()
                response.headers['HX-Redirect'] = next_page
                return response
            else:
                return HttpResponse("Username or Password didn't match")
        return render(request, 'users/login.html')
    return redirect(request.META.get('HTTP_REFERER', '/'))
    """
 
def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out")
    next_page = request.GET.get("next") or "/"
    return redirect(next_page)
    

    
def check_username_availability(request):
    if request.method == "POST":
        username=request.POST["username"]
        if username == "":
            return HttpResponse("")
        
        user_obj=CustomUser.objects.filter(username=username)
        if user_obj.exists():
            return HttpResponse("A user with that username already exists.")
        return HttpResponse("")
    return HttpResponse("Method not allowed")


def check_email_availability(request):
    if request.method == "POST":
        email=request.POST["email"]
        if email == "":
            return HttpResponse("")
        
        user_obj=CustomUser.objects.filter(email=email)
        if user_obj.exists():
            return HttpResponse("User with this Email address already exists.")
        return HttpResponse("")
    return HttpResponse("Method not allowed")
        