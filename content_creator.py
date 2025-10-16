#!/usr/bin/env python3
"""
Content Creator - Professional video generation
Creates spiritual videos with voiceover, subtitles, music, and effects
"""

import subprocess
from pathlib import Path
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import requests
import re
from config import Config

class ContentCreator:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
    
    def create_video(self, content):
        """Create professional video from content"""
        print("  📸 Generating image...", flush=True)
        image_path = self._generate_image(content['visual_prompt'])
        
        print("  🎙️ Generating voiceover...", flush=True)
        audio_path = self._generate_voiceover(content['script'])
        
        print("  📝 Creating subtitles...", flush=True)
        srt_path = self._create_subtitles(content['script'], audio_path)
        
        print("  🎬 Compositing video...", flush=True)
        video_path = self._composite_video(image_path, audio_path, srt_path)
        
        return video_path
    
    def _generate_image(self, prompt):
        """Generate spiritual image with DALL-E"""
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=f"Spiritual and serene: {prompt}. Vertical format, calming colors, sacred geometry, cinematic.",
            size="1024x1792",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        image_path = self.output_dir / 'spiritual_image.png'
        
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as f:
            f.write(img_data)
        
        return image_path
    
    def _generate_voiceover(self, script):
        """Generate voiceover using OpenAI TTS"""
        audio_path = self.output_dir / 'voiceover.mp3'
        
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Calm, spiritual voice
            input=script
        )
        
        response.stream_to_file(audio_path)
        return audio_path
    
    def _create_subtitles(self, script, audio_path):
        """Create SRT subtitle file with 3-5 word chunks"""
        # Get audio duration
        duration = self._get_audio_duration(audio_path)
        
        # Split script into 3-5 word chunks
        words = script.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(current_chunk) >= 3 and (len(current_chunk) >= 5 or word.endswith(('.', ',', '!', '?'))):
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Create SRT file with timing
        srt_path = self.output_dir / 'subtitles.srt'
        time_per_chunk = duration / len(chunks)
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks):
                start_time = i * time_per_chunk
                end_time = (i + 1) * time_per_chunk
                
                f.write(f"{i + 1}\n")
                f.write(f"{self._format_srt_time(start_time)} --> {self._format_srt_time(end_time)}\n")
                f.write(f"{chunk}\n\n")
        
        return srt_path
    
    def _get_audio_duration(self, audio_path):
        """Get audio duration using ffprobe"""
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    
    def _format_srt_time(self, seconds):
        """Format seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _composite_video(self, image_path, audio_path, srt_path):
        """Composite final video with all effects"""
        video_path = self.output_dir / 'spiritual_short.mp4'
        
        # Check for background music
        music_path = Path('assets/background_music.mp3')
        
        # Ken Burns effect: slow zoom from 100% to 110% with slight pan
        video_filter = (
            f"[0:v]scale={Config.VIDEO_WIDTH * 2}:{Config.VIDEO_HEIGHT * 2},"
            f"zoompan=z='min(zoom+0.0005,1.1)':d={Config.VIDEO_DURATION * 30}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"s={Config.VIDEO_WIDTH}x{Config.VIDEO_HEIGHT}:fps=30,"
            f"subtitles={srt_path}:force_style='"
            f"FontName=Arial,FontSize=24,Bold=1,PrimaryColour=&HFFFFFF&,"
            f"OutlineColour=&H000000&,BackColour=&H80000000&,BorderStyle=4,"
            f"Outline=2,Shadow=0,MarginV=80,Alignment=2'"
        )
        
        if music_path.exists():
            # Mix voiceover with background music (music at 20% volume)
            audio_filter = "[1:a]volume=1.0[voice];[2:a]volume=0.2[music];[voice][music]amix=inputs=2:duration=first[aout]"
            
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1', '-i', str(image_path),
                '-i', str(audio_path),
                '-i', str(music_path),
                '-filter_complex', f"{video_filter};{audio_filter}",
                '-map', '[v]',
                '-map', '[aout]',
                '-t', str(self._get_audio_duration(audio_path)),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                str(video_path)
            ]
        else:
            # No background music - just voiceover
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1', '-i', str(image_path),
                '-i', str(audio_path),
                '-filter_complex', f"{video_filter}[v]",
                '-map', '[v]',
                '-map', '1:a',
                '-t', str(self._get_audio_duration(audio_path)),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                str(video_path)
            ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return video_path
