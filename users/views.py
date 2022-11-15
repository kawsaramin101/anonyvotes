from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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