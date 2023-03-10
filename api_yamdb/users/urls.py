from django.urls import path

from users.views import APIUserSignup, CustomTokenViewBase


app_name = 'users'

urlpatterns = [
    path('auth/signup/', APIUserSignup.as_view()),
    path('auth/token/', CustomTokenViewBase.as_view()),
]
