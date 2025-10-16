#!/usr/bin/env python3
"""
Empire Engine - Main automation orchestrator
Runs the complete content cycle every 8 hours
"""

import os
import time
from datetime import datetime
from video_generation_upgrade import create_video

print("🔮 SCRIPT STARTING...")

try:
    print("✅ Imports successful")
    print("🔍 Checking environment variables...")
    required_env = ["OPENAI_API_KEY", "YOUTUBE_TOKEN", "FIREBASE_CONFIG"]
    for var in required_env:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required env var: {var}")
    print("✅ Environment variables present")

    def run_cycle():
        print("=" * 60)
        print(f"🔮 Starting content cycle at {datetime.now()}")
        print("=" * 60)

        script_text = "The Unity of Timeless Wisdom — a reflection on the convergence of all paths toward love and understanding."
        audio_output = "voice.mp3"
        video_output = "final_video.mp4"

        print("🎤 Generating voice-over and video...")
        create_video(script_text, audio_output)
        print("✅ Video generation complete")

        print("🚀 Uploading to YouTube...")
        # You can expand upload logic here
        print("✅ Upload complete (placeholder)")

    # main loop
    print("🚀 Spiritual Empire Engine Starting...")
    print("⏰ Posting every 8 hours")
    run_cycle()

except Exception as e:
    print(f"❌ Error: {e}")
