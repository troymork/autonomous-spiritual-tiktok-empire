import os
import numpy as np
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import time
from pydub import AudioSegment  # use pydub to convert mp3 to wav safely

def create_video(text="Awaken your divine potential.", output_filename="final_video.mp4"):
    try:
        print("🎬 [VideoGen] Starting video creation...")

        # 1. Voice synthesis via gTTS (writes MP3)
        print("🎤 [VideoGen] Generating voice-over (mp3)...")
        mp3_path = "voice.mp3"
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(mp3_path)

        # 2. Convert MP3 to WAV to avoid stream issues
        print("🔄 [VideoGen] Converting MP3 → WAV")
        wav_path = "voice.wav"
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")

        # Now use the WAV file
        audio_clip = AudioFileClip(wav_path)

        # 3. Generate background animation
        print("🖼️ [VideoGen] Generating animated background...")
        duration = audio_clip.duration
        clips = []
        fps = 24
        frames = int(duration * fps)
        for i in range(frames):
            r = int(120 + 60 * np.sin(i / fps * np.pi * 2 / 5))
            g = int(100 + 55 * np.cos(i / fps * np.pi * 2 / 7))
            b = int(140 + 45 * np.sin(i / fps * np.pi * 2 / 11))
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            frame[:, :, 0] = r
            frame[:, :, 1] = g
            frame[:, :, 2] = b
            clips.append(ImageClip(frame, duration=1.0 / fps))
        background = concatenate_videoclips(clips, method="compose")

        # 4. Combine video + audio
        print("🔊 [VideoGen] Combining audio + video...")
        video = background.set_audio(audio_clip).set_duration(audio_clip.duration)

        # 5. Export video with safe parameters
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

        # Cleanup
        background.close()
        video.close()
        audio_clip.close()
        return output_filename

    except Exception as e:
        print(f"❌ [VideoGen] Error: {e}")
        return None
