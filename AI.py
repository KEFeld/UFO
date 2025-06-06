import os
import subprocess
import sounddevice as sd
from scipy.io.wavfile import write
import time

# === CONFIGURATION ===
DURATION = 5  # seconds to record
SAMPLE_RATE = 16000  # whisper expects 16kHz mono
MODEL_PATH = "models/ggml-base.en.bin"
WAV_PATH = "input.wav"
WHISPER_PATH = "build/bin/Release/whisper.exe"  # Adjust if different

def record_audio():
    print(f"🎙️  Recording for {DURATION} seconds...")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    write(WAV_PATH, SAMPLE_RATE, recording)
    print("✅ Recording complete.")

def run_whisper():
    print("🧠 Transcribing with Whisper...")
    result = subprocess.run([
        WHISPER_PATH,
        "-m", MODEL_PATH,
        "-f", WAV_PATH,
        "-otxt",
        "-of", "result"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Whisper failed:", result.stderr)
        return

    with open("result.txt", "r", encoding="utf-8") as f:
        transcript = f.read().strip()
    print("📝 Transcription:", transcript)

if __name__ == "__main__":
    record_audio()
    time.sleep(1)
    run_whisper()
