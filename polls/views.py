# polls/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404 # ❗ Http404 əlavə edildi
from django.urls import reverse
from django.db.models import F 
from django.utils import timezone
from .models import Question, Choice 


def index(request):
    latest_question_list = Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by("-pub_date")[:5]
    
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    
    
def detail(request, question_id):
    # ❗ DÜZƏLİŞ: Obyekti əldə etməzdən əvvəl pub_date-i yoxlayırıq.
    try:
        question = Question.objects.filter(
            pub_date__lte=timezone.now(), # Yalnız keçmiş sualları qəbul edir
            pk=question_id,
        ).get() # Əgər tapılmasa, DoesNotExist xətası verir.
    except Question.DoesNotExist:
        # Gələcək sual tapılsa (və ya ümumiyyətlə tapılmasa) 404 qaytarır.
        raise Http404("Question does not exist") 

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # ❗ DÜZƏLİŞ: results view-u üçün də eyni filtrləməni tətbiq edirik.
    try:
        question = Question.objects.filter(
            pub_date__lte=timezone.now(),
            pk=question_id,
        ).get()
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
        
    return render(request, "polls/results.html", {"question": question})  


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Burada filtrləməyə ehtiyac yoxdur, çünki istifadəçi 'detail' səhifəsində səs verir.
    # Lakin, dərsliyin məntiqini tamamlamaq üçün Part 6-da bu hissəyə qayıdıb
    # 'was_published_recently' istifadə edə bilərik. İndilik keçək.
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1  
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))