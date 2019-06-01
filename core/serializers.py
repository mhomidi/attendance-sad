from rest_framework import serializers

from core.models import Exam


class ExamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def create(self, validated_data):
        exam_id = validated_data.get('id')
        instance, _ = Exam.objects.update_or_create(id=exam_id, defaults=validated_data)
        return instance

    class Meta:
        model = Exam
        exclude = []
