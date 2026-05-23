"""
Compress feature videos for the web: H.264, 720p max width, CRF 28, AAC audio stripped.
Overwrites the originals in assets/videos/ after backing them up to assets/videos-original/.
"""
import os
import shutil
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SRC = r"C:\Users\shake\reelcook-landing\assets\videos"
BACKUP = r"C:\Users\shake\reelcook-landing\assets\videos-original"

os.makedirs(BACKUP, exist_ok=True)

videos = [
    "fridge.mp4", "dinner.mp4", "swipe.mp4", "weekly.mp4",
    "shabbat.mp4", "shopping.mp4", "cook-mode.mp4",
    "translate.mp4", "kosher.mp4", "nutrition.mp4",
    "hero-instagram.mp4",
]

def size_mb(path):
    return os.path.getsize(path) / 1024 / 1024

for name in videos:
    src_path = os.path.join(SRC, name)
    backup_path = os.path.join(BACKUP, name)
    if not os.path.exists(src_path):
        print(f"[skip] {name} not found")
        continue
    # Back up the original once
    if not os.path.exists(backup_path):
        shutil.copy2(src_path, backup_path)
        print(f"[backup] {name} -> videos-original/")
    before = size_mb(backup_path)
    tmp_out = src_path + ".tmp.mp4"
    cmd = [
        FFMPEG, "-y", "-i", backup_path,
        # Scale to max 720px width, keep aspect, ensure even dimensions (codec requirement)
        "-vf", "scale='min(720,iw)':-2",
        # H.264 baseline-ish for max compatibility, CRF 28 is web-friendly mid quality
        "-c:v", "libx264", "-preset", "medium", "-crf", "28",
        # Strip audio (these are muted UI demos anyway)
        "-an",
        # MOV-friendly settings for fast start (metadata at the front of the file)
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        tmp_out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[fail] {name}")
        print(result.stderr[-500:])
        if os.path.exists(tmp_out):
            os.remove(tmp_out)
        continue
    os.replace(tmp_out, src_path)
    after = size_mb(src_path)
    pct = 100 * (1 - after / before)
    print(f"[ok]  {name}: {before:.1f}MB -> {after:.1f}MB  ({pct:.0f}% smaller)")

print("Done. Originals saved in assets/videos-original/ for safekeeping.")
