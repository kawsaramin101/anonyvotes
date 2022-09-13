import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers 
from django.views.decorators.http import require_http_methods 

from .models import Poll, Option, AnonymousUser
from .forms import QuestionForm


def index(request):
    return render(request, 'voting/index.html',)


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
    question = request.session.get("current_question")
    if question is None:
        error = "Please add a question."
    options = json.loads(request.body)
    if not len(options) >= 2 or list(options.values())[0] == "" or list(options.values())[1] == "":
        error = "Please add at least two options."
    
    for index, (option_key, option_value) in enumerate(options.items()):
        if len(option_value) > 1000:
            error = "Option cannot be larger than 1000 characters."
            break
        else:
            Option.objects.create(text=option_value, poll_id=question)
    if error is None:
        return HttpResponse("It worked", status=200)
    return JsonResponse({'message': error}, status=400)

    
    
def vote(request, question_secondary_id):
    poll = Poll.objects.filter(secondary_id=question_secondary_id).prefetch_related('options').first()
    anonymous_user_id = request.session.get('anonymous_user_id')
    if anonymous_user_id is None:
        anonymous_user = AnonymousUser.objects.create()
    else:
        anonymous_user = AnonymousUser.objects.get(id=anonymous_user_id)
        request.session['anonymous_user_id'] = anonymous_user.id 
    #if request.method == "POST":
        
    context = {
        'poll': poll,
        'anonymous_user': anonymous_user,
    }
    return render(request, 'voting/vote.html', context)