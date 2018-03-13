from django.urls import path

from . import views

app_name = 'weather_app'
urlpatterns = [
    path('', views.register_email, name='index'),
    path('register', views.register_email, name='register'),
    path('confirm', views.confirm, name='confirm'),
]