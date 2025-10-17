import os
import numpy as np
from gtts import gTTS
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
)
import time

def create_video(text="Awaken your divine potential.", output_filename="final_video.mp4"):
    try:
        print("🎬 [VideoGen] Starting video creation...")

        # --- Step 1: Voice synthesis ---
        print("🎤 [VideoGen] Generating voice-over...")
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("voice.mp3")

        # --- Step 2: Background image (simple gradient pulse) ---
        print("🖼️ [VideoGen] Generating animated background...")
        duration = 10  # seconds

        # Create a pulsating RGB array animation
        frames = []
        for i in range(0, duration * 10):
            r = int(100 + 50 * np.sin(i / 10))
            g = int(80 + 40 * np.cos(i / 15))
            b = int(120 + 60 * np.sin(i / 20))
            color = np.zeros((720, 1280, 3), dtype=np.uint8)
            color[:, :, 0] = r
            color[:, :, 1] = g
            color[:, :, 2] = b
            frames.append(ImageClip(color, duration=0.1))

        background = concatenate_videoclips(frames, method="compose")

        # --- Step 3: Combine with voice ---
        print("🔊 [VideoGen] Combining audio + video...")
        audio_clip = AudioFileClip("voice.mp3").volumex(1.1)
        video = background.set_audio(audio_clip)
        video = video.set_duration(audio_clip.duration)

        # --- Step 4: Export video ---
        print("💾 [VideoGen] Writing video file...")
        start_time = time.time()

        video.write_videofile(
            output_filename,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            threads=2,
            preset="ultrafast",
            ffmpeg_params=["-movflags", "+faststart"],
            verbose=False,
            logger=None
        )

        elapsed = time.time() - start_time
        print(f"✅ [VideoGen] Video export complete in {elapsed:.2f}s → {output_filename}")

        # --- Step 5: Cleanup ---
        background.close()
        video.close()
        audio_clip.close()
        print("🧹 [VideoGen] Cleanup complete!")

        return output_filename

    except Exception as e:
        print(f"❌ [VideoGen] Error: {e}")
        return None
