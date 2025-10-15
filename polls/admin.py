# polls/admin.py

from django.contrib import admin
from .models import Question, Choice # Choice modelini də import edin!

# 1. Choice modelini Question-a Inline olaraq əlavə edirik
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 # Bir sual əlavə edərkən ilkin olaraq 3 cavab yeri göstərir
    
# 2. Question modelinin admin görünüşünü yenidən təyin edirik
class QuestionAdmin(admin.ModelAdmin):
    # Bu sahələr admin panelində Question-un detallarına daxil olanda görünür
    fields = ['pub_date', 'question_text'] 
    
    # Inline-ı QuestionAdmin-ə əlavə edirik
    inlines = [ChoiceInline]

# 3. Yenilənmiş QuestionAdmin-i Admin panelinə qeyd edirik
admin.site.register(Question, QuestionAdmin)

# 4. Choice modelini ayrıca qeyd etməyə ehtiyac qalmır, çünki o artıq
#    Question modelinin içindədir.