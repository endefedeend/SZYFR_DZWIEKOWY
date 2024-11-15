import numpy as np
from scipy.io.wavfile import write

# Częstotliwości odpowiadające literom
frequencies = {
    'A': 440, 'B': 466, 'C': 494, 'D': 523, 'E': 554, 'F': 587, 'G': 622, 'H': 659, 'I': 698, 'J': 740,
    'K': 784, 'L': 830, 'M': 880, 'N': 932, 'O': 988, 'P': 1047, 'Q': 1109, 'R': 1175, 'S': 1245, 'T': 1319,
    'U': 1397, 'V': 1480, 'W': 1568, 'X': 1661, 'Y': 1760, 'Z': 1865
}

# Parametry dźwięku
sample_rate = 44100
duration = 0.5

def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def generate_silence(duration, sample_rate):
    return np.zeros(int(sample_rate * duration))

def text_to_wav(text, filename):
    text = text.upper()
    audio_data_list = []

    for char in text:
        if char in frequencies:
            tone = generate_sine_wave(frequencies[char], duration, sample_rate)
            audio_data_list.append(tone)
        elif char == ' ':
            silence = generate_silence(duration, sample_rate)
            audio_data_list.append(silence)

    audio_data = np.concatenate(audio_data_list)
    audio_data = np.int16(audio_data * 32767)
    write(filename, sample_rate, audio_data)

secret_key = input("Podaj klucz tajny (tekstowy): ")
text_to_wav(secret_key, "public_message.wav")
print("Utworzono Plik WAV jako 'public_message.wav'.")
