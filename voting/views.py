import json 
import time
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core import serializers 
from django.views.decorators.http import require_http_methods 
from django.urls import reverse 

from .models import Poll, Option, AnonymousUser, Vote
from .forms import QuestionForm, OptionFormSet


def index(request):
    question_form = QuestionForm()
    option_formset = OptionFormSet(queryset=Option.objects.none())
    context = {
        'question_form': question_form,
        'option_formset': option_formset,
    }
    return render(request, 'voting/index.html', context)


@require_http_methods(["POST"])
def add_question(request):
    question_form = QuestionForm(request.POST)
    context = {}
    if question_form.is_valid():
        question = question_form.save(commit=False)
        if request.user.is_authenticated:
            question.created_by = request.user 
        question.save()
        request.session["current_question"] = question.id
        context["question_form"] = question_form
        context["question_status"] = "Question created"
        context["question_secondary_id"] = question.secondary_id
        return render(request, 'voting/partials/question-form.html', context)

    context["question_form"] = question_form
    return render(request, 'voting/partials/question-form.html', context)
    

@require_http_methods(["POST"])
def add_option(request):
    option_status = None
    question_id = request.session.get("current_question")
    if question_id is None:
        option_status = "Please add a question."
    if option_status is None:
        poll = Poll.objects.get(id=question_id)
        #data = json.loads(request.body).get('options')
        option_formset = OptionFormSet(data=request.POST)
        
        if option_formset.is_valid():
            instances = option_formset.save(commit=False)
            for instance in instances:
                instance.poll = poll
                instance.save()
            del request.session['current_question']
            response = HttpResponse()
            response.headers['HX-Redirect'] = reverse('voting:vote', kwargs={'question_secondary_id': poll.secondary_id})
            return response
            #return redirect(reverse('voting:vote', kwargs={'question_secondary_id': poll.secondary_id}))
            #return HttpResponse("It worked", status=201)
        return render(request, 'voting/partials/options-form.html',  {'option_formset': option_formset})
    return render(request, 'voting/partials/options-form.html',  {'option_status': option_status})
    #return HttpResponse(f"{error}", status=400)


def get_poll(secondary_id):
    try:
        poll = Poll.objects.prefetch_related('options', 'votes').get(secondary_id=secondary_id)
    except:
        poll = None 
    return poll 
    
    
def vote(request, question_secondary_id):
    # Query the poll and get the anonymous_user_id from session
    poll = get_poll(question_secondary_id)
    anonymous_user_id = request.session.get('anonymous_user_id')
    
    # Query AnonymousUser from DB and create, if it doesn’t exists already
    if anonymous_user_id is None:
        anonymous_user = AnonymousUser.objects.create()
        request.session['anonymous_user_id'] = anonymous_user.id 
    else:
        anonymous_user = AnonymousUser.objects.get(id=anonymous_user_id)
    
    #Get AnonymousUser Previous vote option if it exists or else set it to Null
    prev_vote = anonymous_user.votes.filter(poll=poll)
    context = {
        'poll': poll,
        'anonymous_user': anonymous_user,
        'prev_selected_option': prev_vote.first().option if prev_vote.exists() else None,
        'pollOptionsName': [option.text for option in poll.options.all()],
        'pollOptionsVoteParcentage':  [option.vote_percentage for option in poll.options.all()],
    }
    
    if request.method == "POST":
        if not poll.is_open:
            return HttpResponse("Poll is closed.")
        
        body = request.POST 
        
        if not poll.options.filter(secondary_id=body.get("option_secondary_id")).exists():
            return HttpResponse("Option doesn’t exist in poll options", status=400)
            
        vote = Vote.objects.filter(poll=poll, voter=anonymous_user)
        if vote.exists():
            if str(vote.first().option.secondary_id) == body.get("option_secondary_id"):
                context["vote_status"] = "Already voted."
                return render(request, 'voting/partials/vote-partial.html', context)
            vote.delete()
            
        selected_option = Option.objects.get(secondary_id=body.get("option_secondary_id"))
        new_vote = Vote.objects.create(poll=poll, option=selected_option, voter=anonymous_user)
        
        context['poll'] = get_poll(question_secondary_id)
        context['prev_selected_option'] = selected_option  
        context["vote_status"] = "Voted. Click to change vote."
        
        return render(request, 'voting/partials/vote-partial.html', context)
    return render(request, 'voting/vote.html', context)
    

def poll_raw_data(request:HttpRequest, question_secondary_id):
    poll = get_poll(question_secondary_id)
    