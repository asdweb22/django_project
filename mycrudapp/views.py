from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
import requests

from .models import Register

# Create your views here.


def index(request):

    return render(request, "index.html")


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        psw = request.POST['pass']

        userauth = Register.objects.filter(username=username, password=psw)
        if userauth:
            request.session['usernm'] = request.POST['username']
            return redirect('userdashborad')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        upass = request.POST['pass']
        ucpass = request.POST['cpass']

        if upass == ucpass:
            if Register.objects.filter(username=username).exists():
                messages.info(request, 'username Already taken')
                return redirect('register')
            elif Register.objects.filter(email=email).exists():
                messages.info(request, 'email Already taken')
                return redirect('register')
            else:
                user = Register(
                    username=username, password=upass, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User Created')
                return redirect('login')
        else:
            messages.info(request, 'Password not maching')
        return redirect('register')

    else:

        return render(request, 'register.html')


def userdashborad(request):
    if request.session.has_key('usernm'):
        s = Register.objects.filter(username=request.session["usernm"])
        return render(request, "userdashborad.html", {'res': s, 'sdata': request.session["usernm"]})
    else:
        return redirect('login')


def myadmin(request):
    userdata = Register.objects.all()

    return render(request, "myadmin.html", {'userdata': userdata})


def find(request):
    userid = request.GET["q"]

    # gives you all filtered records according your query
    # userdata = Register.objects.filter(id=userid)

    # gives you only single records according your query
    s = Register.objects.get(id=userid)

    return render(request, "find.html", {'s': s})


def updatedata(request):
    s = Register.objects.get(id=request.POST["txtid"])

    s.first_name = request.POST["fname"]
    s.last_name = request.POST["lname"]
    s.username = request.POST["username"]
    s.email = request.POST["email"]
    s.password = request.POST["pass"]

    s.save()
    messages.info(request, 'Data updated')

    return redirect('myadmin')


def delete(request):
    s = Register.objects.get(id=request.GET["q"])
    s.delete()

    messages.info(request, "Data deleted")
    return redirect('myadmin')


def logout(request):
    del request.session['usernm']
    return render(request, "index.html")


def news(request):
    if request.method == 'POST':
        c = request.POST['search']
        print(c)

        r = requests.get(
            f'https://newsapi.org/v2/top-headlines?country={c}&apiKey=899aea6e58a3481a8a66573524eb6c5a')
        res = r.json()
        data = res['articles']
        title = []
        description = []
        image = []
        url = []

        for i in data:
            title.append(i['title'])
            description.append(i['description'])
            image.append(i['urlToImage'])
            url.append(i['url'])

        news = zip(title, description, image, url)

        return render(request, "news.html", {'news': news, 'Country': c})

    return render(request, "news.html")


def certificates(request):
    # return HttpResponse("This is service page")
    return render(request, 'certificates.html')
