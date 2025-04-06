
import streamlit as st
import os
from gem import *
from make_sense import *
from audio import *
import os
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "17000"


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
    understand the underlying meaning (guess what the speaker was actually saying). YOU DO NOT NEED TO REPHRASE, if a sentence is akready natural keep it. just when some words dont make sense it is probably due to the wrong transcription. that s what you have to change. this is the text:

    {text}
    """
    return chat([{"role": "user", "content": prompt}])


if __name__ == "__main__":

    st.set_page_config(
        page_title="Video Transcription & Cleanup", page_icon="🎥")
    st.header("Video Transcription & Cleanup (Italian)")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    uploaded_video = st.file_uploader("Upload a video file", type=[
        "mp4", "mov", "avi", "mkv"])

    if uploaded_video is not None:
        video_path = os.path.join("temp_video", uploaded_video.name)
        os.makedirs("temp_video", exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())
        st.success("✅ Video uploaded successfully!")

        try:
            with st.spinner("🔊 Extracting audio..."):
                audio_path = extract_audio(video_path)
        except Exception as e:
            st.error(f"❌ Audio extraction failed: {e}")
            st.stop()

        try:
            with st.spinner("📝 Transcribing audio..."):
                transcription = transcribe_audio(audio_path)
                save_transcription(transcription)
        except Exception as e:
            st.error(f"❌ Transcription failed: {e}")
            st.stop()

        st.subheader("Raw Transcription")
        st.text_area("Transcription", transcription, height=300)

        try:
            with st.spinner("🧠 Cleaning up the transcription..."):
                cleaned_text = make_sense(transcription)
        except Exception as e:
            st.error(f"❌ Cleanup failed: {e}")
            st.stop()

        st.subheader("🧽 Cleaned Transcription (Italian)")
        st.text_area("Cleaned Transcription", cleaned_text, height=300)

        st.success("✅ Done! You can copy the cleaned text above.")
