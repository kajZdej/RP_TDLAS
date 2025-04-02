import numpy as np

def generate_modulated_signal(lf_freq, lf_amp, hf_freq, mod_depth):
    fs = 125e6  # Red Pitaya DAC sample rate
    t = np.linspace(0, 1, int(fs))  # 1-second buffer
    
    # LF triangular wave (normalized to ±1V)
    lf_signal = lf_amp * (2 * np.abs(2 * (t * lf_freq) % 2 - 1) - 1)
    
    # HF sine modulation (10 kHz, small % of LF amplitude)
    hf_signal = 1 + mod_depth * np.sin(2 * np.pi * hf_freq * t)
    
    # Modulate and clip to avoid DAC overflow
    modulated = lf_signal * hf_signal
    return np.clip(modulated, -1, 1)