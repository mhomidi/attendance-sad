from django.db import transaction
from rest_framework import serializers

from core.models import Exam, ClassFormation, ExamListItem, Student, Course, Professor


class ProfessorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def create(self, validated_data):
        professor_id = validated_data.pop('id')
        professor, _ = Professor.objects.update_or_create(id=professor_id, defaults=validated_data)
        return professor

    class Meta:
        model = Professor
        exclude = []


class CourseSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer()

    def create(self, validated_data):
        professor = ProfessorSerializer(data=validated_data.pop('professor'))
        professor.is_valid(raise_exception=True)
        validated_data['professor_id'] = professor.save().id
        return super().create(validated_data)

    class Meta:
        model = Course
        exclude = []


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Student
        exclude = []


class ExamListItemSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    exam_id = serializers.IntegerField()

    def create(self, validated_data):
        validated_data['student'], _ = Student.objects.get_or_create(
            id=validated_data['student']['id'], defaults=validated_data['student'])
        return super().create(validated_data)

    class Meta:
        model = ExamListItem
        exclude = ['exam']


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassFormation
        exclude = []


class ExamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    formation = FormationSerializer()
    items = ExamListItemSerializer(many=True)
    course = CourseSerializer()

    @transaction.atomic
    def create(self, validated_data):
        exam_id = validated_data['id']
        validated_data['formation'] = ClassFormation.objects.create(
            **validated_data['formation'])
        ExamListItem.objects.filter(exam_id=exam_id).delete()
        list_items = ExamListItemSerializer(many=True, data=validated_data.pop('items'))
        list_items.is_valid(raise_exception=True)
        list_items.save()
        course = CourseSerializer(data=validated_data.pop('course'))
        course.is_valid(raise_exception=True)
        validated_data['course_id'] = course.save().id
        exam, _ = Exam.objects.update_or_create(id=exam_id, defaults=validated_data)

        return exam

    class Meta:
        model = Exam
        exclude = []
