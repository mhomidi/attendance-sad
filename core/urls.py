from django.urls import path

from core.views import FetchExams, VerifyExamView

urlpatterns = [
    path('', FetchExams.as_view({'post': 'post'})),
    path('<pk>/', VerifyExamView.as_view({'post': 'post'}))
]
