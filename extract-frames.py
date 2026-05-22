"""Extract a representative still frame from each feature video as a JPG poster."""
import os
import cv2

SRC = r"C:\Users\shake\reelcook-landing\assets\videos"
DST = r"C:\Users\shake\reelcook-landing\assets\posters"
os.makedirs(DST, exist_ok=True)

# Map: video filename -> seconds into the video to grab (chosen to capture meaningful UI state)
videos = [
    ("fridge.mp4",       0.20),
    ("dinner.mp4",       0.20),
    ("swipe.mp4",        0.40),
    ("weekly.mp4",       0.30),
    ("shabbat.mp4",      0.30),
    ("shopping.mp4",     0.30),
    ("cook-mode.mp4",    0.30),
    ("translate.mp4",    0.40),
    ("kosher.mp4",       0.30),
    ("nutrition.mp4",    0.30),
]

for name, fraction in videos:
    path = os.path.join(SRC, name)
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"[fail] cannot open {path}")
        continue
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    target = int(total * fraction) if total else 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, target)
    ok, frame = cap.read()
    if not ok:
        # fallback: try first frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ok, frame = cap.read()
    cap.release()
    if not ok:
        print(f"[fail] could not read frame from {name}")
        continue
    out = os.path.join(DST, name.replace(".mp4", ".jpg"))
    cv2.imwrite(out, frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
    h, w = frame.shape[:2]
    print(f"[ok]  {name} -> {os.path.basename(out)} ({w}x{h})")

print("Done.")
