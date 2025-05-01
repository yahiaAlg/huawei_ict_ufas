from django.urls import  path
from .views import *
urlpatterns = [
    path("", IndexView.as_view() , name="index"),
    path('contact/', contact_view, name='contact'),
    path("about/", about , name="about"),
]
