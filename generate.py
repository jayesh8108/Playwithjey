
import argparse
import json
import pathlib
import subprocess
import textwrap
import wave
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def run(*args):
    subprocess.run([str(x) for x in args], check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format", choices=["short", "long"],
        default="short"
    )
    args = parser.parse_args()

    w, h = (720, 1280) if args.format == "short" else (1280, 720)

    topics = [
        ("GTA 6", "PLAYWITHJEY ORIGINAL ANALYSIS"),
        ("VICE CITY", "What could the open world offer?"),
        ("GAMEPLAY", "What features are you excited for?"),
        ("ROCKSTAR", "Wait for official announcements"),
        ("YOUR OPINION", "Tell us in the comments!")
    ]

    frames = []
    for i, (heading, subtitle) in enumerate(topics):
        img = Image.new("RGB", (w, h), (12, 18, 35))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, w, 18), fill=(255, 65, 120))
        d.text((40, 65), "PLAYWITHJEY",
               font=ImageFont.truetype(FONT, 35),
               fill="white")
        d.text((40, h // 3), heading,
               font=ImageFont.truetype(FONT, 58),
               fill=(255, 90, 150))
        f = ImageFont.truetype(FONT, 27)
        y = h // 3 + 110
        for line in textwrap.wrap(subtitle, 30):
            d.text((40, y), line, font=f, fill="white")
            y += 45
        d.text((40, h - 100), "Original Commentary | PlayWithJey",
               font=ImageFont.truetype(FONT, 19),
               fill=(180, 190, 210))
        path = OUT / f"frame{i}.png"
        img.save(path)
        frames.append(path)

    # Generate silent audio for an original visual explainer.
    audio = OUT / "silent.wav"
    with wave.open(str(audio), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(22050)
        wf.writeframes(b"\x00\x00" * 22050 * 20)

    clips = []
    for i, frame in enumerate(frames):
        clip = OUT / f"clip{i}.mp4"
        run("ffmpeg", "-y", "-loop", "1",
            "-framerate", "25", "-i", frame,
            "-t", "4", "-c:v", "libx264",
            "-pix_fmt", "yuv420p", clip)
        clips.append(clip)

    concat = OUT / "concat.txt"
    concat.write_text(
        "".join(f"file '{p.resolve()}'\n" for p in clips)
    )

    video = OUT / f"playwithjey_{args.format}.mp4"
    run("ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat, "-i", audio,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest", video)

    (OUT / "metadata.txt").write_text(
        "Title: GTA 6 - What We Want To See | PlayWithJey\n"
        "Description: Original GTA 6 discussion and analysis. "
        "Not official gameplay footage.\n"
        "#GTA6 #PlayWithJey #Gaming"
    )

    print("Video created:", video)

if __name__ == "__main__":
    main()
 
