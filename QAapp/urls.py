from django.urls import path
from .views import PostQuestionAnswerView, UserQAListViews

urlpatterns = [
    path("", PostQuestionAnswerView.as_view(), name="PostQA"),
    path("list/", UserQAListViews.as_view(), name="UserQAList"),
]
