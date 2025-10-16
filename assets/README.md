# Background Music Setup

## Adding Background Music (Optional)

To add cinematic background music to your videos:

1. Download a royalty-free spiritual/cinematic music track
2. Name it `background_music.mp3`
3. Place it in the `assets/` folder
4. Videos will automatically include it at 20% volume under the voiceover

## Recommended Sources for Royalty-Free Music

### Free Options:
- **YouTube Audio Library**: https://studio.youtube.com/channel/UC.../music
  - Filter by mood: "Calm", "Inspirational", "Ambient"
- **Pixabay Music**: https://pixabay.com/music/
  - Search: "meditation", "spiritual", "ambient"
- **Free Music Archive**: https://freemusicarchive.org/
  - Genre: Ambient, New Age

### Paid Options (Higher Quality):
- **Epidemic Sound**: https://www.epidemicsound.com/
- **Artlist**: https://artlist.io/
- **Soundstripe**: https://www.soundstripe.com/

## Current Status

- ✅ Video generation works WITHOUT music (voiceover only)
- 🎵 Add `assets/background_music.mp3` to enable background music

## File Requirements

- Format: MP3
- Length: 30+ seconds (will loop if needed)
- Volume: Will be automatically set to 20% (configurable in `content_creator.py`)
