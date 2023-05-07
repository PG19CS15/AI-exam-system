from django.db import models



class Rule(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content


class ExamQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ExamSubmission(models.Model):
    username = models.CharField(max_length=255)
    submission_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.username} - {self.submission_date}"
