from django.urls import path

from core.views import FetchExams, VerifyExamView, ExamListView, ExamDetailView, \
    ExamListItemUpdateView



urlpatterns = [
    path('', FetchExams.as_view({'post': 'post'}), name='fetch-exams'),
    path('exams/', ExamListView.as_view(), name='exams-list'),
    path('exams/<pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('exam-list_item/<pk>/', ExamListItemUpdateView.as_view(), name='exam-item-update'),
    path('<pk>/', VerifyExamView.as_view({'post': 'post'}), name='verify-exam'),

]
