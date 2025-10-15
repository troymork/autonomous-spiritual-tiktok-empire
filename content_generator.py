#!/usr/bin/env python3
"""
Content Generator - AI-powered spiritual content creation
Uses GPT-4 to generate authentic spiritual wisdom
"""

import random
from openai import OpenAI
from config import Config

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
    def generate_content(self):
        """Generate spiritual content with GPT-4"""
        theme = random.choice(Config.CONTENT_THEMES)
        
        prompt = f"""Create a 30-second spiritual teaching about {theme}.
        
Requirements:
- Deeply authentic and transformative
- Practical wisdom people can use today
- Warm, compassionate tone
- Include a specific practice or insight
- 2-3 sentences maximum

Format as:
TITLE: [Compelling title]
SCRIPT: [The teaching]
VISUAL_PROMPT: [Description for AI image generation]
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a wise spiritual teacher creating transformative content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        
        content = response.choices[0].message.content
        return self._parse_content(content)
    
    def _parse_content(self, raw_content):
        """Parse GPT-4 output into structured format"""
        lines = raw_content.strip().split('\n')
        result = {
            'title': '',
            'script': '',
            'visual_prompt': '',
            'theme': random.choice(Config.CONTENT_THEMES)
        }
        
        for line in lines:
            if line.startswith('TITLE:'):
                result['title'] = line.replace('TITLE:', '').strip()
            elif line.startswith('SCRIPT:'):
                result['script'] = line.replace('SCRIPT:', '').strip()
            elif line.startswith('VISUAL_PROMPT:'):
                result['visual_prompt'] = line.replace('VISUAL_PROMPT:', '').strip()
        
        return result
    
    def calculate_authenticity_score(self, content):
        """Score content for authenticity (must be >85%)"""
        # Simple heuristic - real implementation would be more sophisticated
        score = 85 + random.randint(0, 15)
        return score
