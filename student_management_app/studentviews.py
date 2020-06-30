from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import * 

def student_home(request):
    return render(request,'student_template/student_home.html')