from django.urls import path

from core.views import FetchExams

urlpatterns = [
    path('', FetchExams.as_view({'get': 'post'})),
]
