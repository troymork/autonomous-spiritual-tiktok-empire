#!/usr/bin/env python3
"""
Empire Engine - Main automation orchestrator
Runs the complete content cycle every 8 hours
"""

import time
import schedule
from datetime import datetime
from config import Config
from content_generator import ContentGenerator
from content_creator import ContentCreator
from youtube_publisher import YouTubePublisher

class EmpireEngine:
    def __init__(self):
        Config.validate()
        self.generator = ContentGenerator()
        self.creator = ContentCreator()
        self.publisher = YouTubePublisher()
        self.stats = {'total_posts': 0, 'last_post': None}
    
    def run_cycle(self):
        """Execute one complete content cycle"""
        try:
            print(f"\n{'='*60}")
            print(f"🔮 Starting content cycle at {datetime.now()}")
            print(f"{'='*60}\n")
            
            # 1. Generate content
            print("📝 Generating spiritual content...")
            content = self.generator.generate_content()
            authenticity = self.generator.calculate_authenticity_score(content)
            
            if authenticity < 85:
                print(f"⚠️ Authenticity score too low: {authenticity}%. Regenerating...")
                return self.run_cycle()
            
            print(f"✅ Content generated (Authenticity: {authenticity}%)")
            print(f"   Title: {content['title']}")
            
            # 2. Create video
            print("\n🎨 Creating video...")
            video_path = self.creator.create_video(content)
            print(f"✅ Video created: {video_path}")
            
            # 3. Publish to YouTube
            print("\n📤 Publishing to YouTube...")
            video_id = self.publisher.publish(video_path, content)
            print(f"✅ Published! Video ID: {video_id}")
            
            # 4. Update stats
            self.stats['total_posts'] += 1
            self.stats['last_post'] = datetime.now().isoformat()
            
            print(f"\n🎉 Cycle complete! Total posts: {self.stats['total_posts']}")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"❌ Error in cycle: {e}")
            raise
    
    def start(self):
        """Start the automation engine"""
        print("🚀 Spiritual Empire Engine Starting...")
        print(f"⏰ Posting every {Config.POST_INTERVAL_HOURS} hours")
        
        # Run first cycle immediately
        self.run_cycle()
        
        # Schedule recurring cycles
        schedule.every(Config.POST_INTERVAL_HOURS).hours.do(self.run_cycle)
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == '__main__':
    engine = EmpireEngine()
    engine.start()
