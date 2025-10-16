from moviepy.editor import *
from gtts import gTTS

def create_video(script_text, voice_output="voice.mp3", subtitles=True, motion_background=True):
    # generate voice-over
    tts = gTTS(text=script_text, lang="en")
    tts.save(voice_output)
    audio = AudioFileClip(voice_output)
    duration = audio.duration

    # background animation
    bg = ColorClip(size=(1080, 1920), color=(10, 10, 20)).set_duration(duration)
    if motion_background:
        flare = ColorClip(size=(200, 200), color=(255, 180, 80)).set_opacity(0.5)
        flare = flare.set_position(lambda t: (400 + 300 * np.sin(t), 800 + 200 * np.cos(t))).set_duration(duration)
        bg = CompositeVideoClip([bg, flare])

    # subtitles
    if subtitles:
        text = TextClip(script_text, fontsize=36, color="white", method="caption", size=(1000, None))
        text = text.set_position(("center", "bottom")).set_duration(duration)
        video = CompositeVideoClip([bg, text]).set_audio(audio)
    else:
        video = bg.set_audio(audio)

    video.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
    return "final_video.mp4"
