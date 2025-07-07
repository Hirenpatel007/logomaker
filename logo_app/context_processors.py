from django.conf import settings

def business_context(request):
    """Add business information to all templates"""
    return {
        'BUSINESS_INFO': settings.BUSINESS_INFO,
        'AI_CONFIG': settings.AI_CONFIG,
    }