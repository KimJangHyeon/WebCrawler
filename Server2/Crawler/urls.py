from django.urls import path

from Crawler.views import SignUp

urlpatterns = [
    path('SignUp', SignUp.as_view()),
]
