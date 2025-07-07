from django.db import models
from django.contrib.auth.models import User
import uuid

class Industry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

class LogoStyle(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='style_previews/', blank=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class ColorScheme(models.Model):
    name = models.CharField(max_length=50)
    primary_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
    accent_color = models.CharField(max_length=7, blank=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    credits = models.IntegerField(default=3)
    is_premium = models.BooleanField(default=False)
    subscription_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

class LogoRequest(models.Model):
    PRIORITY_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express (24h)'),
        ('urgent', 'Urgent (6h)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    style = models.ForeignKey(LogoStyle, on_delete=models.CASCADE)
    color_scheme = models.ForeignKey(ColorScheme, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='standard')
    variations_count = models.IntegerField(default=5)
    include_business_card = models.BooleanField(default=False)
    include_letterhead = models.BooleanField(default=False)
    include_social_media = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Logo for {self.company_name}"

class GeneratedLogo(models.Model):
    request = models.ForeignKey(LogoRequest, on_delete=models.CASCADE, related_name='logos')
    image = models.ImageField(upload_to='logos/')
    vector_file = models.FileField(upload_to='vectors/', blank=True)
    ai_prompt = models.TextField()
    generation_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    is_favorite = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Logo {self.id} for {self.request.company_name}"

class LogoVariation(models.Model):
    logo = models.ForeignKey(GeneratedLogo, on_delete=models.CASCADE, related_name='variations')
    variation_type = models.CharField(max_length=50)  # horizontal, vertical, icon, etc.
    image = models.ImageField(upload_to='variations/')
    created_at = models.DateTimeField(auto_now_add=True)

class BusinessCard(models.Model):
    logo = models.ForeignKey(GeneratedLogo, on_delete=models.CASCADE)
    front_design = models.ImageField(upload_to='business_cards/')
    back_design = models.ImageField(upload_to='business_cards/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SocialMediaKit(models.Model):
    logo = models.ForeignKey(GeneratedLogo, on_delete=models.CASCADE)
    facebook_cover = models.ImageField(upload_to='social_media/')
    instagram_post = models.ImageField(upload_to='social_media/')
    twitter_header = models.ImageField(upload_to='social_media/')
    linkedin_banner = models.ImageField(upload_to='social_media/')
    created_at = models.DateTimeField(auto_now_add=True)

class LogoFeedback(models.Model):
    logo = models.ForeignKey(GeneratedLogo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AIPromptTemplate(models.Model):
    name = models.CharField(max_length=100)
    template = models.TextField()
    style = models.ForeignKey(LogoStyle, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name