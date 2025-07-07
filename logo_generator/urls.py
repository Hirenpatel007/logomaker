from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('generate/', views.generate_logo, name='generate_logo'),
    path('gallery/', views.gallery, name='gallery'),
    path('profile/', views.profile, name='profile'),
    path('analytics/', views.logo_analytics, name='analytics'),
    path('download/<int:logo_id>/', views.download_logo, name='download_logo'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]