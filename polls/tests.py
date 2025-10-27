# polls/tests.py faylının əvvəli
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

# ❗ Çatışmayan importu əlavə edin
from django.urls import reverse
# ----------------- Köməkçi Funksiya (Helper) -----------------
def create_question(question_text, days):
    """
    Verilmiş sual mətni (question_text) və 
    gələcəyə/keçmişə (müsbət/mənfi 'days') aid pub_date ilə 
    bir Question nümunəsi yaradır.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
# -----------------------------------------------------------


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """
        pub_date gələcəkdə olan suallar üçün was_published_recently() 
        metodu False qaytarmalıdır.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        pub_date 1 gündən çox keçmişdə olan suallar üçün 
        was_published_recently() metodu False qaytarmalıdır.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        pub_date son 1 gün ərzində olan suallar üçün 
        was_published_recently() metodu True qaytarmalıdır.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
# polls/tests.py (əvvəlki kodun ardı)
# ... QuestionModelTests sinifindən sonra

class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """
        Əgər sual yoxdursa, müvafiq bir mesaj göstərilməlidir.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Keçmişdə dərc edilmiş suallar index səhifəsində göstərilir.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Gələcəkdə dərc edilmə tarixi olan suallar index səhifəsində göstərilməməlidir.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Yalnız keçmiş suallar göstərilməlidir.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        Index səhifəsində çoxlu keçmiş suallar göstərilə bilər.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        # Django sualları pub_date-ə görə sıralayır (ən sonuncu birinci gəlir)
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
        
# polls/tests.py (Ən sona əlavə edin)

class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        pub_date gələcəkdə olan sualın 'detail' səhifəsinə 
        GET sorğusu 404 Not Found cavabı verməlidir.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        pub_date keçmişdə olan sualın 'detail' səhifəsinə 
        GET sorğusu 200 OK cavabı verməli və sual mətnini göstərməlidir.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    
    def test_future_question(self):
        """
        pub_date gələcəkdə olan sualın 'results' səhifəsinə 
        GET sorğusu 404 Not Found cavabı verməlidir.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        pub_date keçmişdə olan sualın 'results' səhifəsinə 
        GET sorğusu 200 OK cavabı verməlidir.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)