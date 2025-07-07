from django.db import models
from logo_generator.models import LogoRequest, GeneratedLogo

class AIModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    api_endpoint = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} v{self.version}"

class GenerationTask(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    logo_request = models.ForeignKey(LogoRequest, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    progress = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Task {self.id} - {self.status}"

class AIPrompt(models.Model):
    generation_task = models.ForeignKey(GenerationTask, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    negative_prompt = models.TextField(blank=True)
    style_weight = models.FloatField(default=1.0)
    color_weight = models.FloatField(default=1.0)
    creativity_level = models.FloatField(default=0.7)
    
    def __str__(self):
        return f"Prompt for Task {self.generation_task.id}"

class AIAnalytics(models.Model):
    date = models.DateField(auto_now_add=True)
    total_generations = models.IntegerField(default=0)
    successful_generations = models.IntegerField(default=0)
    failed_generations = models.IntegerField(default=0)
    average_generation_time = models.FloatField(default=0)
    most_popular_style = models.CharField(max_length=50, blank=True)
    most_popular_industry = models.CharField(max_length=50, blank=True)
    
    class Meta:
        unique_together = ['date']
    
    def __str__(self):
        return f"Analytics for {self.date}"