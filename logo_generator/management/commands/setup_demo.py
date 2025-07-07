from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from logo_generator.models import LogoRequest, GeneratedLogo, UserProfile

class Command(BaseCommand):
    help = 'Setup demo data for AI LogoMaker'

    def handle(self, *args, **options):
        self.stdout.write('Setting up demo data...')
        
        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@logomaker.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            UserProfile.objects.create(user=demo_user, credits=10)
            self.stdout.write('Demo user created: demo/demo123')
        
        # Create sample logo requests
        sample_companies = [
            {'name': 'TechCorp', 'industry': 'technology', 'style': 'modern', 'color': 'blue'},
            {'name': 'GreenLeaf', 'industry': 'food', 'style': 'vintage', 'color': 'green'},
            {'name': 'MinimalCo', 'industry': 'consulting', 'style': 'minimalist', 'color': 'black'},
            {'name': 'CreativeHub', 'industry': 'creative', 'style': 'creative', 'color': 'rainbow'},
            {'name': 'ElegantDesign', 'industry': 'retail', 'style': 'elegant', 'color': 'purple'},
        ]
        
        for company in sample_companies:
            LogoRequest.objects.get_or_create(
                company_name=company['name'],
                defaults={
                    'user': demo_user,
                    'industry': company['industry'],
                    'style': company['style'],
                    'color_scheme': company['color'],
                    'description': f'Professional logo for {company["name"]}',
                    'is_processed': True
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('Demo data setup complete!')
        )