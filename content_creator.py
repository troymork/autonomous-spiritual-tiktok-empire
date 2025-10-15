#!/usr/bin/env python3
"""
Content Creator - Video generation with DALL-E + FFmpeg
Creates beautiful spiritual videos
"""

import subprocess
from pathlib import Path
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import requests
from config import Config

class ContentCreator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
    
    def create_video(self, content):
        """Create video from content"""
        # Generate image with DALL-E
        image_path = self._generate_image(content['visual_prompt'])
        
        # Add text overlay
        final_image = self._add_text_overlay(image_path, content['title'], content['script'])
        
        # Create video with FFmpeg
        video_path = self._create_video_from_image(final_image)
        
        return video_path
    
    def _generate_image(self, prompt):
        """Generate spiritual image with DALL-E"""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=f"Spiritual and serene: {prompt}. Vertical format, calming colors, sacred geometry.",
            size="1024x1792",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        image_path = self.output_dir / 'spiritual_image.png'
        
        # Download image
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as f:
            f.write(img_data)
        
        return image_path
    
    def _add_text_overlay(self, image_path, title, script):
        """Add text overlay to image"""
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Simple text overlay (would use proper fonts in production)
        # For now, just save the image as-is
        overlay_path = self.output_dir / 'spiritual_overlay.png'
        img.save(overlay_path)
        return overlay_path
    
    def _create_video_from_image(self, image_path):
        """Create video from static image using FFmpeg"""
        video_path = self.output_dir / 'spiritual_short.mp4'
        
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(image_path),
            '-t', str(Config.VIDEO_DURATION),
            '-vf', f'scale={Config.VIDEO_WIDTH}:{Config.VIDEO_HEIGHT}',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            str(video_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return video_path
