from django.contrib import admin
from .models import LogoRequest, GeneratedLogo, UserProfile

@admin.register(LogoRequest)
class LogoRequestAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'style', 'color_scheme', 'industry', 'created_at', 'is_processed']
    list_filter = ['style', 'color_scheme', 'industry', 'is_processed', 'created_at']
    search_fields = ['company_name', 'industry', 'description']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']

@admin.register(GeneratedLogo)
class GeneratedLogoAdmin(admin.ModelAdmin):
    list_display = ['request', 'generation_method', 'rating', 'is_favorite', 'created_at']
    list_filter = ['generation_method', 'rating', 'is_favorite', 'created_at']
    search_fields = ['request__company_name', 'ai_prompt']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'credits', 'created_at']
    list_filter = ['credits', 'created_at']
    search_fields = ['user__username', 'company']
    readonly_fields = ['created_at']