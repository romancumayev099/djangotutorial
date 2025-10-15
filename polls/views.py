# polls/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse # index üçün lazımdır
from .models import Question

# TƏLƏB OLUNAN DÜZƏLİŞ: index funksiyasını da şablon istifadə edəcək şəkildə dəyişin
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    
    # OUTPUT-u (çıxışı) sadə mətn əvəzinə, şablon vasitəsilə göndərin
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Həll 2 üçün 'polls/detail.html' faylının mövcud olduğunu yoxlayın
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    # Bu funksiyalar hələlik belə qala bilər, amma təkrar yazılmamalıdır.
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)