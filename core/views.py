from django.http import HttpResponse


# Create your views here.
def test_view(request):
    return HttpResponse('Test response')
