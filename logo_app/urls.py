from django.urls import path
from . import views

app_name = 'logo_app'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('generate/', views.generate, name='generate'),
    path('gallery/', views.gallery, name='gallery'),
    path('result/<uuid:request_id>/', views.result, name='result'),
    path('logo/<uuid:logo_id>/', views.logo_detail, name='logo_detail'),
    
    # AJAX endpoints
    path('api/generate/', views.handle_logo_generation, name='api_generate'),
    path('api/feedback/<uuid:logo_id>/', views.submit_feedback, name='api_feedback'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/analytics/', views.analytics, name='api_analytics'),
    
    # Download
    path('download/<uuid:logo_id>/', views.download_logo, name='download_logo'),
]