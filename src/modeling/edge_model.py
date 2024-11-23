import numpy as np

def unidirectional_wave(frequency, amplitude, time_period):
    """Generate a unidirectional wave function."""
    time = np.linspace(0, time_period, 100)
    wave = amplitude * np.sin(2 * np.pi * frequency * time)
    return time, wave

def merged_wave(wave_A, wave_B):
    """Merge two waves to represent a bi-directional relationship."""
    return [a + b for a, b in zip(wave_A, wave_B)]

def edge_intensity(frequency, amplitude):
    """Compute intensity for unidirectional edges."""
    return frequency * amplitude  # Direct interaction of granularity

def merged_intensity(freq_a_b, amp_a_b, freq_b_a, amp_b_a):
    """Compute merged intensity for bi-directional edges."""
    return (freq_a_b * amp_a_b + freq_b_a * amp_b_a)  # Sum granular contributions
