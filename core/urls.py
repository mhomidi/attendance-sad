from django.urls import path

from core.views import test_view

urlpatterns = [
    path('', test_view),
]
