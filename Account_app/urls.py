from Account_app.views import RegisterView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view())
]
