"""
This is admin site.

This module can adjust everythings about the questions.
"""
from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    """Admin can edit all choices in this section."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Make admin site to appear optional menu."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')


admin.site.register(Question, QuestionAdmin)
