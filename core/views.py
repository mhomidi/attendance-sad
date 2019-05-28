from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ViewSet

from core.models import Exam


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class FetchExams(ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_digitized_time(self, time_str: str):
        h, m = time_str.split('h')
        h = h if len(h) > 1 else '0{}'.format(h)
        m = m if len(m) else '00'
        return '{}:{}'.format(h, m)

    def post(self, request):
        data = requests.get(settings.EXAM_LIST_URL).json()
        for exam in data['classes']:
            e, _ = Exam.objects.update_or_create(id=exam['exam_id'], defaults={
                'start_at': self._get_digitized_time(exam['start_at']),
                'end_at': self._get_digitized_time(exam['end_at']),
                'date': datetime.strptime(data['date'], '%a %b %d %Y'),
                'room_number': exam['room_number']
            })
            # TODO: Associate students and other shits

        return Response(UserSerializer(request.user).data)
