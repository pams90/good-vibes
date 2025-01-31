import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import io

# Function to generate white noise
def generate_white_noise(duration, sample_rate=44100):
    noise = np.random.uniform(-1, 1, int(sample_rate * duration))
    return noise

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

# Streamlit App
st.title("Good Vibes Sound Generator 🌿")
st.write("Generate soothing sounds like white noise and calming frequencies.")

# Sidebar for user input
st.sidebar.header("Settings")
sound_type = st.sidebar.selectbox(
    "Choose a sound type:",
    ["White Noise", "Calming Frequency"]
)

duration = st.sidebar.slider("Duration (seconds):", 1, 60, 10)

if sound_type == "Calming Frequency":
    frequency = st.sidebar.slider("Frequency (Hz):", 20, 2000, 440)
else:
    frequency = None

# Generate and play sound
if st.button("Generate Sound"):
    st.write(f"Generating {sound_type} for {duration} seconds...")

    if sound_type == "White Noise":
        audio = generate_white_noise(duration)
    elif sound_type == "Calming Frequency":
        audio = generate_sine_wave(frequency, duration)

    # Save audio to BytesIO and stream it
    audio_bytes = save_audio_to_bytes(audio)
    st.audio(audio_bytes, format="audio/wav")

    st.success("Sound generated! Press the play button above to listen.")
