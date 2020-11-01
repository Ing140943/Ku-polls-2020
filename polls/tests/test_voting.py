"""Test case for DetailView."""
import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from polls.models import Question
from django.test import TestCase
from django.utils import timezone


def create_question(question_text, days):
    """Create a question with the given `question_text`."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time)


class VotingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin', email='email@some.domain', password='12345')
       
    def test_authenticate_user_vote(self):
        self.client.post(reverse('login'), {'username': 'admin', 'password': '12345'}, follow=True)
        question = create_question(question_text='Avaliable Question.', days=10)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticate_user_vote(self):
        self.client.post(reverse('login'), {'username': 'admins', 'password': '12345'}, follow=True)
        question = create_question(question_text='Avaliable Question.', days=10)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 302)
