# polls/urls.py
from django.urls import path
from . import views

app_name = 'polls' # Bu, 'polls:detail' kimi adlandırmalar üçün vacibdir!
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'), 
    
    # ex: /polls/5/ <--- YENİ ƏLAVƏ ETMƏLİ OLDUĞUNUZ SATIR
    path('<int:question_id>/', views.detail, name='detail'), 
    
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]