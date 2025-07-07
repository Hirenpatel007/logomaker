import io
import base64
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from django.core.files.base import ContentFile
import colorsys

class AILogoGenerator:
    def __init__(self):
        self.color_palettes = {
            'blue': ['#1E3A8A', '#3B82F6', '#60A5FA', '#93C5FD'],
            'red': ['#DC2626', '#EF4444', '#F87171', '#FCA5A5'],
            'green': ['#059669', '#10B981', '#34D399', '#6EE7B7'],
            'purple': ['#7C3AED', '#8B5CF6', '#A78BFA', '#C4B5FD'],
            'orange': ['#EA580C', '#F97316', '#FB923C', '#FED7AA'],
            'black': ['#000000', '#374151', '#6B7280', '#D1D5DB'],
            'rainbow': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        }
        
        self.fonts = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New']
        
    def generate_logo(self, logo_request):
        """Generate multiple logo variations using AI-driven algorithms"""
        logos = []
        
        # Generate 3 different logo variations
        for i in range(3):
            logo_data = self._create_logo_variation(logo_request, i)
            logos.append(logo_data)
            
        return logos
    
    def _create_logo_variation(self, request, variation_id):
        """Create a single logo variation"""
        # Create canvas
        width, height = 400, 400
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Get color palette
        colors = self.color_palettes.get(request.color_scheme, self.color_palettes['blue'])
        
        # Generate based on style
        if request.style == 'modern':
            logo_img = self._generate_modern_logo(draw, width, height, colors, request.company_name)
        elif request.style == 'vintage':
            logo_img = self._generate_vintage_logo(draw, width, height, colors, request.company_name)
        elif request.style == 'minimalist':
            logo_img = self._generate_minimalist_logo(draw, width, height, colors, request.company_name)
        elif request.style == 'corporate':
            logo_img = self._generate_corporate_logo(draw, width, height, colors, request.company_name)
        elif request.style == 'creative':
            logo_img = self._generate_creative_logo(draw, width, height, colors, request.company_name)
        elif request.style == 'tech':
            logo_img = self._generate_tech_logo(draw, width, height, colors, request.company_name)
        else:
            logo_img = self._generate_elegant_logo(draw, width, height, colors, request.company_name)
        
        # Save image
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        image_file = ContentFile(buffer.getvalue(), name=f'logo_{request.company_name}_{variation_id}.png')
        
        return {
            'image': image_file,
            'prompt': f"AI-generated {request.style} logo for {request.company_name} in {request.color_scheme} theme",
            'method': f'AI_Algorithm_v{variation_id + 1}'
        }
    
    def _generate_modern_logo(self, draw, width, height, colors, company_name):
        """Generate modern style logo"""
        # Draw geometric shapes
        center_x, center_y = width // 2, height // 2
        
        # Main circle
        draw.ellipse([center_x-80, center_y-80, center_x+80, center_y+80], 
                    fill=colors[0], outline=colors[1], width=3)
        
        # Inner geometric pattern
        for i in range(6):
            angle = i * 60
            x = center_x + 40 * np.cos(np.radians(angle))
            y = center_y + 40 * np.sin(np.radians(angle))
            draw.ellipse([x-10, y-10, x+10, y+10], fill=colors[2])
        
        # Company name
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y + 100), company_name, 
                 fill=colors[0], font=font)
    
    def _generate_vintage_logo(self, draw, width, height, colors, company_name):
        """Generate vintage style logo"""
        center_x, center_y = width // 2, height // 2
        
        # Vintage border
        draw.rectangle([50, 50, width-50, height-50], outline=colors[0], width=5)
        draw.rectangle([60, 60, width-60, height-60], outline=colors[1], width=2)
        
        # Decorative elements
        for i in range(4):
            x = 80 + i * 60
            draw.ellipse([x, 80, x+20, 100], fill=colors[2])
            draw.ellipse([x, height-100, x+20, height-80], fill=colors[2])
        
        # Company name with vintage styling
        try:
            font = ImageFont.truetype("times.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y - 15), company_name, 
                 fill=colors[0], font=font)
    
    def _generate_minimalist_logo(self, draw, width, height, colors, company_name):
        """Generate minimalist style logo"""
        center_x, center_y = width // 2, height // 2
        
        # Simple geometric shape
        draw.rectangle([center_x-60, center_y-60, center_x+60, center_y+60], 
                      fill=colors[0])
        
        # Minimal text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y + 80), company_name, 
                 fill=colors[0], font=font)
    
    def _generate_corporate_logo(self, draw, width, height, colors, company_name):
        """Generate corporate style logo"""
        center_x, center_y = width // 2, height // 2
        
        # Professional rectangle with gradient effect
        for i in range(5):
            alpha = 255 - i * 40
            color_with_alpha = colors[0] + f"{alpha:02x}"
            draw.rectangle([center_x-80+i*5, center_y-40+i*2, 
                          center_x+80-i*5, center_y+40-i*2], 
                         fill=colors[i % len(colors)])
        
        # Company name
        try:
            font = ImageFont.truetype("arial.ttf", 26)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y + 60), company_name, 
                 fill=colors[0], font=font)
    
    def _generate_creative_logo(self, draw, width, height, colors, company_name):
        """Generate creative style logo"""
        center_x, center_y = width // 2, height // 2
        
        # Creative abstract shapes
        for i in range(8):
            angle = i * 45
            x = center_x + 60 * np.cos(np.radians(angle))
            y = center_y + 60 * np.sin(np.radians(angle))
            size = random.randint(15, 30)
            color = random.choice(colors)
            
            if i % 2 == 0:
                draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
            else:
                draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
        
        # Company name
        try:
            font = ImageFont.truetype("arial.ttf", 22)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y + 90), company_name, 
                 fill=colors[0], font=font)
    
    def _generate_tech_logo(self, draw, width, height, colors, company_name):
        """Generate tech style logo"""
        center_x, center_y = width // 2, height // 2
        
        # Tech circuit pattern
        for i in range(3):
            for j in range(3):
                x = center_x - 60 + i * 60
                y = center_y - 60 + j * 60
                draw.rectangle([x-8, y-8, x+8, y+8], fill=colors[0])
                
                # Connect with lines
                if i < 2:
                    draw.line([x+8, y, x+52, y], fill=colors[1], width=2)
                if j < 2:
                    draw.line([x, y+8, x, y+52], fill=colors[1], width=2)
        
        # Company name
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y + 100), company_name, 
                 fill=colors[0], font=font)
    
    def _generate_elegant_logo(self, draw, width, height, colors, company_name):
        """Generate elegant style logo"""
        center_x, center_y = width // 2, height // 2
        
        # Elegant curves
        draw.arc([center_x-70, center_y-70, center_x+70, center_y+70], 
                0, 180, fill=colors[0], width=5)
        draw.arc([center_x-50, center_y-50, center_x+50, center_y+50], 
                180, 360, fill=colors[1], width=5)
        
        # Decorative dots
        for angle in [0, 90, 180, 270]:
            x = center_x + 80 * np.cos(np.radians(angle))
            y = center_y + 80 * np.sin(np.radians(angle))
            draw.ellipse([x-5, y-5, x+5, y+5], fill=colors[2])
        
        # Company name
        try:
            font = ImageFont.truetype("times.ttf", 26)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text((center_x - text_width//2, center_y + 100), company_name, 
                 fill=colors[0], font=font)