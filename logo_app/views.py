from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.conf import settings
import json
import logging
import requests
import base64
import io
from PIL import Image
from .models import (
    LogoRequest, GeneratedLogo, Industry, LogoStyle, ColorScheme,
    UserProfile, PromptHistory, LogoFeedback, SystemStats
)
from .utils.stable_diffusion import StableDiffusionAPI
from .utils.prompt_generator import PromptGenerator
from .forms import LogoGenerationForm, FeedbackForm

logger = logging.getLogger(__name__)

def home(request):
    """Homepage with dynamic content"""
    
    # Get featured logos
    featured_logos = GeneratedLogo.objects.filter(
        is_featured=True, is_public=True
    ).select_related('request')[:8]
    
    # Get statistics
    stats = {
        'total_logos': GeneratedLogo.objects.count(),
        'happy_customers': UserProfile.objects.count(),
        'industries_served': Industry.objects.filter(is_active=True).count(),
        'ai_models': 5,  # Number of AI models available
    }
    
    # Get popular styles
    popular_styles = LogoStyle.objects.filter(
        is_active=True
    ).annotate(
        usage_count=Count('logorequest')
    ).order_by('-usage_count')[:6]
    
    context = {
        'featured_logos': featured_logos,
        'stats': stats,
        'popular_styles': popular_styles,
        'business_info': settings.BUSINESS_INFO,
    }
    
    return render(request, 'logo_app/home.html', context)

def generate(request):
    """Logo generation page with dynamic form"""
    
    if request.method == 'POST':
        return handle_logo_generation(request)
    
    # Get form data
    industries = Industry.objects.filter(is_active=True).order_by('name')
    styles = LogoStyle.objects.filter(is_active=True).order_by('sort_order', 'name')
    color_schemes = ColorScheme.objects.filter(is_active=True).order_by('sort_order', 'name')
    
    # Check user credits
    user_credits = 0
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_credits = profile.credits if not profile.is_premium else 999
    
    context = {
        'industries': industries,
        'styles': styles,
        'color_schemes': color_schemes,
        'user_credits': user_credits,
        'form': LogoGenerationForm(),
    }
    
    return render(request, 'logo_app/generate.html', context)

