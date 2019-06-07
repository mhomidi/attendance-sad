from django.urls import path

from core.views import FetchExams, VerifyExamView

urlpatterns = [
    path('', FetchExams.as_view({'get': 'post'})),
    path('<pk>/', VerifyExamView.as_view({'get': 'post'}))
]
