from gem import chat
import sys


def file_to_text(file):
    try:
        with open(file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: The specified file was not found."
    except Exception as e:
        return f"Error reading file: {e}"


def make_sense(text):
    prompt = f"""
    This is a text file. It comes from a transcription of the audio of a video. the words and sentences are 
    often misunderstood and do not make sense. try to make it natural, grammatically correct and to
    understand the underlying menaing (guess what the speaker was actually saying). keep it in italian. this is the text:

    {text}
    """
    return chat([{"role": "user", "content": prompt}])


if __name__ == "__main__":
    file_path = "transcription.txt"  # Replace with your file path
    text = file_to_text(file_path)
    cleaned_text = make_sense(text)
    with open('cleaned_transcription.txt', 'w') as f:
        f.write(cleaned_text)
    print("Cleaned text saved to cleaned_transcription.txt")
