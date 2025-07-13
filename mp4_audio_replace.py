import subprocess
import os
import tempfile
import shutil

def sanitize(filename):
    return filename.strip().strip('"').strip("'")

def file_exists_or_exit(path):
    if not os.path.isfile(path):
        print(f"❌ File not found: {path}")
        exit()

def win_path(path):
    return path.replace("\\", "/")

# === Step 1: Get user input ===
video_file = sanitize(input("🎥 Enter the name of the original video file (with extension): "))
audio_file = sanitize(input("🎵 Enter the name of the new sound file (.mp3 or .mp4): "))
silence_duration = input("🤫 Silence to add at start? (Enter seconds like 0.0 or 1.25): ").strip()

file_exists_or_exit(video_file)
file_exists_or_exit(audio_file)

# === Step 2: Create temp workspace ===
temp_dir = tempfile.mkdtemp()
final_audio = os.path.join(temp_dir, "final_audio.mp3")

# === Step 3: Extract .mp3 if source is .mp4 ===
ext = os.path.splitext(audio_file)[1].lower()
clean_audio_mp3 = os.path.join(temp_dir, "audio_clean.mp3")

if ext == ".mp4":
    print("🔄 Extracting audio from mp4 as mp3...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", audio_file,
        "-q:a", "0",   # highest VBR
        "-map", "a",
        clean_audio_mp3
    ])

elif ext == ".mp3":
    shutil.copy(audio_file, clean_audio_mp3)

elif ext == ".wav":
    print("🎚️ Converting WAV to MP3 at 320kbps CBR...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", audio_file,
        "-b:a", "320k",  # Constant Bitrate
        clean_audio_mp3
    ])

else:
    print("❌ Unsupported audio format. Use .mp3, .wav, or .mp4 with audio.")
    exit()


# === Step 4: Add silence (if any) ===
if silence_duration and float(silence_duration) > 0:
    print(f"⏱️ Generating {silence_duration}s of silence...")
    silence_mp3 = os.path.join(temp_dir, "silence.mp3")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", silence_duration,
        "-q:a", "0",  # highest mp3 quality
        silence_mp3
    ])

    # Make concat list
    concat_list = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_list, "w") as f:
        f.write(f"file '{win_path(silence_mp3)}'\n")
        f.write(f"file '{win_path(clean_audio_mp3)}'\n")

    # Concatenate with no re-encoding
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        final_audio
    ])
else:
    # No silence, just use the original MP3
    shutil.copy(clean_audio_mp3, final_audio)

# === Step 5: Replace audio in original video ===
base, _ = os.path.splitext(video_file)
output_file = f"{base}_with_new_audio.mp4"

print("🎬 Merging new audio into video...")
subprocess.run([
    "ffmpeg", "-y",
    "-i", video_file,
    "-i", final_audio,
    "-c:v", "copy",
    "-c:a", "copy",
    "-map", "0:v:0",
    "-map", "1:a:0",
    output_file
])

# === Cleanup ===
shutil.rmtree(temp_dir)
print(f"✅ Done! Saved as: {output_file}")
