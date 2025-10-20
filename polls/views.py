# polls/views.py

# Çatışmayan funksiyaları və modelləri import edirik
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse # HttpResponseRedirect və HttpResponse-u əlavə etdik
from django.urls import reverse # reverse funksiyasını əlavə etdik
from django.db.models import F # F ifadəsini əlavə etdik

# Question modelini import etmişdik, Choice modelini də əlavə edirik (Çünki vote funksiyasında istifadə olunur)
from .models import Question, Choice 


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    
    # OUTPUT-u (çıxışı) sadə mətn əvəzinə, şablon vasitəsilə göndəririk
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Həll 2 üçün 'polls/detail.html' faylının mövcud olduğunu yoxlayın
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Düzəliş: Sondakı əlavə mötərizəni sildik.
    return render(request, "polls/results.html", {"question": question}) 

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Seçim id-si (pk) POST data vasitəsilə gəlir
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Səs verilmədiyi halda xəta mesajı ilə 'detail' şablonuna qayıdırıq.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # F("votes") + 1 atomar bir əməliyyat üçün istifadə olunur
        selected_choice.votes = F("votes") + 1 
        selected_choice.save()
        # POST datası uğurla idarə edildikdən sonra həmişə HttpResponseRedirect qaytarın.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))