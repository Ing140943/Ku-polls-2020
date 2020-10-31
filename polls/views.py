"""Contain index, detail and result page."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from .models import Choice, Question, Vote
from django.dispatch import receiver

from .settings import LOGGING
import logging.config

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('polls')

def get_client_ip(request):
    """Get ip address from the user."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def throw_feedback_login(sender, request, user, **kwargs):
    """Show some response when the user have log in."""
    logger.info(f"Username: {user.username} User's IP: {get_client_ip(request)} is log in.")


@receiver(user_logged_out)
def throw_feedback_log_out(sender, request, user, **kwargs):
    """Show some responses when the user have log out."""
    logger.info(f"Username: {user.username} User's IP: {get_client_ip(request)} is log out.")


@receiver(user_login_failed)
def feedback_fail_login(sender, credentials, request, **kwargs):
    """Show some responses when the user fail to log in."""
    logger.warning(f"Username {request.POST['username']} User's IP: {get_client_ip(request)} when the user login failed.")

class IndexView(generic.ListView):
    """The index page for showing infomation the questions."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]


class DetailView(generic.DetailView):
    """The detail page for showing infomation the questions."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """The result page show the total vote for each polls."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Voting for each polls by select the choice."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if not (question.can_vote()):
            text = "The poll that you selected is not allowed."
            return HttpResponseRedirect(reverse('polls:index'), messages.warning(request, text))
        Vote.objects.update_or_create(user =request.user, question =question, defaults ={'choice': selected_choice})
        for q in Question.objects.all():
            q.recently_vote = request.user.vote_set.get(question=question).choice.choice_text
            q.save()
        messages.success(request, "Already complete your polls.")
        logger.info(f"Username: {request.user.username} User's IP: {get_client_ip(request)}  Question ID: {question.id} vote sucessful.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
