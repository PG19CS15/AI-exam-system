from django.urls import path
from . import views
from .views import ExamQuestionListAPI, SubmitExamAPI, get_rules

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path("test/", views.testEndPoint, name="test"),
    path("exam-questions/", ExamQuestionListAPI.as_view(), name="exam-questions"),
    path("rules/", get_rules, name="get_rules"),
    path("submit-exam/", SubmitExamAPI.as_view(), name="submit-exam"),
    path("", views.getRoutes, name="get_routes"),
]
