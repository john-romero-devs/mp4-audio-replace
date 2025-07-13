# 🎧 mp4-audio-replace

A Python tool that lets you swap out the audio track in any video (MP4) with a new one — **without wrecking the quality**. Toss in a voiceover, add a meme soundtrack, or just vibe with your own audio. Optionally add some silence upfront if you need the timing just right.

---

## ✨ Features
- 🎵 Accepts `.mp3`, `.wav`, or `.mp4` (audio-only) as your new sound
- ⏱️ Add optional silence before the audio starts (great for syncing)
- 🎯 Zero re-encoding when possible — full quality preserved
- 🧰 Powered by [FFmpeg](https://ffmpeg.org/), so it's rock solid

---

## ⚙️ Requirements
- Python 3.x
- FFmpeg installed and added to your system path

---

## 🚀 How to Use
Just run the script and follow the prompts:
```bash
python mp4_audio_replace.py
```

You’ll be asked to:
- Pick the video file
- Pick the audio file (MP3, WAV, or MP4 with audio)
- Optionally enter how much silence (in seconds) to add before the audio kicks in

---

## 🎬 Use Cases
- Replace temp voiceovers with final mixes
- Add music to clips without touching the visuals
- Drop in meme sounds with frame-accurate timing
- Cleanly swap background tracks on your own content

> 🛑 This tool does **not** download, decrypt, or modify protected or copyrighted videos.
> Use it for stuff you own or have rights to.

---

## 🪪 License
MIT — totally free to use, remix, or build on.
