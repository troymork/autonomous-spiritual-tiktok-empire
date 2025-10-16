#!/usr/bin/env python3
"""
Empire Engine - Main automation orchestrator
Runs the complete content cycle every 8 hours
"""

import sys
print("🔮 SCRIPT STARTING...", flush=True)
sys.stdout.flush()

import time
import schedule
from datetime import datetime

print("✅ Imports: time, schedule, datetime", flush=True)

try:
    from config import Config
    print("✅ Config imported", flush=True)
except Exception as e:
    print(f"❌ Config import failed: {e}", flush=True)
    raise

try:
    from content_generator import ContentGenerator
    print("✅ ContentGenerator imported", flush=True)
except Exception as e:
    print(f"❌ ContentGenerator import failed: {e}", flush=True)
    raise

try:
    from content_creator import ContentCreator
    print("✅ ContentCreator imported", flush=True)
except Exception as e:
    print(f"❌ ContentCreator import failed: {e}", flush=True)
    raise

try:
    from youtube_publisher import YouTubePublisher
    print("✅ YouTubePublisher imported", flush=True)
except Exception as e:
    print(f"❌ YouTubePublisher import failed: {e}", flush=True)
    raise

class EmpireEngine:
    def __init__(self):
        print("🔮 Initializing EmpireEngine...", flush=True)
        try:
            Config.validate()
            print("✅ Config validated", flush=True)
        except Exception as e:
            print(f"❌ Config validation failed: {e}", flush=True)
            raise
        
        try:
            self.generator = ContentGenerator()
            print("✅ ContentGenerator initialized", flush=True)
        except Exception as e:
            print(f"❌ ContentGenerator init failed: {e}", flush=True)
            raise
            
        try:
            self.creator = ContentCreator()
            print("✅ ContentCreator initialized", flush=True)
        except Exception as e:
            print(f"❌ ContentCreator init failed: {e}", flush=True)
            raise
            
        try:
            self.publisher = YouTubePublisher()
            print("✅ YouTubePublisher initialized", flush=True)
        except Exception as e:
            print(f"❌ YouTubePublisher init failed: {e}", flush=True)
            raise
            
        self.stats = {'total_posts': 0, 'last_post': None}
        print("✅ EmpireEngine ready!", flush=True)
    
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
    print("🚀 Main block executing...", flush=True)
    try:
        engine = EmpireEngine()
        print("✅ Engine created, calling start()...", flush=True)
        engine.start()
    except Exception as e:
        print(f"❌ Fatal error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
