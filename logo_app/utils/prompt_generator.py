"""
Professional Prompt Generator for Logo Creation
Generates optimized prompts for Stable Diffusion
"""

import random
from typing import List, Dict

class PromptGenerator:
    """Advanced prompt generator for logo creation"""
    
    def __init__(self):
        self.style_templates = {
            'modern': {
                'base': 'modern minimalist logo design, clean lines, professional, contemporary',
                'keywords': ['sleek', 'geometric', 'simple', 'elegant', 'sophisticated'],
                'negative': 'vintage, old-fashioned, cluttered, ornate'
            },
            'vintage': {
                'base': 'vintage retro logo design, classic typography, aged texture, nostalgic',
                'keywords': ['classic', 'timeless', 'heritage', 'traditional', 'antique'],
                'negative': 'modern, futuristic, digital, high-tech'
            },
            'creative': {
                'base': 'creative artistic logo design, unique, innovative, colorful, expressive',
                'keywords': ['artistic', 'imaginative', 'bold', 'vibrant', 'dynamic'],
                'negative': 'boring, generic, corporate, conservative'
            },
            'corporate': {
                'base': 'professional corporate logo, trustworthy, reliable, business-focused',
                'keywords': ['professional', 'trustworthy', 'established', 'formal', 'authoritative'],
                'negative': 'casual, playful, artistic, unconventional'
            },
            'tech': {
                'base': 'futuristic technology logo, digital, high-tech, innovation, modern',
                'keywords': ['digital', 'innovative', 'cutting-edge', 'advanced', 'electronic'],
                'negative': 'organic, handmade, vintage, traditional'
            },
            'elegant': {
                'base': 'elegant sophisticated logo, luxury brand, premium quality, refined',
                'keywords': ['luxurious', 'premium', 'sophisticated', 'refined', 'upscale'],
                'negative': 'cheap, casual, rough, amateur'
            }
        }
        
        self.industry_keywords = {
            'technology': ['tech', 'digital', 'software', 'innovation', 'IT', 'computing'],
            'healthcare': ['medical', 'health', 'care', 'wellness', 'hospital', 'clinic'],
            'finance': ['financial', 'banking', 'money', 'investment', 'trust', 'security'],
            'education': ['learning', 'academic', 'school', 'knowledge', 'growth', 'development'],
            'retail': ['shopping', 'commerce', 'store', 'brand', 'customer', 'market'],
            'food': ['restaurant', 'culinary', 'dining', 'fresh', 'delicious', 'cuisine'],
            'real-estate': ['property', 'home', 'building', 'investment', 'location', 'housing'],
            'consulting': ['advisory', 'professional', 'expertise', 'solutions', 'strategy'],
            'creative': ['design', 'art', 'creative', 'studio', 'imagination', 'artistic'],
            'fitness': ['health', 'gym', 'sports', 'active', 'strength', 'wellness']
        }
        
        self.color_descriptors = {
            'blue': ['professional blue', 'trust', 'reliability', 'corporate blue', 'navy'],
            'red': ['bold red', 'energy', 'passion', 'power', 'vibrant red'],
            'green': ['natural green', 'growth', 'eco-friendly', 'fresh', 'sustainable'],
            'purple': ['royal purple', 'luxury', 'creativity', 'innovation', 'premium'],
            'orange': ['energetic orange', 'friendly', 'warm', 'enthusiastic', 'vibrant'],
            'black': ['elegant black', 'sophisticated', 'premium', 'minimalist', 'classic'],
            'gold': ['luxury gold', 'premium', 'elegant', 'prestigious', 'high-end']
        }
    
    def generate_prompts(self, business_name: str, business_description: str, 
                        industry, style, color_scheme, custom_prompt: str = "", 
                        variations_count: int = 4) -> List[Dict]:
        """Generate multiple prompt variations"""
        
        prompts = []
        
        for i in range(variations_count):
            prompt_data = self._create_single_prompt(
                business_name=business_name,
                business_description=business_description,
                industry=industry,
                style=style,
                color_scheme=color_scheme,
                custom_prompt=custom_prompt,
                variation_id=i
            )
            prompts.append(prompt_data)
        
        return prompts
    
    def _create_single_prompt(self, business_name: str, business_description: str,
                             industry, style, color_scheme, custom_prompt: str,
                             variation_id: int) -> Dict:
        """Create a single optimized prompt"""
        
        # Get style configuration
        style_config = self.style_templates.get(style.slug, self.style_templates['modern'])
        
        # Build positive prompt components
        components = []
        
        # Base style description
        components.append(style_config['base'])
        
        # Industry-specific keywords
        if industry.slug in self.industry_keywords:
            industry_words = self.industry_keywords[industry.slug]
            selected_words = random.sample(industry_words, min(2, len(industry_words)))
            components.append(f"{industry.name} industry, {', '.join(selected_words)}")
        
        # Color scheme
        if color_scheme.slug in self.color_descriptors:
            color_words = self.color_descriptors[color_scheme.slug]
            selected_colors = random.sample(color_words, min(2, len(color_words)))
            components.append(f"{color_scheme.name} color scheme, {', '.join(selected_colors)}")
        
        # Style-specific keywords for variation
        if style_config['keywords']:
            keyword = random.choice(style_config['keywords'])
            components.append(keyword)
        
        # Business description context
        if business_description:
            # Extract key concepts from description
            key_concepts = self._extract_key_concepts(business_description)
            if key_concepts:
                components.append(', '.join(key_concepts[:2]))
        
        # Custom prompt integration
        if custom_prompt:
            components.append(custom_prompt)
        
        # Quality and format specifications
        quality_terms = [
            'professional logo design',
            'high quality',
            'vector style',
            'clean design',
            'scalable',
            'commercial logo',
            'brand identity'
        ]
        
        # Add variation-specific quality terms
        variation_terms = [
            ['masterpiece', 'best quality', 'ultra detailed'],
            ['professional grade', 'commercial quality', 'brand ready'],
            ['premium design', 'high-end logo', 'luxury branding'],
            ['modern branding', 'contemporary design', 'cutting-edge']
        ]
        
        if variation_id < len(variation_terms):
            quality_terms.extend(variation_terms[variation_id])
        else:
            quality_terms.extend(random.choice(variation_terms))
        
        components.extend(quality_terms)
        
        # Build final positive prompt
        positive_prompt = ', '.join(components)
        
        # Build negative prompt
        negative_components = [
            'low quality, blurry, pixelated, jpeg artifacts',
            'amateur, unprofessional, messy, cluttered',
            'watermark, signature, copyright',
            'realistic photo, photograph, 3d render',
            'text, letters, words, typography errors',
            'multiple logos, duplicated elements'
        ]
        
        # Add style-specific negative terms
        if style_config.get('negative'):
            negative_components.append(style_config['negative'])
        
        negative_prompt = ', '.join(negative_components)
        
        return {
            'positive': positive_prompt,
            'negative': negative_prompt,
            'variation_id': variation_id + 1,
            'style': style.name,
            'industry': industry.name,
            'color_scheme': color_scheme.name
        }
    
    def _extract_key_concepts(self, description: str) -> List[str]:
        """Extract key concepts from business description"""
        
        # Simple keyword extraction
        important_words = [
            'innovative', 'creative', 'professional', 'reliable', 'trusted',
            'premium', 'quality', 'service', 'solution', 'expert',
            'modern', 'traditional', 'family', 'local', 'global',
            'sustainable', 'eco-friendly', 'organic', 'natural',
            'luxury', 'affordable', 'fast', 'convenient'
        ]
        
        description_lower = description.lower()
        found_concepts = []
        
        for word in important_words:
            if word in description_lower:
                found_concepts.append(word)
        
        return found_concepts[:3]  # Return top 3 concepts
    
    def optimize_prompt_for_model(self, prompt: str, model_name: str = "") -> str:
        """Optimize prompt for specific model"""
        
        # Model-specific optimizations
        if 'realistic' in model_name.lower():
            # Add realism enhancers
            prompt += ', photorealistic style, detailed rendering'
        elif 'artistic' in model_name.lower():
            # Add artistic enhancers
            prompt += ', artistic interpretation, creative style'
        elif 'logo' in model_name.lower():
            # Add logo-specific enhancers
            prompt += ', logo optimized, brand focused, commercial ready'
        
        return prompt
    
    def get_style_suggestions(self, industry_name: str) -> List[str]:
        """Get recommended styles for an industry"""
        
        industry_style_map = {
            'technology': ['modern', 'tech', 'creative'],
            'healthcare': ['corporate', 'modern', 'elegant'],
            'finance': ['corporate', 'elegant', 'modern'],
            'education': ['modern', 'creative', 'corporate'],
            'retail': ['creative', 'modern', 'elegant'],
            'food': ['creative', 'vintage', 'elegant'],
            'real-estate': ['corporate', 'elegant', 'modern'],
            'consulting': ['corporate', 'modern', 'elegant'],
            'creative': ['creative', 'modern', 'artistic'],
            'fitness': ['modern', 'creative', 'tech']
        }
        
        return industry_style_map.get(industry_name.lower(), ['modern', 'corporate', 'creative'])
    
    def get_color_suggestions(self, industry_name: str) -> List[str]:
        """Get recommended colors for an industry"""
        
        industry_color_map = {
            'technology': ['blue', 'purple', 'black'],
            'healthcare': ['blue', 'green', 'red'],
            'finance': ['blue', 'black', 'gold'],
            'education': ['blue', 'green', 'orange'],
            'retail': ['red', 'orange', 'purple'],
            'food': ['red', 'orange', 'green'],
            'real-estate': ['blue', 'green', 'gold'],
            'consulting': ['blue', 'black', 'purple'],
            'creative': ['purple', 'orange', 'red'],
            'fitness': ['red', 'orange', 'green']
        }
        
        return industry_color_map.get(industry_name.lower(), ['blue', 'black', 'red'])