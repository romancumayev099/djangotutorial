# polls/urls.py (Düzəldilmiş versiya)
from django.urls import path
from . import views

app_name = 'polls' # Bu, 'polls:detail' kimi adlandırmalar üçün vacibdir!
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'), 
    
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'), 
    
    # ex: /polls/5/results/ <-- Şərhi yığışdırdıq
    path('<int:question_id>/results/', views.results, name='results'),
    
    # ex: /polls/5/vote/ <-- Şərhi yığışdırdıq VƏ listin içərisinə köçürdük
    path('<int:question_id>/vote/', views.vote, name='vote'), 
]

# AŞAĞIDAKİ SƏTRİ SİLİN: Çünki yuxarıda artıq listin daxilindədir.
# path("<int:question_id>/vote/", views.vote, name="vote"),