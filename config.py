#!/usr/bin/env python3
"""
Configuration Manager for Spiritual Empire
Handles all environment variables and settings
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # YouTube Configuration
    YOUTUBE_TOKEN = json.loads(os.getenv('YOUTUBE_TOKEN', '{}'))
    
    # Content Settings
    CONTENT_THEMES = [
        "sacred geometry and divine patterns",
        "meditation and inner peace",
        "manifestation and conscious creation",
        "chakra alignment and energy healing",
        "ancient wisdom and modern spirituality"
    ]
    
    # Video Settings
    VIDEO_WIDTH = 1080
    VIDEO_HEIGHT = 1920  # Vertical for Shorts
    VIDEO_DURATION = 30  # seconds
    
    # Automation Settings
    POST_INTERVAL_HOURS = 8
    
    @classmethod
    def validate(cls):
        """Validate all required config"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set")
        if not cls.YOUTUBE_TOKEN:
            raise ValueError("YOUTUBE_TOKEN not set")
        return True
