from django.contrib import admin
from .models import ExamQuestion, Rule, ExamSubmission

admin.site.register(ExamQuestion)
admin.site.register(Rule)

admin.site.register(ExamSubmission)
