import os
import numpy as np
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import time

def create_video(text="Awaken your divine potential.", output_filename="final_video.mp4"):
    try:
        print("🎬 [VideoGen] Starting video creation...")

        # Step 1: Voice synthesis using gTTS (creates valid MP3 without ffmpeg)
        print("🎤 [VideoGen] Generating voice-over...")
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save("voice.mp3")

        # Step 2: Background animation (gentle pulsing gradient)
        print("🖼️ [VideoGen] Generating animated background...")
        duration = 10  # seconds
        clips = []
        for i in range(duration * 10):
            r = int(120 + 60 * np.sin(i / 8))
            g = int(100 + 55 * np.cos(i / 10))
            b = int(140 + 45 * np.sin(i / 12))
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            frame[:, :, 0] = r
            frame[:, :, 1] = g
            frame[:, :, 2] = b
            clips.append(ImageClip(frame, duration=0.1))
        background = concatenate_videoclips(clips, method="compose")

        # Step 3: Combine with voice
        print("🔊 [VideoGen] Combining audio + video...")
        audio = AudioFileClip("voice.mp3").volumex(1.1)
        video = background.set_audio(audio).set_duration(audio.duration)

        # Step 4: Export video safely
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
        print(f"✅ [VideoGen] Video ready in {elapsed:.2f}s → {output_filename}")

        # Step 5: Cleanup
        background.close()
        video.close()
        audio.close()
        print("🧹 [VideoGen] Cleanup complete!")
        return output_filename

    except Exception as e:
        print(f"❌ [VideoGen] Error: {e}")
        return None
