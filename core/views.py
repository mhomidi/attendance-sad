from datetime import datetime
from typing import Dict, List

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
        result = []
        for exam in data['classes']:
            classified_data = self._get_classified_data(exam, data['date'])
            serializer = ExamSerializer(data=classified_data)
            serializer.is_valid(raise_exception=True)
            result.append(serializer.save())
        return Response(ExamSerializer(result, many=True).data)
