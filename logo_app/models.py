from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
import json

class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Industries"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class LogoStyle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    prompt_template = models.TextField(help_text="Base prompt template for this style")
    negative_prompt = models.TextField(blank=True, help_text="Negative prompt for this style")
    preview_image = models.ImageField(upload_to='style_previews/', blank=True)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class ColorScheme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    primary_color = models.CharField(max_length=7, help_text="Hex color code")
    secondary_color = models.CharField(max_length=7, blank=True)
    accent_color = models.CharField(max_length=7, blank=True)
    description = models.TextField(blank=True)
    prompt_keywords = models.CharField(max_length=200, help_text="Keywords for AI prompt")
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    credits = models.IntegerField(default=3)
    is_premium = models.BooleanField(default=False)
    premium_expires = models.DateTimeField(null=True, blank=True)
    total_logos_generated = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def has_credits(self):
        return self.credits > 0 or self.is_premium
    
    def deduct_credit(self):
        if not self.is_premium and self.credits > 0:
            self.credits -= 1
            self.save()

class LogoRequest(models.Model):
    PRIORITY_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express (24h)'),
        ('urgent', 'Urgent (6h)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, help_text="For anonymous users")
    
    # Business Information
    business_name = models.CharField(max_length=200)
    business_description = models.TextField(blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    
    # Design Preferences
    style = models.ForeignKey(LogoStyle, on_delete=models.CASCADE)
    color_scheme = models.ForeignKey(ColorScheme, on_delete=models.CASCADE)
    additional_colors = models.CharField(max_length=200, blank=True)
    
    # AI Generation Settings
    custom_prompt = models.TextField(blank=True, help_text="Additional prompt details")
    final_prompt = models.TextField(blank=True, help_text="Generated final prompt")
    negative_prompt = models.TextField(blank=True)
    variations_count = models.IntegerField(default=4)
    
    # Request Details
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='standard')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Logo for {self.business_name}"
    
    def get_absolute_url(self):
        return reverse('logo_app:result', kwargs={'request_id': self.id})

class GeneratedLogo(models.Model):
    request = models.ForeignKey(LogoRequest, on_delete=models.CASCADE, related_name='logos')
    image = models.ImageField(upload_to='logos/%Y/%m/')
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/', blank=True)
    
    # AI Generation Details
    seed = models.BigIntegerField(null=True, blank=True)
    steps = models.IntegerField(default=30)
    cfg_scale = models.FloatField(default=7.5)
    sampler = models.CharField(max_length=50, blank=True)
    model_used = models.CharField(max_length=100, blank=True)
    generation_time = models.FloatField(null=True, blank=True, help_text="Time in seconds")
    
    # Quality Metrics
    quality_score = models.IntegerField(default=0, help_text="AI quality assessment 0-100")
    user_rating = models.IntegerField(null=True, blank=True, help_text="User rating 1-5")
    
    # Usage Stats
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    # Metadata
    file_size = models.IntegerField(null=True, blank=True, help_text="File size in bytes")
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Logo {self.id} for {self.request.business_name}"
    
    def get_absolute_url(self):
        return reverse('logo_app:logo_detail', kwargs={'logo_id': self.id})
    
    def increment_view(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def increment_download(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])

class PromptHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    raw_prompt = models.TextField()
    final_prompt = models.TextField()
    negative_prompt = models.TextField(blank=True)
    style = models.ForeignKey(LogoStyle, on_delete=models.CASCADE, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    success_rate = models.FloatField(default=0.0, help_text="Success rate of this prompt")
    usage_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prompt: {self.raw_prompt[:50]}..."

class LogoFeedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    logo = models.ForeignKey(GeneratedLogo, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    is_helpful = models.BooleanField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['logo', 'user', 'session_key']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback for {self.logo} - {self.rating} stars"

class AIModelConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    model_path = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    # Model Settings
    default_steps = models.IntegerField(default=30)
    default_cfg_scale = models.FloatField(default=7.5)
    default_sampler = models.CharField(max_length=50, default='DPM++ 2M Karras')
    
    # Performance Metrics
    average_generation_time = models.FloatField(null=True, blank=True)
    success_rate = models.FloatField(default=0.0)
    total_generations = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return self.name

class SystemStats(models.Model):
    date = models.DateField(unique=True)
    total_requests = models.IntegerField(default=0)
    successful_generations = models.IntegerField(default=0)
    failed_generations = models.IntegerField(default=0)
    unique_users = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    average_generation_time = models.FloatField(default=0.0)
    most_popular_style = models.CharField(max_length=100, blank=True)
    most_popular_industry = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "System Statistics"
    
    def __str__(self):
        return f"Stats for {self.date}"