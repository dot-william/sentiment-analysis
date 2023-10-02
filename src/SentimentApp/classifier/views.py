from django.shortcuts import render
from pathlib import Path
# Create your views here.
def home(request):
    
    return render(request, 'pages/home.html')