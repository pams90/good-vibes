import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import io
import os

# Function to generate white noise
def generate_white_noise(duration, sample_rate=44100):
    noise = np.random.uniform(-1, 1, int(sample_rate * duration))
    return noise

# Function to generate pink noise
def generate_pink_noise(duration, sample_rate=44100):
    # Pink noise has a power spectral density that decreases by 3 dB per octave
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
    a = [1, -2.494956002, 2.017265875, -0.522189400]
    white_noise = np.random.uniform(-1, 1, int(sample_rate * duration))
    pink_noise = np.zeros_like(white_noise)
    for i in range(len(white_noise)):
        pink_noise[i] = (
            b[0] * white_noise[i]
            + b[1] * (white_noise[i - 1] if i > 0 else 0)
            + b[2] * (white_noise[i - 2] if i > 1 else 0)
            + b[3] * (white_noise[i - 3] if i > 2 else 0)
            - a[1] * (pink_noise[i - 1] if i > 0 else 0)
            - a[2] * (pink_noise[i - 2] if i > 1 else 0)
            - a[3] * (pink_noise[i - 3] if i > 2 else 0)
        )
    return pink_noise

# Function to generate brown noise
def generate_brown_noise(duration, sample_rate=44100):
    white_noise = np.random.uniform(-1, 1, int(sample_rate * duration))
    brown_noise = np.cumsum(white_noise)
    brown_noise = brown_noise / np.max(np.abs(brown_noise))  # Normalize
    return brown_noise

# Function to generate a sine wave
def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return sine_wave

# Function to save audio to a BytesIO object
def save_audio_to_bytes(audio, sample_rate=44100):
    audio = np.int16(audio * 32767)
    byte_io = io.BytesIO()
    write(byte_io, sample_rate, audio)
    byte_io.seek(0)
    return byte_io

# Load pre-recorded nature sounds
def load_nature_sound(sound_type):
    # Placeholder paths for pre-recorded sounds
    sound_files = {
        "Rain": "rain.wav",
        "Ocean Waves": "ocean.wav",
        "Forest Sounds": "forest.wav",
    }
    if sound_type in sound_files:
        if os.path.exists(sound_files[sound_type]):
            with open(sound_files[sound_type], "rb") as f:
                return f.read()
        else:
            st.warning(f"Pre-recorded {sound_type} file not found.")
            return None
    return None

# Streamlit App
st.title("Good Vibes Sound Generator 🌿")
st.write("Generate soothing sounds like nature, white noise, and calming frequencies.")

# Sidebar for user input
st.sidebar.header("Settings")
sound_type = st.sidebar.selectbox(
    "Choose a sound type:",
    [
        "White Noise",
        "Pink Noise",
        "Brown Noise",
        "Calming Frequency",
        "Rain",
        "Ocean Waves",
        "Forest Sounds",
    ],
)

duration = st.sidebar.slider("Duration (seconds):", 1, 36000, 600)  # Up to 10 hours

if sound_type == "Calming Frequency":
    frequency = st.sidebar.slider("Frequency (Hz):", 20, 2000, 432)
else:
    frequency = None

# Generate and play sound
if st.button("Generate Sound"):
    st.write(f"Generating {sound_type} for {duration} seconds...")

    if sound_type == "White Noise":
        audio = generate_white_noise(duration)
    elif sound_type == "Pink Noise":
        audio = generate_pink_noise(duration)
    elif sound_type == "Brown Noise":
        audio = generate_brown_noise(duration)
    elif sound_type == "Calming Frequency":
        audio = generate_sine_wave(frequency, duration)
    elif sound_type in ["Rain", "Ocean Waves", "Forest Sounds"]:
        audio_bytes = load_nature_sound(sound_type)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            st.success("Sound generated! Press the play button above to listen.")
        else:
            st.error("Failed to load nature sound.")
        st.stop()
    else:
        st.error("Invalid sound type selected.")
        st.stop()

    # Save audio to BytesIO and stream it
    audio_bytes = save_audio_to_bytes(audio)
    st.audio(audio_bytes, format="audio/wav")

    st.success("Sound generated! Press the play button above to listen.")
