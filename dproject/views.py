from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from dproject.models import information, link
from django.db import connection

# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def authenticate_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('insert_credentials'))
            else:
                return HttpResponse("account not active")
        else:
            print("someone tried to login")
    else:
        return render(request, 'authenticate_user.html', context={'insert me': 'please insert me'})


@login_required
def insert_credentials(request):

    if request.method == "POST":
        print("in request post")
        info = information()
        info.designation = request.POST['designation']
        info.name = request.POST['name']
        info.save()
        with connection.cursor() as cursor:
            cursor.execute('select link from dproject_link where SNo = (select MAX(SNo) from dproject_link)')
            value = dictfetchall(cursor)[0]
        usable = value['link']
        return HttpResponseRedirect(usable)

    else:

        return render(request, 'input_credentials.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('authenticate'))
