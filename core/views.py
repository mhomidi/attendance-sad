from datetime import datetime
from typing import Dict, List

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from requests import status_codes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from core.models import Exam, ExamListItem
from core.serializers import ExamSerializer


class FetchExams(ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get_digitized_time(time_str: str) -> str:
        h, m = time_str.split('h')
        h = h if len(h) > 1 else '0{}'.format(h)
        m = m if len(m) else '00'
        return '{}:{}'.format(h, m)

    @staticmethod
    def _get_normalized_date(date_str: str) -> 'datetime.date':
        return datetime.strptime(date_str, '%a %b %d %Y').date()

    def _get_basic_exam_data(self, api_data: Dict, api_date: str) -> Dict:
        return {
            'id': api_data['exam_id'],
            'date': self._get_normalized_date(api_date),
        }

    def _get_class_formation_data(self, api_data: Dict, api_date: str) -> Dict:
        return {
            'starts_at': self._get_digitized_time(api_data['start_at']),
            'ends_at': self._get_digitized_time(api_data['end_at']),
            'weekday': self._get_normalized_date(api_date).weekday(),
            'room_number': api_data['room_number'],
        }

    def _get_exam_list_items(self, api_data: Dict) -> List[Dict]:
        return [{
            'student': {
                'id': item['id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
            },
            'exam_id': api_data['exam_id'],
            'chair_number': item['chair_number'],
        } for item in api_data['students']]

    def _get_course_data(self, api_data: Dict) -> Dict:
        return {
            'name': api_data['course_name'],
            'professor': {
                'first_name': api_data['professor']['first_name'],
                'last_name': api_data['professor']['last_name'],
                'id': api_data['professor']['id'],
            }
        }

    def _get_classified_data(self, api_data: Dict, api_date: str) -> Dict:
        result = {
            **self._get_basic_exam_data(api_data, api_date),
            'formation': self._get_class_formation_data(api_data, api_date),
            'items': self._get_exam_list_items(api_data),
            'course': self._get_course_data(api_data)
        }
        return result

    def post(self, request):
        data = requests.get(settings.EXAM_LIST_URL).json()
        for exam in data['classes']:
            classified_data = self._get_classified_data(exam, data['date'])
            serializer = ExamSerializer(data=classified_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return redirect('exams-list')


class ExamListView(ListView):
    model = Exam
    template_name = 'exam_list_view.html'


class ExamDetailView(UpdateView):
    model = Exam
    template_name = 'exam_detail_view.html'
    fields = ['state']

    def get_success_url(self):
        return reverse('exam-detail', kwargs={'pk': self.object.id})


class ExamListItemUpdateView(UpdateView):
    model = ExamListItem
    template_name = 'exam_list_item_update_view.html'
    fields = ['state']

    def get_success_url(self):
        return reverse('exam-detail', kwargs={'pk': self.object.exam_id})


class VerifyExamView(ViewSet):
    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        exam.is_sent_to_shit = True
        exam.save()
        body = {
            'exam_id': exam.pk,
            'is_teacher_signed': str(exam.state == 'Verified').lower(),
            'present_students_list': list(exam.items.values_list('student__id', flat=True))
        }
        requests.post(settings.EXAM_LIST_URL, data=body)
        return redirect('exam-detail', pk=exam.pk)
