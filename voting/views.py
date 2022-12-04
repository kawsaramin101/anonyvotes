import json 
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers 
from django.views.decorators.http import require_http_methods 

from .models import Poll, Option, AnonymousUser, Vote
from .forms import QuestionForm, OptionFormSet


def index(request):
    optionformset = OptionFormSet(queryset=Option.objects.none())
    context = {
        'optionformset': optionformset
    }
    return render(request, 'voting/index.html', context)


@require_http_methods(["POST"])
def add_question(request):
    question_form = QuestionForm(json.loads(request.body))
    if question_form.is_valid():
        question = question_form.save(commit=False)
        if request.user.is_authenticated:
            question.created_by = request.user 
        question.save()
        request.session["current_question"] = question.id
        return JsonResponse({'secondary_id': question.secondary_id}, status=200)
    return HttpResponse("Something went wrong", status=400)


@require_http_methods(["POST"])
def add_option(request):
    error = None
    question_id = request.session.get("current_question")
    if question_id is None:
        error = "Please add a question."
    if error is None:
        data = json.loads(request.body).get('options')
        optionformset = OptionFormSet(data=data)
        
        if optionformset.is_valid():
            instances = optionformset.save(commit=False)
            for instance in instances:
                instance.poll_id = question_id
                instance.save()
            del request.session['current_question']
            return HttpResponse("It worked", status=201)
        return render(request, 'voting/partials/options-form.html',  {'optionformset': optionformset})
    return HttpResponse(f"{error}", status=400)


def get_poll(secondary_id):
    try:
        poll = Poll.objects.prefetch_related('options', 'votes').get(secondary_id=secondary_id)
    except:
        poll = None 
    return poll 
    
    
def vote(request, question_secondary_id):
    poll = get_poll(question_secondary_id)
    anonymous_user_id = request.session.get('anonymous_user_id')
    
    if anonymous_user_id is None:
        anonymous_user = AnonymousUser.objects.create()
        request.session['anonymous_user_id'] = anonymous_user.id 
    else:
        anonymous_user = AnonymousUser.objects.get(id=anonymous_user_id)
    prev_vote = anonymous_user.votes.filter(poll=poll)
    context = {
        'poll': poll,
        'anonymous_user': anonymous_user,
        'prev_selected_option': prev_vote.first().option if prev_vote.exists() else None
    }
    if request.method == "POST":
        if not poll.is_open:
            return HttpResponse("Poll is closed.")
        body = request.POST
        if not poll.options.filter(secondary_id=body.get("option_secondary_id")).exists():
            return HttpResponse("Option doesn’t exist in poll options", status=400)
        vote = Vote.objects.filter(poll=poll, voter=anonymous_user)
        if vote.exists():
            vote.delete()
        selected_option = Option.objects.get(secondary_id=body.get("option_secondary_id"))
        new_vote = Vote.objects.create(poll=poll, option=selected_option, voter=anonymous_user)
        context['poll'] = get_poll(question_secondary_id)
        context['prev_selected_option'] = selected_option 
        return render(request, 'voting/partials/vote-partial.html', context)
    return render(request, 'voting/vote.html', context)
    
        