from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse 

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
    