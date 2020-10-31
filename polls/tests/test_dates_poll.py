"""Test for the question that valid"""
import datetime


from django.test import TestCase
from django.utils import timezone

from ..models import Question

def create_question(question_text, days):
    """Create a question with the given `question_text`."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time)

class QuestionModelTests(TestCase):
    """Test question model with many situations."""

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_is_published_with_avaliable_polls(self):
        """is_published() return True for questions that are currently on."""
        time = timezone.now() - datetime.timedelta(days=7)
        question = Question(pub_date=time)
        self.assertIs(question.is_published(), True)

    def test_is_published_with_unavaliable_polls(self):
        """is_publishd() return False for the questions that are't currentlr on."""
        time = timezone.now() + datetime.timedelta(days=7)
        question = Question(pub_date=time)
        self.assertIs(question.is_published(), False)

    def test_can_vote_questions_before_published_date(self):
        """The user can vote only the polls that are allowed."""
        time = timezone.now() - datetime.timedelta(days=5)
        date = timezone.now() + datetime.timedelta(days=5)
        question = Question(pub_date=time, end_date=date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_questions_after_published_date(self):
        """The user can vote only the polls that are allowed."""
        time = timezone.now() + datetime.timedelta(days=5)
        date = timezone.now() - datetime.timedelta(days=5)
        question = Question(pub_date=time, end_date=date)
        self.assertEqual(question.can_vote(), False)