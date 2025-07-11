"""
Professional Template System for LogoMaker Pro
Manages logo templates with categories, ratings, and customization
Created by Hiren Patel
"""

from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from django.core.files.base import ContentFile

class TemplateCategory(models.Model):
    """Categories for organizing logo templates"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    is_featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Template Categories"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class LogoTemplate(models.Model):
    """Professional logo templates"""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy to Customize'),
        ('medium', 'Medium Complexity'),
        ('advanced', 'Advanced Design')
    ]
    
    STYLE_CHOICES = [
        ('modern', 'Modern'),
        ('vintage', 'Vintage'),
        ('minimalist', 'Minimalist'),
        ('corporate', 'Corporate'),
        ('creative', 'Creative'),
        ('tech', 'Technology'),
        ('elegant', 'Elegant'),
        ('playful', 'Playful'),
        ('bold', 'Bold'),
        ('classic', 'Classic')
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, related_name='templates')
    
    # Template files
    preview_image = models.ImageField(upload_to='templates/previews/')
    template_svg = models.FileField(upload_to='templates/svg/', blank=True, null=True)
    template_png = models.ImageField(upload_to='templates/png/')
    
    # Metadata
    style = models.CharField(max_length=20, choices=STYLE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    primary_color = models.CharField(max_length=7, default='#3B82F6')
    secondary_color = models.CharField(max_length=7, default='#1E40AF')
    accent_color = models.CharField(max_length=7, blank=True, null=True)
    
    # Usage and popularity
    download_count = models.IntegerField(default=0)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    # Features
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    
    # Customization options
    allow_text_edit = models.BooleanField(default=True)
    allow_color_change = models.BooleanField(default=True)
    allow_icon_change = models.BooleanField(default=False)
    
    # SEO and organization
    tags = models.CharField(max_length=500, help_text="Comma-separated tags")
    industries = models.CharField(max_length=300, help_text="Suitable industries")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-rating_average', '-download_count']
    
    def __str__(self):
        return self.name
    
    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def increment_download(self):
        """Increment download count"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
    
    def get_tags_list(self):
        """Get tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_industries_list(self):
        """Get industries as a list"""
        return [industry.strip() for industry in self.industries.split(',') if industry.strip()]

class TemplateRating(models.Model):
    """Template ratings and reviews"""
    template = models.ForeignKey(LogoTemplate, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['template', 'user', 'session_key']

class TemplateCustomization(models.Model):
    """Store customized templates"""
    template = models.ForeignKey(LogoTemplate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    
    # Customization data
    custom_text = models.CharField(max_length=200, blank=True)
    custom_colors = models.JSONField(default=dict)  # Store color modifications
    custom_settings = models.JSONField(default=dict)  # Store other modifications
    
    # Generated files
    customized_image = models.ImageField(upload_to='templates/customized/')
    
    created_at = models.DateTimeField(auto_now_add=True)

class TemplateCollection(models.Model):
    """Curated collections of templates"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='collections/')
    templates = models.ManyToManyField(LogoTemplate, related_name='collections')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TemplateManager:
    """Template management utility class"""
    
    @staticmethod
    def search_templates(query, category=None, style=None, industry=None, limit=20):
        """Search templates with filters"""
        templates = LogoTemplate.objects.all()
        
        if query:
            templates = templates.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(tags__icontains=query)
            )
        
        if category:
            templates = templates.filter(category__slug=category)
        
        if style:
            templates = templates.filter(style=style)
        
        if industry:
            templates = templates.filter(industries__icontains=industry)
        
        return templates[:limit]
    
    @staticmethod
    def get_featured_templates(limit=12):
        """Get featured templates"""
        return LogoTemplate.objects.filter(is_featured=True)[:limit]
    
    @staticmethod
    def get_trending_templates(limit=12):
        """Get trending templates"""
        return LogoTemplate.objects.filter(is_trending=True)[:limit]
    
    @staticmethod
    def get_popular_templates(limit=12):
        """Get most popular templates"""
        return LogoTemplate.objects.order_by('-download_count', '-rating_average')[:limit]
    
    @staticmethod
    def get_new_templates(limit=12):
        """Get newest templates"""
        return LogoTemplate.objects.filter(is_new=True).order_by('-created_at')[:limit]
    
    @staticmethod
    def get_recommendations_for_business(business_description, industry=None, limit=8):
        """Get template recommendations based on business context"""
        templates = LogoTemplate.objects.all()
        
        # Filter by industry if provided
        if industry:
            templates = templates.filter(industries__icontains=industry)
        
        # Score templates based on business description keywords
        scored_templates = []
        
        for template in templates:
            score = 0
            
            # Check description keywords
            description_words = business_description.lower().split()
            template_keywords = (template.tags + ' ' + template.description).lower()
            
            for word in description_words:
                if len(word) > 3 and word in template_keywords:
                    score += 1
            
            # Boost score for popular templates
            score += template.rating_average * 0.5
            score += min(template.download_count / 100, 5)
            
            if score > 0:
                scored_templates.append((template, score))
        
        # Sort by score and return top results
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        return [template for template, score in scored_templates[:limit]]

