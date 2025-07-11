"""
Enhanced AI Logo Generation Engine
Supports multiple AI providers: OpenAI DALL-E, Stable Diffusion, and more
Created by Hiren Patel for LogoMaker Pro
"""

import os
import openai
import requests
import base64
import io
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

class EnhancedAIEngine:
    """Enhanced AI Engine supporting multiple providers"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        self.huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        # Initialize OpenAI if key available
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate_logo_dalle(self, prompt, size="1024x1024", quality="standard", n=1):
        """Generate logo using OpenAI DALL-E 3"""
        try:
            if not self.openai_api_key:
                return {"success": False, "error": "OpenAI API key not configured"}
            
            # Enhanced prompt for logo generation
            logo_prompt = f"""
            Create a professional, minimalist logo design for: {prompt}
            
            Requirements:
            - Clean, scalable vector-style design
            - Professional and modern aesthetic
            - Suitable for business use
            - High contrast and clarity
            - Minimal color palette
            - No text unless specifically requested
            - Transparent or white background preferred
            
            Style: Corporate logo design, vector graphics style
            """
            
            response = openai.Image.create(
                model="dall-e-3",
                prompt=logo_prompt,
                size=size,
                quality=quality,
                n=n
            )
            
            # Process the generated images
            generated_images = []
            for i, image_data in enumerate(response.data):
                image_url = image_data.url
                
                # Download the image
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    # Convert to PIL Image
                    image = Image.open(io.BytesIO(img_response.content))
                    
                    # Save to ContentFile
                    img_io = io.BytesIO()
                    image.save(img_io, format='PNG', quality=95)
                    img_file = ContentFile(img_io.getvalue(), name=f'dalle_logo_{i}.png')
                    
                    generated_images.append({
                        "image_file": img_file,
                        "url": image_url,
                        "size": image.size,
                        "format": "PNG",
                        "model": "dall-e-3",
                        "provider": "openai"
                    })
            
            return {
                "success": True,
                "images": generated_images,
                "provider": "openai",
                "model": "dall-e-3"
            }
            
        except Exception as e:
            logger.error(f"DALL-E generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_logo_stability(self, prompt, width=1024, height=1024, cfg_scale=7, steps=30):
        """Generate logo using Stability AI"""
        try:
            if not self.stability_api_key:
                return {"success": False, "error": "Stability API key not configured"}
            
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            # Enhanced prompt for logo generation
            logo_prompt = f"""
            Professional minimalist logo design: {prompt}
            
            High quality vector-style logo, clean lines, modern aesthetic, 
            corporate branding, scalable design, minimal colors, 
            transparent background, business logo, professional design
            """
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}"
            }
            
            payload = {
                "text_prompts": [
                    {
                        "text": logo_prompt,
                        "weight": 1
                    },
                    {
                        "text": "blurry, low quality, pixelated, watermark, text, signature, frame, border",
                        "weight": -1
                    }
                ],
                "cfg_scale": cfg_scale,
                "height": height,
                "width": width,
                "steps": steps,
                "samples": 1,
                "style_preset": "digital-art"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process generated images
                generated_images = []
                for i, image_data in enumerate(data["artifacts"]):
                    # Decode base64 image
                    image_bytes = base64.b64decode(image_data["base64"])
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Save to ContentFile
                    img_io = io.BytesIO()
                    image.save(img_io, format='PNG', quality=95)
                    img_file = ContentFile(img_io.getvalue(), name=f'stability_logo_{i}.png')
                    
                    generated_images.append({
                        "image_file": img_file,
                        "size": image.size,
                        "format": "PNG",
                        "model": "stable-diffusion-xl",
                        "provider": "stability"
                    })
                
                return {
                    "success": True,
                    "images": generated_images,
                    "provider": "stability",
                    "model": "stable-diffusion-xl"
                }
            else:
                return {"success": False, "error": f"Stability API error: {response.text}"}
                
        except Exception as e:
            logger.error(f"Stability AI generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_logo_huggingface(self, prompt, model="stabilityai/stable-diffusion-xl-base-1.0"):
        """Generate logo using Hugging Face models"""
        try:
            if not self.huggingface_api_key:
                return {"success": False, "error": "Hugging Face API key not configured"}
            
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
            
            # Enhanced prompt
            logo_prompt = f"""
            professional minimalist logo design for {prompt}, 
            vector style, clean corporate branding, scalable design, 
            high quality, modern aesthetic, business logo
            """
            
            payload = {"inputs": logo_prompt}
            
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                # Convert response to image
                image = Image.open(io.BytesIO(response.content))
                
                # Save to ContentFile
                img_io = io.BytesIO()
                image.save(img_io, format='PNG', quality=95)
                img_file = ContentFile(img_io.getvalue(), name='huggingface_logo.png')
                
                return {
                    "success": True,
                    "images": [{
                        "image_file": img_file,
                        "size": image.size,
                        "format": "PNG",
                        "model": model,
                        "provider": "huggingface"
                    }],
                    "provider": "huggingface",
                    "model": model
                }
            else:
                return {"success": False, "error": f"Hugging Face API error: {response.text}"}
                
        except Exception as e:
            logger.error(f"Hugging Face generation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_logo_multi_provider(self, prompt, providers=None, **kwargs):
        """Generate logos using multiple providers for variety"""
        if providers is None:
            providers = ["dalle", "stability", "huggingface"]
        
        results = []
        
        for provider in providers:
            try:
                if provider == "dalle" and self.openai_api_key:
                    result = self.generate_logo_dalle(prompt, **kwargs)
                elif provider == "stability" and self.stability_api_key:
                    result = self.generate_logo_stability(prompt, **kwargs)
                elif provider == "huggingface" and self.huggingface_api_key:
                    result = self.generate_logo_huggingface(prompt, **kwargs)
                else:
                    continue
                
                if result["success"]:
                    results.extend(result["images"])
                    
            except Exception as e:
                logger.error(f"Error with provider {provider}: {str(e)}")
                continue
        
        return {
            "success": len(results) > 0,
            "images": results,
            "total_generated": len(results)
        }
    
    def enhance_logo_prompt(self, business_name, business_description, industry, style, color_scheme):
        """Generate enhanced prompts using AI-powered prompt engineering"""
        
        # Industry-specific keywords
        industry_keywords = {
            "technology": "tech, digital, innovation, modern, futuristic, circuit, data",
            "healthcare": "medical, health, care, cross, heart, wellness, clean",
            "finance": "money, bank, growth, trust, security, professional, stable",
            "education": "book, knowledge, learning, growth, academic, wisdom",
            "retail": "shopping, commerce, customer, service, friendly, accessible",
            "food": "fresh, organic, delicious, quality, natural, appetite",
            "real_estate": "house, building, property, home, architecture, solid",
            "consulting": "professional, expertise, guidance, strategy, solutions",
            "creative": "art, design, creativity, inspiration, unique, original",
            "fitness": "strength, energy, health, movement, vitality, active"
        }
        
        # Style-specific modifiers
        style_modifiers = {
            "modern": "clean lines, minimalist, contemporary, sleek, geometric",
            "vintage": "classic, retro, timeless, heritage, traditional, elegant",
            "creative": "artistic, unique, innovative, expressive, dynamic, bold",
            "corporate": "professional, trustworthy, reliable, established, formal",
            "tech": "digital, futuristic, high-tech, innovative, cutting-edge",
            "elegant": "sophisticated, refined, luxury, premium, graceful"
        }
        
        # Color psychology
        color_psychology = {
            "blue": "trust, reliability, professionalism, stability",
            "red": "energy, passion, urgency, boldness",
            "green": "growth, nature, health, prosperity",
            "purple": "luxury, creativity, wisdom, innovation",
            "orange": "enthusiasm, creativity, warmth, energy",
            "black": "elegance, sophistication, power, authority",
            "colorful": "vibrant, diverse, creative, energetic"
        }
        
        # Build enhanced prompt
        industry_key = industry.name.lower().replace(" & ", "_").replace(" ", "_")
        style_key = style.name.lower()
        color_key = color_scheme.name.lower().replace(" ", "_")
        
        industry_words = industry_keywords.get(industry_key, "professional, quality")
        style_words = style_modifiers.get(style_key, "professional, clean")
        color_words = color_psychology.get(color_key, "professional, balanced")
        
        enhanced_prompt = f"""
        Create a professional logo for "{business_name}" - a {business_description}
        
        Industry context: {industry.name} ({industry_words})
        Style: {style.name} ({style_words})
        Color psychology: {color_scheme.name} ({color_words})
        
        Design requirements:
        - Scalable vector-style design
        - Professional and memorable
        - Suitable for business cards, websites, and signage
        - Clean, modern aesthetic
        - High contrast for readability
        - Minimal yet distinctive
        - Reflects brand personality and values
        
        Technical specs:
        - Vector-style illustration
        - Professional logo design
        - Corporate branding
        - Transparent or white background
        - High resolution and clarity
        """
        
        return enhanced_prompt.strip()
    
    def get_available_providers(self):
        """Get list of available AI providers based on API keys"""
        providers = []
        
        if self.openai_api_key:
            providers.append({
                "name": "OpenAI DALL-E 3",
                "key": "dalle",
                "description": "High-quality artistic logo generation",
                "best_for": "Creative and unique designs"
            })
        
        if self.stability_api_key:
            providers.append({
                "name": "Stability AI",
                "key": "stability", 
                "description": "Professional logo generation with Stable Diffusion",
                "best_for": "Professional and corporate logos"
            })
        
        if self.huggingface_api_key:
            providers.append({
                "name": "Hugging Face",
                "key": "huggingface",
                "description": "Open-source AI models for logo generation",
                "best_for": "Diverse styles and experimentation"
            })
        
        return providers