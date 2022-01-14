from django.urls import path, include
from mycrudapp import views

urlpatterns = [

    path("", views.index, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('userdashborad', views.userdashborad, name="userdashborad"),
    path('myadmin', views.myadmin, name="myadmin"),
    path('find', views.find, name="find"),
    path('updatedata', views.updatedata, name="updatedata"),
    path('delete', views.delete, name="delete"),
    path('logout', views.logout, name="logout"),
    path("news", views.news, name="news"),
    path("certificates", views.certificates, name="certificates"),

]
