#!/usr/bin/env python3
"""
Empire Engine - Main automation orchestrator
Runs the complete content cycle every 8 hours
"""

import sys
import os
print("🔮 SCRIPT STARTING...", flush=True)
sys.stdout.flush()

import time
import schedule
from datetime import datetime

print("✅ Imports: time, schedule, datetime", flush=True)

# Check environment variables immediately
print("🔍 Checking environment variables...", flush=True)
if not os.getenv('OPENAI_API_KEY'):
    print("❌ OPENAI_API_KEY not set!", flush=True)
    sys.exit(1)
if not os.getenv('YOUTUBE_TOKEN'):
    print("❌ YOUTUBE_TOKEN not set!", flush=True)
    sys.exit(1)
print("✅ Environment variables present", flush=True)

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
            print(f"\n{'='*60}", flush=True)
            print(f"🔮 Starting content cycle at {datetime.now()}", flush=True)
            print(f"{'='*60}\n", flush=True)
            
            # 1. Generate content
            print("📝 Generating spiritual content...", flush=True)
            sys.stdout.flush()
            content = self.generator.generate_content()
            authenticity = self.generator.calculate_authenticity_score(content)
            
            if authenticity < 85:
                print(f"⚠️ Authenticity score too low: {authenticity}%. Regenerating...", flush=True)
                return self.run_cycle()
            
            print(f"✅ Content generated (Authenticity: {authenticity}%)", flush=True)
            print(f"   Title: {content['title']}", flush=True)
            
            # 2. Create video
            print("\n🎨 Creating video...", flush=True)
            sys.stdout.flush()
            video_path = self.creator.create_video(content)
            print(f"✅ Video created: {video_path}", flush=True)
            
            # 3. Publish to YouTube
            print("\n📤 Publishing to YouTube...", flush=True)
            sys.stdout.flush()
            video_id = self.publisher.publish(video_path, content)
            print(f"✅ Published! Video ID: {video_id}", flush=True)
            
            # 4. Update stats
            self.stats['total_posts'] += 1
            self.stats['last_post'] = datetime.now().isoformat()
            
            print(f"\n🎉 Cycle complete! Total posts: {self.stats['total_posts']}", flush=True)
            print(f"{'='*60}\n", flush=True)
            
        except Exception as e:
            print(f"❌ Error in cycle: {e}", flush=True)
            import traceback
            traceback.print_exc()
            raise
    
    def start(self):
        """Start the automation engine"""
        print("🚀 Spiritual Empire Engine Starting...", flush=True)
        print(f"⏰ Posting every {Config.POST_INTERVAL_HOURS} hours", flush=True)
        sys.stdout.flush()
        
        # Run first cycle immediately
        print("▶️ Running first cycle now...", flush=True)
        self.run_cycle()
        
        # Schedule recurring cycles
        print(f"✅ First cycle complete. Next cycle in {Config.POST_INTERVAL_HOURS} hours", flush=True)
        schedule.every(Config.POST_INTERVAL_HOURS).hours.do(self.run_cycle)
        
        # Keep running
        print("🔄 Scheduler running. Waiting for next cycle...", flush=True)
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
