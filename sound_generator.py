import streamlit as st
import numpy as np
from scipy.io.wavfile import write
import io
from pydub import AudioSegment

# Function to generate white noise
def generate_white_noise(duration, sample_rate=44100):
    noise = np.random.uniform(-1, 1, int(sample_rate * duration))
    return noise

# Function to generate pink noise
def generate_pink_noise(duration, sample_rate=44100):
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

# Function to simulate rain sounds
def simulate_rain(duration, sample_rate=44100):
    white_noise = generate_white_noise(duration, sample_rate)
    brown_noise = generate_brown_noise(duration, sample_rate)
    rain = 0.7 * white_noise + 0.3 * brown_noise
    return rain / np.max(np.abs(rain))  # Normalize

# Function to simulate ocean waves
def simulate_ocean_waves(duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_frequency = 0.1  # Slow wave frequency
    sine_wave = 0.5 * np.sin(2 * np.pi * wave_frequency * t)
    pink_noise = generate_pink_noise(duration, sample_rate)
    ocean = 0.6 * sine_wave + 0.4 * pink_noise
    return ocean / np.max(np.abs(ocean))  # Normalize

# Function to simulate forest sounds
def simulate_forest(duration, sample_rate=44100):
    white_noise = generate_white_noise(duration, sample_rate)
    chirp_frequency = 2000  # Frequency of bird chirps
    chirp_duration = 0.1  # Duration of each chirp
    chirp_samples = int(chirp_duration * sample_rate)
    t_chirp = np.linspace(0, chirp_duration, chirp_samples, endpoint=False)
    chirp = 0.5 * np.sin(2 * np.pi * chirp_frequency * t_chirp)
    chirp_envelope = np.exp(-5 * t_chirp)  # Fade out the chirp
    chirp = chirp * chirp_envelope

    # Add chirps at random intervals
    for _ in range(int(duration / 2)):  # Add a chirp every 2 seconds on average
        start = np.random.randint(0, len(white_noise) - chirp_samples)
        white_noise[start : start + chirp_samples] += chirp

    forest = white_noise / np.max(np.abs(white_noise))  # Normalize
    return forest

# Function to simulate piano sounds (simple sine wave approximation)
def simulate_piano(duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequencies = [261.63, 329.63, 392.00]  # C4, E4, G4 (C major chord)
    piano_wave = np.zeros_like(t)
    for freq in frequencies:
        piano_wave += 0.2 * np.sin(2 * np.pi * freq * t)
    return piano_wave / np.max(np.abs(piano_wave))  # Normalize

# Function to simulate guitar sounds (simple sine wave approximation)
def simulate_guitar(duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequencies = [82.41, 110.00, 146.83]  # E2, A2, D3 (open strings)
    guitar_wave = np.zeros_like(t)
    for freq in frequencies:
        guitar_wave += 0.2 * np.sin(2 * np.pi * freq * t)
    return guitar_wave / np.max(np.abs(guitar_wave))  # Normalize

# Function to simulate flute sounds (simple sine wave approximation)
def simulate_flute(duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequency = 440.00  # A4 note
    flute_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return flute_wave / np.max(np.abs(flute_wave))  # Normalize

# Function to simulate singing bowls (simple sine wave approximation)
def simulate_singing_bowls(duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    frequency = 392.00  # G4 note
    singing_bowl_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    envelope = np.exp(-0.5 * t)  # Slow fade
    singing_bowl_wave = singing_bowl_wave * envelope
    return singing_bowl_wave / np.max(np.abs(singing_bowl_wave))  # Normalize

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
st.write("Generate soothing sounds like nature, white noise, and calming frequencies.")

# Sidebar for user input
st.sidebar.header("Settings")
sound_category = st.sidebar.selectbox(
    "Choose a sound category:",
    ["Nature Sounds", "Noise Colors", "Calming Frequencies", "Ambient Music"],
)

if sound_category == "Nature Sounds":
    sound_type = st.sidebar.selectbox(
        "Choose a sound type:",
        ["Rain", "Ocean Waves", "Forest"],
    )
elif sound_category == "Noise Colors":
    sound_type = st.sidebar.selectbox(
        "Choose a sound type:",
        ["White Noise", "Pink Noise", "Brown Noise"],
    )
elif sound_category == "Calming Frequencies":
    sound_type = st.sidebar.selectbox(
        "Choose a sound type:",
        ["432 Hz", "528 Hz"],
    )
elif sound_category == "Ambient Music":
    sound_type = st.sidebar.selectbox(
        "Choose a sound type:",
        ["Piano", "Guitar", "Flute", "Singing Bowls"],
    )

duration = st.sidebar.slider("Duration (seconds):", 1, 36000, 600)  # Up to 10 hours

# Generate and play sound
if st.button("Generate Sound"):
    st.write(f"Generating {sound_type} for {duration} seconds...")

    if sound_type == "White Noise":
        audio = generate_white_noise(duration)
    elif sound_type == "Pink Noise":
        audio = generate_pink_noise(duration)
    elif sound_type == "Brown Noise":
        audio = generate_brown_noise(duration)
    elif sound_type == "432 Hz":
        audio = generate_sine_wave(432, duration)
    elif sound_type == "528 Hz":
        audio = generate_sine_wave(528, duration)
    elif sound_type == "Rain":
        audio = simulate_rain(duration)
    elif sound_type == "Ocean Waves":
        audio = simulate_ocean_waves(duration)
    elif sound_type == "Forest":
        audio = simulate_forest(duration)
    elif sound_type == "Piano":
        audio = simulate_piano(duration)
    elif sound_type == "Guitar":
        audio = simulate_guitar(duration)
    elif sound_type == "Flute":
        audio = simulate_flute(duration)
    elif sound_type == "Singing Bowls":
        audio = simulate_singing_bowls(duration)
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
