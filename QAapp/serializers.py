from rest_framework import serializers
from .models import QAModel


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QAModel
        fields = ["user", "id", "question", "answer", "date_posted"]
