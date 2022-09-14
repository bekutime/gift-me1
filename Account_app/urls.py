from Account_app.views import RegisterView, LoginView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('auth/', LoginView.as_view())
    # path('verify-email/', VerifyEmail.as_view(), name="verify-email")
]
