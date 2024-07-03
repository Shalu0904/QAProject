from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import QAModel
from .serializers import QASerializer
from rest_framework.pagination import PageNumberPagination


class PostQuestionAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "delete", "patch"]

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = QASerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        question_id = request.query_params.get("id")
        try:
            question = QAModel.objects.get(id=question_id)
            if question.user == request.user:
                serializer = QASerializer(question)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "You are not authorized to view this answer.",
                    status=status.HTTP_403_FORBIDDEN,
                )
        except QAModel.DoesNotExist:
            return Response(
                "Question does not exist.", status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            qa = QAModel.objects.get(pk=pk)
            if qa.user != request.user:
                return Response(
                    "You are not authorized to delete this question.",
                    status=status.HTTP_403_FORBIDDEN,
                )

            qa.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QAModel.DoesNotExist:
            return Response(
                "Question does not exist.", status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk):
        try:
            qa = QAModel.objects.get(pk=pk)
            if qa.user != request.user:
                return Response(
                    "You are not authorized to update this question.",
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = QASerializer(qa, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        except QAModel.DoesNotExist:
            return Response(
                "Question does not exist.", status=status.HTTP_404_NOT_FOUND
            )


class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 100


class UserQAListViews(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        user = request.user
        data = QAModel.objects.filter(user=user)

        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(data, request)

        serializer = QASerializer(paginated_data, many=True)
        return paginator.get_paginated_response(serializer.data)
