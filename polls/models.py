# polls/models.py (Birləşdirilmiş Düzgün Versiya)

import datetime
from django.db import models
from django.utils import timezone 

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    # ❗ _str_ metodu
    def _str_(self):
        return self.question_text
    
    # ❗ was_published_recently metodu (Sınaqların tələb etdiyi)
    def was_published_recently(self):
        now = timezone.now()
        # pub_date 1 gün ərzindədirsə True qaytarır
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    # Foreign Key Question sinfinin təkrar təyin olunmuş versiyasına yox, 
    # yuxarıdakı yeganə versiyasına yönəlməlidir.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def _str_(self):
        return self.choice_text