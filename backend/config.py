"""
Centralized Configuration for Tea Stall Bench
"""

# Supported Content Types
CONTENT_TYPES = [
    'post',        # Short-form (social media, WhatsApp)
    'blog',        # Blog article
    'tutorial',    # Teaching/how-to
    'listicle',    # List-based ("10 Tips...")
    'newsletter',  # Email format
    'story'        # Narrative content
]

# Writing styles (unified style + tone) - ordered by temperature (factual → creative)
STYLES = [
    'technical',       # Precise, factual, detailed (temp: 0.3)
    'educational',     # Teaching, clear, structured (temp: 0.5)
    'professional',    # Business-like, polished (temp: 0.6)
    'friendly',        # Warm, casual, approachable (temp: 0.75)
    'inspirational',   # Motivating, uplifting (temp: 0.8)
    'storytelling'     # Narrative, engaging, compelling (temp: 0.9)
]

LENGTHS = ['short', 'medium', 'long']
CHANNELS = ['instagram', 'whatsapp', 'linkedin', 'email', 'blog']

# Channel-specific length guidelines (in words)
CHANNEL_LENGTH_GUIDES = {
    'instagram': {
        'short': '50-100 words',
        'medium': '100-150 words',
        'long': '150-200 words'
    },
    'whatsapp': {
        'short': '100-200 words',
        'medium': '200-400 words',
        'long': '400-600 words'
    },
    'linkedin': {
        'short': '150-300 words',
        'medium': '300-600 words',
        'long': '600-1000 words'
    },
    'email': {
        'short': '200-400 words',
        'medium': '400-800 words',
        'long': '800-1200 words'
    },
    'blog': {
        'short': '300-500 words',
        'medium': '600-1000 words',
        'long': '1200-1800 words'
    }
}
