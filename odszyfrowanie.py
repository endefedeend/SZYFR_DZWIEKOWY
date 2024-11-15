import numpy as np
from scipy.io import wavfile
from scipy.fft import fft

# Częstotliwości odpowiadające literom A-Z
frequencies = {
    'A': 440, 'B': 466, 'C': 494, 'D': 523, 'E': 554, 'F': 587, 'G': 622, 'H': 659, 'I': 698, 'J': 740,
    'K': 784, 'L': 830, 'M': 880, 'N': 932, 'O': 988, 'P': 1047, 'Q': 1109, 'R': 1175, 'S': 1245, 'T': 1319,
    'U': 1397, 'V': 1480, 'W': 1568, 'X': 1661, 'Y': 1760, 'Z': 1865
}

# Tworzenie odwrotnej mapy częstotliwości do liter
frequencies_to_letters = {v: k for k, v in frequencies.items()}

# Parametry
duration = 0.5  # Czas trwania każdej litery w sekundach
threshold = 100  # Próg amplitudy, aby uznać dominującą częstotliwość

def find_closest_frequency(frequency, frequencies_list):
    return min(frequencies_list, key=lambda x: abs(x - frequency))

def process_segment(segment, sample_rate):
    # Transformacja Fouriera
    spectrum = fft(segment)
    freqs = np.fft.fftfreq(len(spectrum), 1 / sample_rate)

    # Przefiltrowanie tylko dodatnich częstotliwości
    positive_freqs = freqs[:len(freqs) // 2]
    positive_spectrum = np.abs(spectrum[:len(spectrum) // 2])

    # Znalezienie dominującej częstotliwości
    idx = np.argmax(positive_spectrum)
    dominant_freq = abs(positive_freqs[idx])

    return dominant_freq

def wav_to_text(filename):
    sample_rate, data = wavfile.read(filename)

    # Jeżeli dźwięk jest stereo, konwertujemy na mono
    if len(data.shape) == 2:
        data = np.mean(data, axis=1)

    num_samples_per_letter = int(sample_rate * duration)
    decoded_text = ""

    for i in range(0, len(data), num_samples_per_letter):
        segment = data[i:i + num_samples_per_letter]

        if len(segment) == 0:
            break

        # Sprawdzenie, czy segment to cisza (bardzo mała amplituda)
        if np.max(np.abs(segment)) < threshold:
            decoded_text += " "
            continue

        dominant_freq = process_segment(segment, sample_rate)
        closest_freq = find_closest_frequency(dominant_freq, list(frequencies.values()))
        decoded_text += frequencies_to_letters[closest_freq]

    return decoded_text

# Przykład użycia
decoded_key = wav_to_text("public_message.wav")
print(f"Odczytano klucz: {decoded_key}")
