from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'deployr2/index.html', {})


def start_deployment(request):
    return render(request, 'deployr2/start_deployment.html', {})