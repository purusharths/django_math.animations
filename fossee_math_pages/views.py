from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "fossee_math_pages/index.html")

def pagenotfound(request):
    return render(request, "fossee_math_pages/404.html")

def internship(request):
    return render(request, "fossee_math_pages/internship.html")

def real_number_line(request):
    return render(request, "fossee_math_pages/real_number_line).html")

def realanalysis(request):
    return render(request, "fossee_math_pages/realanalysis.html")

def topics(request):
    return render(request, "fossee_math_pages/topics.html")