@csrf_exempt
def handle_logo_generation(request):
    """Handle AJAX logo generation request"""
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        business_name = data.get('business_name', '').strip()
        if not business_name:
            return JsonResponse({
                'success': False,
                'error': 'Business name is required'
            })
        
        # Check user credits
        if request.user.is_authenticated:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            if not profile.has_credits():
                return JsonResponse({
                    'success': False,
                    'error': 'Insufficient credits. Please upgrade or purchase more credits.'
                })
        
        # Get form data
        industry_id = data.get('industry')
        style_id = data.get('style')
        color_scheme_id = data.get('color_scheme')
        business_description = data.get('business_description', '')
        custom_prompt = data.get('custom_prompt', '')
        variations_count = min(int(data.get('variations_count', 4)), 8)
        
        # Get objects
        industry = get_object_or_404(Industry, id=industry_id, is_active=True)
        style = get_object_or_404(LogoStyle, id=style_id, is_active=True)
        color_scheme = get_object_or_404(ColorScheme, id=color_scheme_id, is_active=True)
        
        # Create logo request
        logo_request = LogoRequest.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key,
            business_name=business_name,
            business_description=business_description,
            industry=industry,
            style=style,
            color_scheme=color_scheme,
            custom_prompt=custom_prompt,
            variations_count=variations_count,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            status='processing'
        )
        
        # Generate prompts
        prompt_generator = PromptGenerator()
        prompts = prompt_generator.generate_prompts(
            business_name=business_name,
            business_description=business_description,
            industry=industry,
            style=style,
            color_scheme=color_scheme,
            custom_prompt=custom_prompt,
            variations_count=variations_count
        )
        
        # Store final prompt
        logo_request.final_prompt = prompts[0]['positive']
        logo_request.negative_prompt = prompts[0]['negative']
        logo_request.save()
        
        # Generate logos using Stable Diffusion
        sd_api = StableDiffusionAPI()
        generated_logos = []
        
        for i, prompt_data in enumerate(prompts):
            try:
                # Generate image
                result = sd_api.generate_image(
                    positive_prompt=prompt_data['positive'],
                    negative_prompt=prompt_data['negative'],
                    width=512,
                    height=512,
                    steps=30,
                    cfg_scale=7.5
                )
                
                if result['success']:
                    # Save generated logo
                    logo = GeneratedLogo.objects.create(
                        request=logo_request,
                        image=result['image_file'],
                        seed=result.get('seed'),
                        steps=result.get('steps', 30),
                        cfg_scale=result.get('cfg_scale', 7.5),
                        sampler=result.get('sampler', ''),
                        model_used=result.get('model', ''),
                        generation_time=result.get('generation_time', 0),
                        quality_score=result.get('quality_score', 85),
                        file_size=result.get('file_size', 0),
                        image_width=result.get('width', 512),
                        image_height=result.get('height', 512)
                    )
                    
                    generated_logos.append({
                        'id': str(logo.id),
                        'image_url': logo.image.url,
                        'quality_score': logo.quality_score,
                        'generation_time': logo.generation_time,
                        'variation_id': i + 1
                    })
                    
            except Exception as e:
                logger.error(f"Error generating logo variation {i}: {str(e)}")
                continue
        
        if generated_logos:
            # Update request status
            logo_request.status = 'completed'
            logo_request.completed_at = timezone.now()
            logo_request.save()
            
            # Deduct user credit
            if request.user.is_authenticated:
                profile.deduct_credit()
                profile.total_logos_generated += len(generated_logos)
                profile.save()
            
            # Save prompt history
            PromptHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                raw_prompt=custom_prompt,
                final_prompt=logo_request.final_prompt,
                negative_prompt=logo_request.negative_prompt,
                style=style,
                industry=industry,
                success_rate=len(generated_logos) / variations_count * 100
            )
            
            return JsonResponse({
                'success': True,
                'request_id': str(logo_request.id),
                'logos': generated_logos,
                'total_generated': len(generated_logos),
                'generation_time': sum(logo.get('generation_time', 0) for logo in generated_logos),
                'redirect_url': f'/result/{logo_request.id}/'
            })
        else:
            logo_request.status = 'failed'
            logo_request.save()
            
            return JsonResponse({
                'success': False,
                'error': 'Failed to generate logos. Please try again with different parameters.'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request data'
        })
    except Exception as e:
        logger.error(f"Error in logo generation: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred. Please try again.'
        })

def result(request, request_id):
    """Display generated logos"""
    
    logo_request = get_object_or_404(LogoRequest, id=request_id)
    logos = logo_request.logos.all().order_by('-quality_score')
    
    # Check if user has access to this request
    if logo_request.user and logo_request.user != request.user:
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to view this request.')
            return redirect('logo_app:home')
    
    context = {
        'logo_request': logo_request,
        'logos': logos,
        'total_logos': logos.count(),
        'feedback_form': FeedbackForm(),
    }
    
    return render(request, 'logo_app/result.html', context)

