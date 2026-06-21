import os
import sys

# Point Python to the src/ directory so it can find your modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from transcriber.transcriber import LocalTranscriber
from utils.logger import Logger

def test_music_transcription():
    # Define the expected path to the MP3 file
    audio_filename = "thriller.mp3"
    audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), audio_filename))

    if not os.path.exists(audio_path):
        Logger.log_error(f"Could not find '{audio_filename}'. Please place it in the tests/ folder.")
        return

    print(f"\n--- Stress Testing Whisper with '{audio_filename}' ---")
    
    # 1. Simulate the Streamlit UI reading the uploaded file into raw bytes
    Logger.log_info(f"Reading {audio_filename} into memory buffer...")
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    # 2. Initialize the transcriber (using 'base' for standard laptops)
    transcriber = LocalTranscriber(MODEL_SIZE="small")

    # 3. Run the extraction pipeline
    print("\nBeginning transcription... (Watch your laptop fans, this might take a minute!)")
    transcript = transcriber.transcribe_binary(audio_bytes, FILE_EXTENSION="mp3", LANGUAGE="en")

    # 4. Output the results
    print("\n" + "="*50)
    print("--- FINAL TRANSCRIPT ---")
    print("="*50)
    print(transcript)
    Logger.log_info(transcript) 
    print("="*50 + "\n")

if __name__ == "__main__":
    test_music_transcription()