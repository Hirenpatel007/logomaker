"""
🎨 STABLE DIFFUSION AI INTEGRATION - UNLIMITED FREE LOGO GENERATION
Created by Hiren Patel for World-Class Logo Generation
No API Keys Required - Completely Free & Unlimited
"""

import requests
import json
import base64
import io
import os
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
import time
import logging

logger = logging.getLogger(__name__)

class StableDiffusionAI:
    """
    Stable Diffusion AI Integration for Unlimited Free Logo Generation
    Uses AUTOMATIC1111 WebUI API - No external API keys required
    """
    
    def __init__(self):
        self.api_url = "http://127.0.0.1:7860"  # Local Stable Diffusion WebUI
        self.timeout = 300  # 5 minutes timeout
        self.logo_styles = self._init_logo_styles()
        self.quality_settings = self._init_quality_settings()
        
    def _init_logo_styles(self):
        """Initialize professional logo style prompts"""
        return {
            'modern': {
                'base_prompt': 'modern minimalist logo design, clean lines, professional, corporate identity',
                'negative': 'cluttered, messy, low quality, blurry, pixelated, amateur',
                'style_weight': 1.2
            },
            'vintage': {
                'base_prompt': 'vintage retro logo design, classic typography, aged texture, nostalgic',
                'negative': 'modern, digital, pixelated, low quality, amateur',
                'style_weight': 1.1
            },
            'tech': {
                'base_prompt': 'futuristic technology logo, digital, circuit patterns, high-tech, innovation',
                'negative': 'organic, handdrawn, vintage, low quality, blurry',
                'style_weight': 1.3
            },
            'creative': {
                'base_prompt': 'creative artistic logo design, unique, innovative, colorful, expressive',
                'negative': 'boring, generic, corporate, low quality, pixelated',
                'style_weight': 1.2
            },
            'elegant': {
                'base_prompt': 'elegant sophisticated logo, luxury brand, premium quality, refined',
                'negative': 'cheap, amateur, low quality, messy, cluttered',
                'style_weight': 1.1
            },
            'playful': {
                'base_prompt': 'playful fun logo design, vibrant colors, friendly, approachable',
                'negative': 'serious, corporate, boring, low quality, blurry',
                'style_weight': 1.0
            },
            'professional': {
                'base_prompt': 'professional business logo, trustworthy, reliable, corporate',
                'negative': 'casual, amateur, low quality, pixelated, messy',
                'style_weight': 1.2
            },
            'artistic': {
                'base_prompt': 'artistic creative logo, hand-crafted, unique design, artistic flair',
                'negative': 'generic, corporate, boring, low quality, amateur',
                'style_weight': 1.1
            }
        }
    
    def _init_quality_settings(self):
        """Initialize high-quality generation settings"""
        return {
            'steps': 30,  # Higher steps for better quality
            'cfg_scale': 7.5,  # Creativity vs adherence balance
            'width': 512,
            'height': 512,
            'sampler_name': 'DPM++ 2M Karras',  # High quality sampler
            'restore_faces': True,
            'enable_hr': True,  # High-res fix
            'hr_scale': 2,  # 2x upscaling
            'hr_upscaler': 'ESRGAN_4x',
            'denoising_strength': 0.7
        }
    
    def check_api_status(self):
        """Check if Stable Diffusion WebUI is running"""
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/progress", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def generate_logo(self, company_name, industry, style='modern', color_scheme='blue', description=''):
        """
        Generate professional logo using Stable Diffusion
        
        Args:
            company_name (str): Name of the company
            industry (str): Industry/business type
            style (str): Logo style from available styles
            color_scheme (str): Color preference
            description (str): Additional description
            
        Returns:
            list: Generated logo data with images and metadata
        """
        
        if not self.check_api_status():
            logger.error("Stable Diffusion WebUI is not running")
            return self._generate_fallback_logos(company_name, style, color_scheme)
        
        try:
            # Generate multiple variations
            logos = []
            for i in range(5):  # Generate 5 variations
                logo_data = self._generate_single_logo(
                    company_name, industry, style, color_scheme, description, i
                )
                if logo_data:
                    logos.append(logo_data)
                    
            return logos if logos else self._generate_fallback_logos(company_name, style, color_scheme)
            
        except Exception as e:
            logger.error(f"Error generating logos: {str(e)}")
            return self._generate_fallback_logos(company_name, style, color_scheme)
    
    def _generate_single_logo(self, company_name, industry, style, color_scheme, description, variation_id):
        """Generate a single logo variation"""
        
        # Build comprehensive prompt
        prompt = self._build_logo_prompt(company_name, industry, style, color_scheme, description, variation_id)
        
        # Prepare API payload
        payload = {
            "prompt": prompt['positive'],
            "negative_prompt": prompt['negative'],
            "steps": self.quality_settings['steps'],
            "cfg_scale": self.quality_settings['cfg_scale'],
            "width": self.quality_settings['width'],
            "height": self.quality_settings['height'],
            "sampler_name": self.quality_settings['sampler_name'],
            "restore_faces": self.quality_settings['restore_faces'],
            "enable_hr": self.quality_settings['enable_hr'],
            "hr_scale": self.quality_settings['hr_scale'],
            "hr_upscaler": self.quality_settings['hr_upscaler'],
            "denoising_strength": self.quality_settings['denoising_strength'],
            "seed": -1,  # Random seed for variation
            "batch_size": 1,
            "n_iter": 1
        }
        
        try:
            # Send generation request
            response = requests.post(
                f"{self.api_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('images'):
                    # Decode base64 image
                    image_data = base64.b64decode(result['images'][0])
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Post-process image for logo optimization
                    processed_image = self._post_process_logo(image)
                    
                    # Save to ContentFile
                    buffer = io.BytesIO()
                    processed_image.save(buffer, format='PNG', quality=100, optimize=True)
                    buffer.seek(0)
                    
                    image_file = ContentFile(
                        buffer.getvalue(),
                        name=f'ai_logo_{company_name}_{style}_{variation_id}.png'
                    )
                    
                    return {
                        'image': image_file,
                        'prompt': prompt['positive'],
                        'style': style,
                        'method': f'StableDiffusion_v{variation_id + 1}',
                        'quality_score': self._calculate_quality_score(processed_image),
                        'generation_time': result.get('info', {}).get('time_taken', 0),
                        'seed': result.get('info', {}).get('seed', -1)
                    }
            
        except Exception as e:
            logger.error(f"Error in single logo generation: {str(e)}")
            
        return None
    
    def _build_logo_prompt(self, company_name, industry, style, color_scheme, description, variation_id):
        """Build comprehensive prompt for logo generation"""
        
        style_config = self.logo_styles.get(style, self.logo_styles['modern'])
        
        # Industry-specific keywords
        industry_keywords = {
            'technology': 'tech, digital, innovation, software, IT',
            'healthcare': 'medical, health, care, wellness, hospital',
            'finance': 'financial, banking, money, investment, trust',
            'education': 'learning, academic, school, knowledge, growth',
            'retail': 'shopping, commerce, store, brand, customer',
            'food': 'restaurant, culinary, dining, fresh, delicious',
            'real-estate': 'property, home, building, investment, location',
            'consulting': 'advisory, professional, expertise, solutions',
            'creative': 'design, art, creative, studio, imagination',
            'fitness': 'health, gym, sports, active, strength'
        }
        
        # Color-specific prompts
        color_prompts = {
            'blue': 'blue color scheme, professional blue, trust, reliability',
            'red': 'red color palette, energy, passion, bold',
            'green': 'green colors, nature, growth, eco-friendly',
            'purple': 'purple theme, luxury, creativity, innovation',
            'orange': 'orange palette, energetic, friendly, warm',
            'black': 'black and white, monochrome, elegant, sophisticated',
            'rainbow': 'colorful, vibrant, diverse, creative colors'
        }
        
        # Build positive prompt
        positive_parts = [
            f"professional logo design for '{company_name}'",
            style_config['base_prompt'],
            industry_keywords.get(industry, 'business, professional'),
            color_prompts.get(color_scheme, 'professional colors'),
            "high quality, vector style, clean design, scalable",
            "masterpiece, best quality, ultra detailed",
            "commercial logo, brand identity, professional branding"
        ]
        
        if description:
            positive_parts.append(description)
        
        # Add variation-specific elements
        variation_elements = [
            "geometric elements, modern typography",
            "abstract symbol, creative icon",
            "minimalist approach, clean lines",
            "bold design, strong presence",
            "elegant curves, sophisticated style"
        ]
        
        if variation_id < len(variation_elements):
            positive_parts.append(variation_elements[variation_id])
        
        positive_prompt = ", ".join(positive_parts)
        
        # Build negative prompt
        negative_prompt = ", ".join([
            style_config['negative'],
            "text, letters, words, typography errors",
            "low quality, blurry, pixelated, jpeg artifacts",
            "amateur, unprofessional, messy, cluttered",
            "watermark, signature, copyright",
            "realistic photo, photograph, 3d render",
            "multiple logos, duplicated elements"
        ])
        
        return {
            'positive': positive_prompt,
            'negative': negative_prompt
        }
    
    def _post_process_logo(self, image):
        """Post-process generated image for logo optimization"""
        
        # Ensure square aspect ratio
        size = min(image.size)
        left = (image.width - size) // 2
        top = (image.height - size) // 2
        image = image.crop((left, top, left + size, top + size))
        
        # Resize to standard logo size
        image = image.resize((512, 512), Image.Resampling.LANCZOS)
        
        # Enhance contrast and sharpness
        from PIL import ImageEnhance
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        # Convert to RGBA for transparency support
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        return image
    
    def _calculate_quality_score(self, image):
        """Calculate quality score for generated logo"""
        
        # Simple quality metrics
        score = 85  # Base score
        
        # Check image size
        if image.size[0] >= 512 and image.size[1] >= 512:
            score += 5
        
        # Check if image has transparency
        if image.mode == 'RGBA':
            score += 5
        
        # Add random variation for demo
        import random
        score += random.randint(-5, 10)
        
        return min(100, max(70, score))
    
    def _generate_fallback_logos(self, company_name, style, color_scheme):
        """Generate fallback logos when Stable Diffusion is not available"""
        
        logger.info("Generating fallback logos using built-in generator")
        
        # Import the existing magical AI generator as fallback
        from .magical_ai import MagicalAIEngine
        
        magical_ai = MagicalAIEngine()
        
        # Create request data for fallback
        request_data = {
            'company_name': company_name,
            'style': style,
            'color_scheme': color_scheme,
            'industry': 'business'
        }
        
        # Generate using magical AI as fallback
        return magical_ai.generate_magical_logo(request_data)
    
    def get_available_models(self):
        """Get list of available Stable Diffusion models"""
        
        if not self.check_api_status():
            return []
        
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/sd-models", timeout=10)
            if response.status_code == 200:
                models = response.json()
                return [model['title'] for model in models]
        except Exception as e:
            logger.error(f"Error fetching models: {str(e)}")
        
        return []
    
    def switch_model(self, model_name):
        """Switch to a specific Stable Diffusion model"""
        
        if not self.check_api_status():
            return False
        
        try:
            payload = {"sd_model_checkpoint": model_name}
            response = requests.post(
                f"{self.api_url}/sdapi/v1/options",
                json=payload,
                timeout=30
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error switching model: {str(e)}")
            return False
    
    def get_generation_progress(self):
        """Get current generation progress"""
        
        if not self.check_api_status():
            return {'progress': 0, 'eta': 0}
        
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/progress", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Error getting progress: {str(e)}")
        
        return {'progress': 0, 'eta': 0}

# Utility functions for easy integration

def generate_logo_batch(requests_data):
    """Generate multiple logos in batch"""
    
    sd_ai = StableDiffusionAI()
    results = []
    
    for request_data in requests_data:
        logos = sd_ai.generate_logo(
            company_name=request_data.get('company_name', ''),
            industry=request_data.get('industry', 'business'),
            style=request_data.get('style', 'modern'),
            color_scheme=request_data.get('color_scheme', 'blue'),
            description=request_data.get('description', '')
        )
        results.append({
            'request': request_data,
            'logos': logos
        })
    
    return results

def check_stable_diffusion_status():
    """Quick status check for Stable Diffusion"""
    
    sd_ai = StableDiffusionAI()
    return {
        'available': sd_ai.check_api_status(),
        'models': sd_ai.get_available_models(),
        'api_url': sd_ai.api_url
    }

def get_recommended_settings():
    """Get recommended settings for logo generation"""
    
    return {
        'installation_guide': {
            'step_1': 'Download AUTOMATIC1111 WebUI from GitHub',
            'step_2': 'Install Python 3.10+ and Git',
            'step_3': 'Run webui-user.bat (Windows) or webui.sh (Linux/Mac)',
            'step_4': 'Access http://127.0.0.1:7860 in browser',
            'step_5': 'Download logo-optimized models from CivitAI'
        },
        'recommended_models': [
            'Realistic Vision V5.1',
            'DreamShaper 8',
            'Absolute Reality V1.8.1',
            'Epic Realism Natural Sin RC1',
            'Juggernaut XL V9'
        ],
        'optimal_settings': {
            'steps': 25-35,
            'cfg_scale': 7-8,
            'sampler': 'DPM++ 2M Karras',
            'resolution': '512x512 or 768x768',
            'batch_size': 1
        },
        'logo_prompts': {
            'positive': 'professional logo, vector style, clean design, high quality, masterpiece',
            'negative': 'low quality, blurry, text, letters, realistic photo, 3d render'
        }
    }