class TemplateGenerator:
    """Generate programmatic templates"""
    
    @staticmethod
    def generate_text_logo(text, font_size=72, color='#3B82F6', bg_color='white'):
        """Generate a simple text-based logo template"""
        try:
            # Create image
            img_width, img_height = 400, 200
            image = Image.new('RGB', (img_width, img_height), bg_color)
            draw = ImageDraw.Draw(image)
            
            # Try to use a nice font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position for centering
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, fill=color, font=font)
            
            # Save to ContentFile
            img_io = io.BytesIO()
            image.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue(), name=f'{text}_logo.png')
            
            return img_file
            
        except Exception as e:
            print(f"Error generating text logo: {e}")
            return None
    
    @staticmethod
    def generate_geometric_logo(shape='circle', size=200, color='#3B82F6', bg_color='white'):
        """Generate geometric shape logos"""
        try:
            image = Image.new('RGB', (size, size), bg_color)
            draw = ImageDraw.Draw(image)
            
            margin = size // 8
            
            if shape == 'circle':
                draw.ellipse([margin, margin, size-margin, size-margin], fill=color)
            elif shape == 'square':
                draw.rectangle([margin, margin, size-margin, size-margin], fill=color)
            elif shape == 'triangle':
                points = [
                    (size//2, margin),
                    (margin, size-margin),
                    (size-margin, size-margin)
                ]
                draw.polygon(points, fill=color)
            
            # Save to ContentFile
            img_io = io.BytesIO()
            image.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue(), name=f'{shape}_logo.png')
            
            return img_file
            
        except Exception as e:
            print(f"Error generating geometric logo: {e}")
            return None

# Initial template data
INITIAL_TEMPLATES = [
    {
        "name": "Modern Tech Logo",
        "description": "Clean and modern logo perfect for technology companies",
        "category": "technology",
        "style": "modern",
        "tags": "tech, software, digital, clean, modern, corporate",
        "industries": "Technology, Software, Digital Services",
        "primary_color": "#3B82F6",
        "secondary_color": "#1E40AF"
    },
    {
        "name": "Creative Studio Badge",
        "description": "Artistic badge design for creative agencies and studios",
        "category": "creative",
        "style": "creative",
        "tags": "creative, artistic, studio, agency, design, modern",
        "industries": "Design, Creative, Marketing, Advertising",
        "primary_color": "#8B5CF6",
        "secondary_color": "#7C3AED"
    },
    {
        "name": "Corporate Shield",
        "description": "Professional shield logo for established businesses",
        "category": "corporate",
        "style": "corporate",
        "tags": "corporate, professional, shield, trust, business, established",
        "industries": "Finance, Consulting, Legal, Insurance",
        "primary_color": "#374151",
        "secondary_color": "#1F2937"
    },
    {
        "name": "Health Plus Cross",
        "description": "Medical cross design for healthcare providers",
        "category": "healthcare",
        "style": "minimalist",
        "tags": "medical, health, cross, care, hospital, clinic",
        "industries": "Healthcare, Medical, Wellness, Pharmacy",
        "primary_color": "#10B981",
        "secondary_color": "#059669"
    },
    {
        "name": "Food & Restaurant Emblem",
        "description": "Elegant emblem for restaurants and food businesses",
        "category": "food",
        "style": "elegant",
        "tags": "food, restaurant, cooking, chef, dining, elegant",
        "industries": "Restaurant, Food, Catering, Hospitality",
        "primary_color": "#F59E0B",
        "secondary_color": "#D97706"
    }
]