def gallery(request):
    """Public gallery of logos"""
    
    # Get filter parameters
    style_filter = request.GET.get('style')
    industry_filter = request.GET.get('industry')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Base queryset
    logos = GeneratedLogo.objects.filter(
        is_public=True
    ).select_related('request', 'request__industry', 'request__style')
    
    # Apply filters
    if style_filter:
        logos = logos.filter(request__style__slug=style_filter)
    
    if industry_filter:
        logos = logos.filter(request__industry__slug=industry_filter)
    
    if search_query:
        logos = logos.filter(
            Q(request__business_name__icontains=search_query) |
            Q(request__business_description__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'popular':
        logos = logos.order_by('-view_count', '-download_count')
    elif sort_by == 'rating':
        logos = logos.annotate(avg_rating=Avg('feedback__rating')).order_by('-avg_rating')
    else:
        logos = logos.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(logos, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    styles = LogoStyle.objects.filter(is_active=True).order_by('name')
    industries = Industry.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'styles': styles,
        'industries': industries,
        'current_style': style_filter,
        'current_industry': industry_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_logos': logos.count(),
    }
    
    return render(request, 'logo_app/gallery.html', context)

def logo_detail(request, logo_id):
    """Individual logo detail page"""
    
    logo = get_object_or_404(GeneratedLogo, id=logo_id, is_public=True)
    
    # Increment view count
    logo.increment_view()
    
    # Get related logos
    related_logos = GeneratedLogo.objects.filter(
        request__industry=logo.request.industry,
        is_public=True
    ).exclude(id=logo.id)[:6]
    
    # Get feedback
    feedback = logo.feedback.all().order_by('-created_at')
    
    context = {
        'logo': logo,
        'related_logos': related_logos,
        'feedback': feedback,
        'feedback_form': FeedbackForm(),
    }
    
    return render(request, 'logo_app/logo_detail.html', context)

def download_logo(request, logo_id):
    """Download logo file"""
    
    logo = get_object_or_404(GeneratedLogo, id=logo_id)
    
    # Check permissions
    if not logo.is_public and logo.request.user != request.user:
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to download this logo.')
            return redirect('logo_app:gallery')
    
    # Increment download count
    logo.increment_download()
    
    # Prepare response
    response = HttpResponse(logo.image.read(), content_type='image/png')
    filename = f"{logo.request.business_name}_logo_{logo.id}.png"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@csrf_exempt
def submit_feedback(request, logo_id):
    """Submit feedback for a logo"""
    
    if request.method == 'POST':
        logo = get_object_or_404(GeneratedLogo, id=logo_id)
        
        try:
            data = json.loads(request.body)
            rating = int(data.get('rating', 0))
            comment = data.get('comment', '').strip()
            
            if not 1 <= rating <= 5:
                return JsonResponse({
                    'success': False,
                    'error': 'Rating must be between 1 and 5'
                })
            
            # Create or update feedback
            feedback, created = LogoFeedback.objects.get_or_create(
                logo=logo,
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else '',
                defaults={
                    'rating': rating,
                    'comment': comment,
                    'ip_address': get_client_ip(request)
                }
            )
            
            if not created:
                feedback.rating = rating
                feedback.comment = comment
                feedback.save()
            
            # Update logo's user rating
            avg_rating = logo.feedback.aggregate(Avg('rating'))['rating__avg']
            logo.user_rating = round(avg_rating) if avg_rating else rating
            logo.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Failed to submit feedback'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def api_status(request):
    """API status endpoint"""
    
    sd_api = StableDiffusionAPI()
    status = sd_api.check_status()
    
    return JsonResponse({
        'stable_diffusion': status,
        'database': True,  # If we reach here, DB is working
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    })

def analytics(request):
    """Analytics data for dashboard"""
    
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Get recent stats
    today = timezone.now().date()
    stats = SystemStats.objects.filter(date=today).first()
    
    if not stats:
        # Create today's stats
        stats = SystemStats.objects.create(
            date=today,
            total_requests=LogoRequest.objects.count(),
            successful_generations=LogoRequest.objects.filter(status='completed').count(),
            failed_generations=LogoRequest.objects.filter(status='failed').count(),
            unique_users=UserProfile.objects.count(),
            total_downloads=GeneratedLogo.objects.aggregate(
                total=models.Sum('download_count')
            )['total'] or 0
        )
    
    return JsonResponse({
        'total_requests': stats.total_requests,
        'successful_generations': stats.successful_generations,
        'failed_generations': stats.failed_generations,
        'success_rate': (stats.successful_generations / max(stats.total_requests, 1)) * 100,
        'unique_users': stats.unique_users,
        'total_downloads': stats.total_downloads,
        'popular_styles': list(
            LogoStyle.objects.annotate(
                usage_count=Count('logorequest')
            ).values('name', 'usage_count').order_by('-usage_count')[:5]
        ),
        'popular_industries': list(
            Industry.objects.annotate(
                usage_count=Count('logorequest')
            ).values('name', 'usage_count').order_by('-usage_count')[:5]
        )
    })

# Utility functions
def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip