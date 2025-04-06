import sys
import subprocess
import whisper

# Step 1: Extract audio from video


def extract_audio(video_path, audio_path="extracted_audio.wav"):
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec",
               "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path]
    subprocess.run(command, check=True)
    return audio_path

# Step 2: Transcribe using Whisper


def transcribe_audio(audio_path):
    # You can also try: "tiny", "small", "medium", "large"
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Step 3: Save transcription to a text file


def save_transcription(text, output_file="transcription.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)


# Main script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ No video file provided. Using default video 'Untitled.mov'")
        video_path = "Untitled.mov"
    else:
        video_path = sys.argv[1]

    audio_path = extract_audio(video_path)
    transcription = transcribe_audio(audio_path)
    save_transcription(transcription)
    print("✅ Transcription saved to transcription.txt")
