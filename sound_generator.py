import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import io
from pydub import AudioSegment

# Function to generate a sine wave
def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return sine_wave

# Function to simulate ambient and meditation sounds
def simulate_sound(duration, frequencies, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sound_wave = np.zeros_like(t)
    for freq in frequencies:
        sound_wave += 0.1 * np.sin(2 * np.pi * freq * t)
    return sound_wave / np.max(np.abs(sound_wave))  # Normalize

# Function to save audio to a BytesIO object (WAV format)
def save_audio_to_bytes(audio, sample_rate=44100):
    audio = np.int16(audio * 32767)
    byte_io = io.BytesIO()
    write(byte_io, sample_rate, audio)
    byte_io.seek(0)
    return byte_io

# Function to convert WAV to MP3
def convert_to_mp3(wav_bytes):
    audio = AudioSegment.from_wav(io.BytesIO(wav_bytes))
    mp3_bytes = io.BytesIO()
    audio.export(mp3_bytes, format="mp3")
    mp3_bytes.seek(0)
    return mp3_bytes

# Streamlit App
st.title("Good Vibes Sound Generator 🌿")
st.write("Generate soothing Ambient & Meditation sounds.")

# Sidebar for user input
st.sidebar.header("Settings")
sound_type = st.sidebar.selectbox(
    "Choose a sound type:",
    [
        "Deep Om Chanting",
        "Tibetan Singing Bowls",
        "Crystal Bowls Healing Sounds",
        "Soft Bell Chimes",
        "Ethereal Choir Voices",
        "Angelic Choir Pads",
        "Solfeggio Tones with Soft Drone",
        "Monastic Gregorian Chants",
        "Zen Temple Bells",
        "Slow Deep String Pads",
        "Cosmic Drone Sounds",
        "Astral Space Ambience",
        "Cosmic Wind Effects",
        "Mystical Flute Melodies"
    ]
)

duration = st.sidebar.slider("Duration (seconds):", 1, 36000, 600)  # Up to 10 hours

# Generate and play sound
if st.button("Generate Sound"):
    st.write(f"Generating {sound_type} for {duration} seconds...")

    if sound_type == "Deep Om Chanting":
        audio = simulate_sound(duration, [136.1])
    elif sound_type == "Tibetan Singing Bowls":
        audio = simulate_sound(duration, [250, 500, 1000])
    elif sound_type == "Crystal Bowls Healing Sounds":
        audio = simulate_sound(duration, [432, 528, 639])
    elif sound_type == "Soft Bell Chimes":
        audio = simulate_sound(duration, [600, 800])
    elif sound_type == "Ethereal Choir Voices":
        audio = simulate_sound(duration, [220, 440, 880])
    elif sound_type == "Angelic Choir Pads":
        audio = simulate_sound(duration, [523.25, 659.25, 783.99])
    elif sound_type == "Solfeggio Tones with Soft Drone":
        audio = simulate_sound(duration, [396, 417, 528])
    elif sound_type == "Monastic Gregorian Chants":
        audio = simulate_sound(duration, [150, 300])
    elif sound_type == "Zen Temple Bells":
        audio = simulate_sound(duration, [250, 400])
    elif sound_type == "Slow Deep String Pads":
        audio = simulate_sound(duration, [100, 200])
    elif sound_type == "Cosmic Drone Sounds":
        audio = simulate_sound(duration, [50, 100])
    elif sound_type == "Astral Space Ambience":
        audio = simulate_sound(duration, [20, 40])
    elif sound_type == "Cosmic Wind Effects":
        audio = simulate_sound(duration, [10, 20])
    elif sound_type == "Mystical Flute Melodies":
        audio = simulate_sound(duration, [440, 660])
    else:
        st.error("Sound type not implemented yet.")
        st.stop()

    # Save audio to BytesIO and stream it
    audio_bytes = save_audio_to_bytes(audio)
    st.audio(audio_bytes, format="audio/wav")

    # Download buttons
    st.write("### Download Audio")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download as WAV",
            data=audio_bytes,
            file_name=f"{sound_type}_{duration}s.wav",
            mime="audio/wav",
        )
    with col2:
        mp3_bytes = convert_to_mp3(audio_bytes.getvalue())
        st.download_button(
            label="Download as MP3",
            data=mp3_bytes,
            file_name=f"{sound_type}_{duration}s.mp3",
            mime="audio/mp3",
        )

    st.success("Sound generated! Press the play button above to listen.")
