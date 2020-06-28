from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .emailBackend import emailBackend
from django.contrib import messages
# Create your views here.
def showDemoPage(request):
    return render(request, 'demo.html')


def showLoginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = emailBackend.authenticate(request, username=email, password=password)
        if user != None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponse("Staff login"+str(user.user_type))
            else:
                return HttpResponse("Studentlogin"+str(user.user_type))
        else:
            messages.error(request,"Invalid login details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        user = request.user.email
        usertype = request.user.user_type
        return HttpResponse(user + usertype)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")