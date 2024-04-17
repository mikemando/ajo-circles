from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path('circle/create', views.CircleCreationView.as_view(), name='create_circle')
]
