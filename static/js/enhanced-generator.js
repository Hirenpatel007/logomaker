/**
 * Enhanced Logo Generation Interface
 * Handles template selection, color suggestions, and AI generation
 * Created by Hiren Patel for LogoMaker Pro
 */

class EnhancedLogoGenerator {
    constructor() {
        this.selectedOption = 'ai';
        this.selectedTemplate = null;
        this.selectedStyle = null;
        this.selectedColors = {
            primary: '#3B82F6',
            secondary: null,
            accent: null
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeSmartColorSuggestions();
    }

    setupEventListeners() {
        // Generation option selection
        document.querySelectorAll('.option-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const option = e.currentTarget.onclick ? 
                    e.currentTarget.onclick.toString().match(/selectOption\('(\w+)'\)/)[1] : 
                    e.currentTarget.dataset.option;
                this.selectGenerationOption(option);
            });
        });

        // Template selection
        document.querySelectorAll('.template-card').forEach(card => {
            card.addEventListener('click', () => {
                this.selectTemplate(card.dataset.template);
            });
        });

        // Template category filtering
        document.querySelectorAll('.template-category-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.filterTemplates(btn.dataset.category);
            });
        });

        // Style selection
        document.querySelectorAll('.style-option').forEach(option => {
            option.addEventListener('click', () => {
                this.selectStyle(option.dataset.style);
            });
        });

        // Color picker selection
        document.querySelectorAll('.color-picker').forEach(picker => {
            picker.addEventListener('click', () => {
                this.selectColor(picker.dataset.color, picker.style.background);
            });
        });

        // Business info changes trigger color suggestions
        const businessName = document.getElementById('businessName');
        const industry = document.getElementById('industry');
        const businessDescription = document.getElementById('businessDescription');

        [businessName, industry, businessDescription].forEach(input => {
            if (input) {
                input.addEventListener('input', () => {
                    this.updateColorSuggestions();
                });
                input.addEventListener('change', () => {
                    this.updateColorSuggestions();
                });
            }
        });

        // Form submission
        document.getElementById('logoForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateLogos();
        });
    }

    selectGenerationOption(option) {
        this.selectedOption = option;
        
        // Update UI
        document.querySelectorAll('.option-card').forEach(card => {
            card.classList.remove('border-blue-500', 'border-purple-500');
            card.classList.add('border-transparent');
        });

        const selectedCard = document.querySelector(`[onclick*="${option}"]`);
        if (selectedCard) {
            selectedCard.classList.remove('border-transparent');
            selectedCard.classList.add(option === 'ai' ? 'border-blue-500' : 'border-purple-500');
        }

        // Show/hide template section
        const templateSection = document.getElementById('templateSection');
        if (option === 'template') {
            templateSection.classList.remove('hidden');
        } else {
            templateSection.classList.add('hidden');
        }

        // Update progress steps
        this.updateProgressSteps();
    }

    selectTemplate(templateId) {
        this.selectedTemplate = templateId;
        
        // Update UI
        document.querySelectorAll('.template-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        const selectedCard = document.querySelector(`[data-template="${templateId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
    }

    filterTemplates(category) {
        // Update category buttons
        document.querySelectorAll('.template-category-btn').forEach(btn => {
            btn.classList.remove('active', 'bg-blue-100', 'text-blue-800', 'border-blue-200');
            btn.classList.add('bg-gray-100', 'text-gray-700', 'border-transparent');
        });

        const activeBtn = document.querySelector(`[data-category="${category}"]`);
        if (activeBtn) {
            activeBtn.classList.remove('bg-gray-100', 'text-gray-700', 'border-transparent');
            activeBtn.classList.add('active', 'bg-blue-100', 'text-blue-800', 'border-blue-200');
        }

        // Filter templates (in a real implementation, this would filter the actual template cards)
        console.log(`Filtering templates by category: ${category}`);
    }

    selectStyle(style) {
        this.selectedStyle = style;
        
        // Update UI
        document.querySelectorAll('.style-option').forEach(option => {
            option.classList.remove('border-blue-500', 'bg-blue-50');
        });
        
        const selectedOption = document.querySelector(`[data-style="${style}"]`);
        if (selectedOption) {
            selectedOption.classList.add('border-blue-500', 'bg-blue-50');
        }

        // Update color suggestions based on style
        this.updateColorSuggestions();
    }

    selectColor(color, background) {
        this.selectedColors.primary = color;
        
        // Update UI
        document.querySelectorAll('.color-picker').forEach(picker => {
            picker.classList.remove('selected');
        });
        
        const selectedPicker = document.querySelector(`[data-color="${color}"]`);
        if (selectedPicker) {
            selectedPicker.classList.add('selected');
        }
    }

    initializeSmartColorSuggestions() {
        // Color palette data for different industries
        this.colorPalettes = {
            technology: {
                primary: ['#3B82F6', '#6366F1', '#8B5CF6'],
                secondary: ['#1E40AF', '#4338CA', '#7C3AED'],
                accent: ['#F59E0B', '#10B981', '#EF4444'],
                reasoning: 'Blues and purples convey innovation and trust in technology'
            },
            healthcare: {
                primary: ['#10B981', '#06B6D4', '#FFFFFF'],
                secondary: ['#059669', '#0891B2', '#F3F4F6'],
                accent: ['#3B82F6', '#F59E0B', '#EF4444'],
                reasoning: 'Green and blue represent health, cleanliness, and care'
            },
            finance: {
                primary: ['#1E40AF', '#059669', '#374151'],
                secondary: ['#1E3A8A', '#047857', '#1F2937'],
                accent: ['#F59E0B', '#3B82F6', '#10B981'],
                reasoning: 'Deep blues and greens suggest stability and growth'
            },
            creative: {
                primary: ['#8B5CF6', '#EC4899', '#F59E0B'],
                secondary: ['#7C3AED', '#DB2777', '#D97706'],
                accent: ['#3B82F6', '#10B981', '#EF4444'],
                reasoning: 'Vibrant colors inspire creativity and artistic expression'
            },
            food: {
                primary: ['#EF4444', '#F59E0B', '#10B981'],
                secondary: ['#DC2626', '#D97706', '#059669'],
                accent: ['#FEF3C7', '#FEE2E2', '#D1FAE5'],
                reasoning: 'Warm colors stimulate appetite and suggest freshness'
            }
        };
    }

    updateColorSuggestions() {
        const industry = document.getElementById('industry').value;
        const businessName = document.getElementById('businessName').value;
        const description = document.getElementById('businessDescription').value;

        if (!industry || !businessName) {
            document.getElementById('colorSuggestions').classList.add('hidden');
            return;
        }

        const palette = this.colorPalettes[industry];
        if (palette) {
            this.showColorSuggestions(palette, industry);
        }
    }

    showColorSuggestions(palette, industry) {
        const colorSuggestions = document.getElementById('colorSuggestions');
        const recommendationText = document.getElementById('colorRecommendationText');
        
        // Show the suggestions
        colorSuggestions.classList.remove('hidden');
        
        // Update recommendation text
        recommendationText.textContent = `${palette.reasoning} for ${industry} businesses`;

        // Populate color grids
        this.populateColorGrid('primaryColors', palette.primary);
        this.populateColorGrid('secondaryColors', palette.secondary);
        this.populateColorGrid('accentColors', palette.accent);
    }

    populateColorGrid(containerId, colors) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';

        colors.forEach(color => {
            const colorDiv = document.createElement('div');
            colorDiv.className = 'w-8 h-8 rounded-full border-2 border-white shadow-md cursor-pointer hover:scale-110 transition-transform';
            colorDiv.style.backgroundColor = color;
            colorDiv.title = color;
            colorDiv.addEventListener('click', () => {
                this.selectSuggestedColor(color);
            });
            container.appendChild(colorDiv);
        });
    }

    selectSuggestedColor(color) {
        // Update the selected color in the main picker
        document.querySelectorAll('.color-picker').forEach(picker => {
            picker.classList.remove('selected');
        });

        // Add selected color to the form
        this.selectedColors.primary = color;
        
        // Visual feedback
        console.log(`Selected suggested color: ${color}`);
    }

    updateProgressSteps() {
        // This would update the visual progress indicators
        console.log(`Current step updated for option: ${this.selectedOption}`);
    }

    async generateLogos() {
        const formData = this.gatherFormData();
        
        if (!this.validateForm(formData)) {
            return;
        }

        // Show loading state
        this.showLoadingState();

        try {
            const response = await fetch('/generate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                // Redirect to results
                window.location.href = result.redirect_url;
            } else {
                this.showError(result.error || 'Generation failed. Please try again.');
            }
        } catch (error) {
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.hideLoadingState();
        }
    }

    gatherFormData() {
        return {
            generation_type: this.selectedOption,
            template_id: this.selectedTemplate,
            business_name: document.getElementById('businessName').value,
            industry: document.getElementById('industry').value,
            business_description: document.getElementById('businessDescription').value,
            style: this.selectedStyle,
            color_scheme: this.selectedColors,
            variations_count: document.getElementById('variationsCount').value,
            ai_provider: document.getElementById('aiProvider').value,
            custom_requirements: document.getElementById('customRequirements').value
        };
    }

    validateForm(formData) {
        if (!formData.business_name.trim()) {
            this.showError('Please enter your business name.');
            return false;
        }

        if (!formData.industry) {
            this.showError('Please select your industry.');
            return false;
        }

        if (this.selectedOption === 'template' && !this.selectedTemplate) {
            this.showError('Please select a template.');
            return false;
        }

        if (this.selectedOption === 'ai' && !this.selectedStyle) {
            this.showError('Please select a logo style.');
            return false;
        }

        return true;
    }

    showLoadingState() {
        const btn = document.getElementById('generateBtn');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-3"></i>Generating...';
        
        if (window.showLoading) {
            window.showLoading('AI is creating your perfect logos...');
        }
    }

    hideLoadingState() {
        const btn = document.getElementById('generateBtn');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic mr-3"></i>Generate AI Logos';
        
        if (window.hideLoading) {
            window.hideLoading();
        }
    }

    showError(message) {
        // Create or update error message
        let errorDiv = document.getElementById('errorMessage');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'errorMessage';
            errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4';
            document.getElementById('logoForm').prepend(errorDiv);
        }
        
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle mr-2"></i>${message}`;
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }
}

// Global functions for onclick handlers
window.selectOption = function(option) {
    if (window.logoGenerator) {
        window.logoGenerator.selectGenerationOption(option);
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.logoGenerator = new EnhancedLogoGenerator();
    console.log('Enhanced Logo Generator initialized');
});