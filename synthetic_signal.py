import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq , irfft
SAMPLE_RATE = 40000  # Hertz
DURATION = 5  # Seconds
signal = np.array(10 * [None])
gain = np.array(10 * [2])
synthetic_signals = np.array(10 * [None])
tone = 0
def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y
for i in range(10):
    x, synthetic_signals[i] =  generate_sine_wave(((2000/2)+i*2000), SAMPLE_RATE, DURATION)
    tone += synthetic_signals[i]
plt.plot(x , tone)
plt.show()
write("synthetic_tone.wav", SAMPLE_RATE, tone)
# N = SAMPLE_RATE * DURATION

# yf = rfft(tone)
# xf = rfftfreq(N, 1 / SAMPLE_RATE)

# plt.plot(xf, np.abs(yf))
# plt.show()
