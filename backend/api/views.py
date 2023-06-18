from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from django.views import View
from .models import ExamQuestion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ExamSubmission
from .serializer import ExamSubmissionSerializer

# Create your views here.
from django.http import JsonResponse
from .models import Rule


def get_rules(request):
    rules = Rule.objects.values_list("content", flat=True)
    return JsonResponse(list(rules), safe=False)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/token/",
        "/api/register/",
        "/api/token/refresh/",
        "/api/prediction/",
    ]
    return Response(routes)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == "GET":
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({"response": data}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get("text")
        data = (
            f"Congratulation your API just responded to POST request with text: {text}"
        )
        return Response({"response": data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


class ExamQuestionListAPI(APIView):
    def get(self, request):
        questions = ExamQuestion.objects.all()
        serialized_questions = [
            {
                "id": question.pk,
                "question_text": question.question_text,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "points": question.points,
            }
            for question in questions
        ]
        return Response(serialized_questions)


class SubmitExamAPI(APIView):
    def post(self, request):
        submitted_answers = request.data
        score = 0

        for question_id, answer in submitted_answers.items():
            try:
                question = ExamQuestion.objects.get(id=question_id)
                if answer == question.correct_answer:
                    score += question.points
            except ExamQuestion.DoesNotExist:
                # Handle the case where the question doesn't exist
                pass

        username = request.user.username  # Assuming you have authentication enabled
        submission = ExamSubmission(username=username, score=score)
        submission.save()

        serializer = ExamSubmissionSerializer(submission)
        return Response(serializer.data)
