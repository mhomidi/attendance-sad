from datetime import datetime
from typing import Dict

import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

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

    def _translate_exam_basic_data(self, api_data: Dict, api_date: str) -> Dict:
        return {
            'id': api_data['exam_id'],
            'room_number': api_data['room_number'],
            'start_at': self._get_digitized_time(api_data['start_at']),
            'end_at': self._get_digitized_time(api_data['end_at']),
            'date': self._get_normalized_date(api_date),
        }

    def post(self, request):
        data = requests.get(settings.EXAM_LIST_URL).json()
        result = []
        for exam in data['classes']:
            translated_data = self._translate_exam_basic_data(exam, data['date'])
            serializer = ExamSerializer(data=translated_data)
            serializer.is_valid(raise_exception=True)
            result.append(serializer.save())
            # TODO: Associate students and other shits

        return Response(ExamSerializer(result, many=True).data)
