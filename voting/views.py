import json
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
        question = question_form.save()
        request.session["current_question"] = question.id
        #serialized_instance = serializers.serialize('json', [ question ])
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

    
def vote(request, question_secondary_id):
    poll = Poll.objects.filter(secondary_id=question_secondary_id).prefetch_related('options', 'votes').first()
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
        body = json.loads(request.body)
        if not poll.options.filter(secondary_id=body.get("option_secondary_id")).exists():
            return HttpResponse("Option doesn’t exist in poll options", status=400)
        vote = Vote.objects.filter(poll=poll, voter=anonymous_user)
        if vote.exists():
            vote.delete()
        selected_option = Option.objects.get(secondary_id=body.get("option_secondary_id"))
        new_vote = Vote.objects.create(poll=poll, option=selected_option, voter=anonymous_user)
        context["prev_selected_option"] = selected_option
        return render(request, 'voting/partials/vote-partial.html', context)
    return render(request, 'voting/vote.html', context)
    
        