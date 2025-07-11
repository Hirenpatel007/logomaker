"""
Smart Color Palette Generator
AI-powered color suggestions based on industry, psychology, and branding
Created by Hiren Patel for LogoMaker Pro
"""

import colorsys
import random
from typing import List, Dict, Tuple
import webcolors

class SmartColorPalette:
    """Generate intelligent color palettes for logos"""
    
    def __init__(self):
        # Industry-specific color associations
        self.industry_colors = {
            "technology": {
                "primary": ["#3B82F6", "#6366F1", "#8B5CF6", "#06B6D4"],
                "secondary": ["#1E40AF", "#4338CA", "#7C3AED", "#0891B2"],
                "accent": ["#F59E0B", "#EF4444", "#10B981", "#8B5CF6"]
            },
            "healthcare": {
                "primary": ["#10B981", "#06B6D4", "#3B82F6", "#FFFFFF"],
                "secondary": ["#059669", "#0891B2", "#2563EB", "#F3F4F6"],
                "accent": ["#EF4444", "#F59E0B", "#8B5CF6", "#6B7280"]
            },
            "finance": {
                "primary": ["#1E40AF", "#059669", "#374151", "#1F2937"],
                "secondary": ["#3730A3", "#047857", "#4B5563", "#111827"],
                "accent": ["#F59E0B", "#DC2626", "#7C3AED", "#FBBF24"]
            },
            "food": {
                "primary": ["#EF4444", "#F59E0B", "#10B981", "#8B5CF6"],
                "secondary": ["#DC2626", "#D97706", "#059669", "#7C3AED"],
                "accent": ["#FEF3C7", "#FEE2E2", "#D1FAE5", "#EDE9FE"]
            },
            "creative": {
                "primary": ["#8B5CF6", "#EC4899", "#F59E0B", "#EF4444"],
                "secondary": ["#7C3AED", "#DB2777", "#D97706", "#DC2626"],
                "accent": ["#06B6D4", "#10B981", "#6366F1", "#F97316"]
            },
            "corporate": {
                "primary": ["#1F2937", "#374151", "#3B82F6", "#1E40AF"],
                "secondary": ["#111827", "#4B5563", "#2563EB", "#1E3A8A"],
                "accent": ["#F59E0B", "#10B981", "#8B5CF6", "#EF4444"]
            }
        }
        
        # Color psychology mapping
        self.color_psychology = {
            "trust": ["#3B82F6", "#1E40AF", "#06B6D4", "#0891B2"],
            "energy": ["#EF4444", "#DC2626", "#F59E0B", "#D97706"],
            "growth": ["#10B981", "#059669", "#84CC16", "#65A30D"],
            "luxury": ["#8B5CF6", "#7C3AED", "#1F2937", "#374151"],
            "friendly": ["#F59E0B", "#FBBF24", "#FDE047", "#EAB308"],
            "professional": ["#374151", "#4B5563", "#6B7280", "#9CA3AF"],
            "innovative": ["#6366F1", "#4F46E5", "#8B5CF6", "#A855F7"],
            "natural": ["#84CC16", "#16A34A", "#15803D", "#166534"]
        }
        
        # Trending color palettes
        self.trending_palettes = [
            {
                "name": "Ocean Breeze",
                "colors": ["#0EA5E9", "#0284C7", "#0369A1", "#075985"],
                "mood": "Professional, Trustworthy, Clean"
            },
            {
                "name": "Sunset Glow",
                "colors": ["#F97316", "#EA580C", "#DC2626", "#B91C1C"],
                "mood": "Energetic, Warm, Creative"
            },
            {
                "name": "Forest Fresh",
                "colors": ["#16A34A", "#15803D", "#166534", "#14532D"],
                "mood": "Natural, Growth, Sustainable"
            },
            {
                "name": "Royal Purple",
                "colors": ["#9333EA", "#7C3AED", "#6D28D9", "#5B21B6"],
                "mood": "Luxury, Creative, Premium"
            },
            {
                "name": "Modern Minimal",
                "colors": ["#1F2937", "#374151", "#4B5563", "#6B7280"],
                "mood": "Professional, Modern, Sophisticated"
            }
        ]
    
    def suggest_colors_for_business(self, business_description: str, industry: str, 
                                  brand_personality: List[str] = None) -> Dict:
        """Suggest colors based on business context"""
        
        if brand_personality is None:
            brand_personality = []
        
        suggestions = {
            "primary_colors": [],
            "secondary_colors": [],
            "accent_colors": [],
            "reasoning": []
        }
        
        # Get industry-based colors
        industry_key = industry.lower().replace(" & ", "").replace(" ", "")
        if industry_key in self.industry_colors:
            industry_palette = self.industry_colors[industry_key]
            suggestions["primary_colors"].extend(industry_palette["primary"])
            suggestions["secondary_colors"].extend(industry_palette["secondary"])
            suggestions["accent_colors"].extend(industry_palette["accent"])
            suggestions["reasoning"].append(f"Colors chosen for {industry} industry standards")
        
        # Add psychology-based colors
        for personality in brand_personality:
            if personality.lower() in self.color_psychology:
                psych_colors = self.color_psychology[personality.lower()]
                suggestions["accent_colors"].extend(psych_colors[:2])
                suggestions["reasoning"].append(f"Added {personality} colors for brand personality")
        
        # Analyze business description for keywords
        description_lower = business_description.lower()
        
        # Keyword-based color suggestions
        if any(word in description_lower for word in ["tech", "digital", "software", "app"]):
            suggestions["primary_colors"].extend(["#3B82F6", "#6366F1"])
            suggestions["reasoning"].append("Tech-focused blue tones for innovation")
        
        if any(word in description_lower for word in ["eco", "green", "sustainable", "natural"]):
            suggestions["primary_colors"].extend(["#10B981", "#84CC16"])
            suggestions["reasoning"].append("Green tones for eco-friendly messaging")
        
        if any(word in description_lower for word in ["luxury", "premium", "high-end", "exclusive"]):
            suggestions["primary_colors"].extend(["#8B5CF6", "#1F2937"])
            suggestions["reasoning"].append("Premium colors for luxury positioning")
        
        if any(word in description_lower for word in ["fun", "creative", "playful", "kids"]):
            suggestions["accent_colors"].extend(["#F59E0B", "#EF4444", "#8B5CF6"])
            suggestions["reasoning"].append("Vibrant colors for playful brand image")
        
        # Remove duplicates and limit selections
        suggestions["primary_colors"] = list(set(suggestions["primary_colors"]))[:6]
        suggestions["secondary_colors"] = list(set(suggestions["secondary_colors"]))[:6]
        suggestions["accent_colors"] = list(set(suggestions["accent_colors"]))[:8]
        
        return suggestions
    
    def generate_complementary_palette(self, base_color: str, size: int = 5) -> List[str]:
        """Generate complementary colors based on a base color"""
        try:
            # Convert hex to RGB
            rgb = webcolors.hex_to_rgb(base_color)
            h, s, v = colorsys.rgb_to_hsv(rgb.red/255, rgb.green/255, rgb.blue/255)
            
            colors = [base_color]
            
            # Generate complementary colors
            for i in range(1, size):
                # Vary hue, saturation, and value
                new_h = (h + (i * 0.2)) % 1.0
                new_s = max(0.3, min(1.0, s + (i * 0.1) - 0.2))
                new_v = max(0.3, min(1.0, v + (i * 0.1) - 0.2))
                
                # Convert back to RGB and hex
                rgb = colorsys.hsv_to_rgb(new_h, new_s, new_v)
                hex_color = "#{:02x}{:02x}{:02x}".format(
                    int(rgb[0] * 255),
                    int(rgb[1] * 255),
                    int(rgb[2] * 255)
                )
                colors.append(hex_color.upper())
            
            return colors
            
        except Exception:
            # Fallback to predefined palette
            return ["#3B82F6", "#6366F1", "#8B5CF6", "#EC4899", "#F59E0B"]
    
    def generate_monochromatic_palette(self, base_color: str, variations: int = 5) -> List[str]:
        """Generate monochromatic variations of a color"""
        try:
            rgb = webcolors.hex_to_rgb(base_color)
            h, s, v = colorsys.rgb_to_hsv(rgb.red/255, rgb.green/255, rgb.blue/255)
            
            colors = []
            
            # Generate variations by changing value and saturation
            for i in range(variations):
                factor = 0.3 + (i * 0.7 / (variations - 1))
                new_s = s * factor
                new_v = 0.3 + (factor * 0.7)
                
                rgb = colorsys.hsv_to_rgb(h, new_s, new_v)
                hex_color = "#{:02x}{:02x}{:02x}".format(
                    int(rgb[0] * 255),
                    int(rgb[1] * 255),
                    int(rgb[2] * 255)
                )
                colors.append(hex_color.upper())
            
            return colors
            
        except Exception:
            return ["#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD", "#DBEAFE"]
    
    def get_trending_palettes(self) -> List[Dict]:
        """Get current trending color palettes"""
        return self.trending_palettes
    
    def analyze_color_harmony(self, colors: List[str]) -> Dict:
        """Analyze color harmony and provide feedback"""
        if len(colors) < 2:
            return {"harmony_score": 0, "feedback": "Need at least 2 colors"}
        
        harmony_score = 0
        feedback = []
        
        try:
            # Convert colors to HSV for analysis
            hsv_colors = []
            for color in colors:
                rgb = webcolors.hex_to_rgb(color)
                hsv = colorsys.rgb_to_hsv(rgb.red/255, rgb.green/255, rgb.blue/255)
                hsv_colors.append(hsv)
            
            # Check hue relationships
            hues = [hsv[0] for hsv in hsv_colors]
            hue_differences = []
            
            for i in range(len(hues)):
                for j in range(i+1, len(hues)):
                    diff = abs(hues[i] - hues[j])
                    diff = min(diff, 1.0 - diff)  # Account for circular nature
                    hue_differences.append(diff)
            
            avg_hue_diff = sum(hue_differences) / len(hue_differences) if hue_differences else 0
            
            # Score based on hue relationships
            if 0.15 <= avg_hue_diff <= 0.35:  # Complementary/triadic
                harmony_score += 30
                feedback.append("Good complementary color relationships")
            elif avg_hue_diff < 0.15:  # Analogous
                harmony_score += 25
                feedback.append("Nice analogous color scheme")
            
            # Check saturation balance
            saturations = [hsv[1] for hsv in hsv_colors]
            sat_variance = sum((s - sum(saturations)/len(saturations))**2 for s in saturations) / len(saturations)
            
            if sat_variance < 0.1:
                harmony_score += 20
                feedback.append("Well-balanced saturation levels")
            
            # Check value (brightness) contrast
            values = [hsv[2] for hsv in hsv_colors]
            value_range = max(values) - min(values)
            
            if value_range > 0.3:
                harmony_score += 25
                feedback.append("Good contrast for readability")
            
            # Professional color check
            professional_hues = [h for h in hues if 0.5 <= h <= 0.7 or h <= 0.1 or h >= 0.9]
            if len(professional_hues) / len(hues) >= 0.5:
                harmony_score += 25
                feedback.append("Professional color selection")
            
            harmony_score = min(100, harmony_score)
            
        except Exception as e:
            harmony_score = 50
            feedback = ["Color analysis completed"]
        
        return {
            "harmony_score": harmony_score,
            "feedback": feedback,
            "grade": "Excellent" if harmony_score >= 80 else 
                    "Good" if harmony_score >= 60 else 
                    "Fair" if harmony_score >= 40 else "Needs Improvement"
        }
    
    def suggest_palette_improvements(self, colors: List[str]) -> Dict:
        """Suggest improvements to an existing palette"""
        analysis = self.analyze_color_harmony(colors)
        suggestions = {
            "current_score": analysis["harmony_score"],
            "improvements": [],
            "alternative_colors": []
        }
        
        if analysis["harmony_score"] < 80:
            if len(colors) > 0:
                # Suggest better complementary colors
                base_color = colors[0]
                complementary = self.generate_complementary_palette(base_color, 3)
                suggestions["alternative_colors"] = complementary[1:]
                suggestions["improvements"].append("Try these complementary colors for better harmony")
            
            if analysis["harmony_score"] < 60:
                suggestions["improvements"].append("Consider using fewer colors for a cleaner look")
                suggestions["improvements"].append("Ensure sufficient contrast between colors")
            
            if analysis["harmony_score"] < 40:
                suggestions["improvements"].append("Current palette may be too busy or conflicting")
                suggestions["improvements"].append("Start with 2-3 main colors and build from there")
        
        return suggestions