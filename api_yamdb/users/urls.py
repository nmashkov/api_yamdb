from django.urls import path

from users.views import APIUserSignup, CustomTokenViewBase


app_name = 'users'

urlpatterns = [
    path('signup/', APIUserSignup.as_view()),
    path('token/', CustomTokenViewBase.as_view()),
]
