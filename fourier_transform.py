from scipy.fft import rfft, rfftfreq , irfft
import numpy as np

def fourier(data ,gain) :
    signal = np.array(10 * [None])
    new_magnitudes = []
    data = np.array(data)
    ft = rfft(data)
    Magnitudes = np.abs(ft)
    k, m = divmod(len(Magnitudes), 10)
    for i in range(10):
            signal[i] = Magnitudes[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
            signal[i] = signal[i] * gain[i]
            new_magnitudes = new_magnitudes + list(signal[i])
    new_magnitudes = np.array(new_magnitudes)
    modified= np.multiply(new_magnitudes, np.exp(1j*np.angle(ft)))    
    output_signal = irfft(modified)
    return output_signal , Magnitudes


def spectro_range(data , min , max):
        ft = rfft(data)
        begin_index = int((len(ft)) * min) 
        end_index = int((len(ft)) * max) 
        ft[0:begin_index] = 0
        ft[end_index:len(ft)] = 0
        output_signal = irfft(ft)
        return output_signal


