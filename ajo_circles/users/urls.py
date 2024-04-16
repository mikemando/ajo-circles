from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.BlacklistTokenUpdateView.as_view(), name='blacklist'),
]
