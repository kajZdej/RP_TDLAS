import numpy as np

def generate_signal(shape, freq, amp, length=1, fs=125e6):
    t = np.linspace(0, length, int(fs * length))
    if shape == "triangular":
        signal = amp * (2 * np.abs(2 * (t * freq) % 2 - 1) - 1)
    elif shape == "sine":
        signal = amp * np.sin(2 * np.pi * freq * t)
    elif shape == "square":
        signal = amp * np.sign(np.sin(2 * np.pi * freq * t))
    return signal

def generate_modulated_signal(lf_shape, lf_freq, lf_amp, hf_freq, mod_depth):
    fs = 125e6
    lf_signal = generate_signal(lf_shape, lf_freq, lf_amp)
    hf_signal = 1 + mod_depth * np.sin(2 * np.pi * hf_freq * np.arange(len(lf_signal)) / fs)
    return np.clip(lf_signal * hf_signal, -1, 1)