"""The overview of the webserver."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Have to create question which have deadline."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end dated')

    def __str__(self):
        """Return the question in text form."""
        return self.question_text

    def was_published_recently(self):
        """Check that polls is published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check that this question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check what questions user can vote."""
        now = timezone.now()
        return self.end_date >= now and self.end_date >= self.pub_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Have to create many choices for answer the polls."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice in text form."""
        return self.choice_text
