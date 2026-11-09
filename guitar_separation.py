import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt, spectrogram
import os


output_folder = "output_results"
os.makedirs(output_folder, exist_ok=True)


fs = 22050
duration = 3.0
t = np.linspace(0, duration, int(fs * duration), endpoint=False)


def make_instrument(freqs, amps, decay=0.4, harm=5):
    sig = np.zeros_like(t)
    for f, a in zip(freqs, amps):
        for h in range(1, harm + 1):
            sig += (a / (h ** decay)) * np.sin(2 * np.pi * f * h * t)
    envelope = np.exp(-0.4 * t)
    return sig * envelope


guitar = make_instrument(
    freqs=[110, 146.8, 196, 246.9],
    amps=[0.9, 0.75, 0.6, 0.5],
    decay=0.45, harm=6
)


piano = make_instrument(
    freqs=[261.6, 329.6, 392, 523.3],
    amps=[0.7, 0.55, 0.4, 0.3],
    decay=0.55, harm=4
)

violin = make_instrument(
    freqs=[440, 554.4, 659.3],
    amps=[0.6, 0.45, 0.35],
    decay=0.6, harm=5
)

mixed = guitar + 0.8 * piano + 0.7 * violin
mixed = mixed / np.max(np.abs(mixed)) * 0.9


def bandpass(data, low, high, fs, order=5):
    nyq = 0.5 * fs
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, data)


separated = bandpass(mixed, 80, 1100, fs)
separated = separated / np.max(np.abs(separated)) * 0.9


def save_wav(name, signal):
    signal = signal / np.max(np.abs(signal)) * 0.95
    wavfile.write(os.path.join(output_folder, name), fs, (signal * 32767).astype(np.int16))

save_wav("01_guitar_original.wav", guitar)
save_wav("02_piano.wav", piano)
save_wav("03_violin.wav", violin)
save_wav("04_mixed.wav", mixed)
save_wav("05_guitar_separated.wav", separated)


corr = np.corrcoef(guitar, separated)[0, 1]
mse = np.mean((guitar - separated)**2)

print(f"\nGuitar Separation Evaluation Results:")
print(f"Correlation : {corr:.4f}")
print(f"MSE         : {mse:.6e}")


fig, ax = plt.subplots(3, 2, figsize=(14, 10))


ax[0, 0].plot(t, mixed, color='purple', linewidth=0.8)
ax[0, 0].set_title("Mixed Signal (All Instruments)")
ax[0, 0].set_xlabel("Time (s)")
ax[0, 0].grid(True, alpha=0.3)


f = np.fft.rfftfreq(len(mixed), 1/fs)
X = 20 * np.log10(np.abs(np.fft.rfft(mixed * np.hanning(len(mixed)))) + 1e-12)
ax[0, 1].plot(f, X - X.max())
ax[0, 1].set_xlim(0, 2000)
ax[0, 1].set_title("Spectrum of Mixed Signal")
ax[0, 1].set_xlabel("Frequency (Hz)")
ax[0, 1].grid(True, alpha=0.3)


ax[1, 0].plot(t, guitar, label="Original Guitar", alpha=0.8)
ax[1, 0].plot(t, separated, label="Separated Guitar", alpha=0.7)
ax[1, 0].set_title("Guitar: Original vs Separated")
ax[1, 0].set_xlabel("Time (s)")
ax[1, 0].legend()
ax[1, 0].grid(True, alpha=0.3)


ax[1, 1].text(0.1, 0.6, f"Correlation: {corr:.4f}\n\nMSE: {mse:.6e}",
              transform=ax[1, 1].transAxes, fontsize=14)
ax[1, 1].set_title("Separation Evaluation")
ax[1, 1].axis("off")


f_s, t_s, Sxx = spectrogram(mixed, fs, nperseg=512)
ax[2, 0].pcolormesh(t_s, f_s, 10*np.log10(Sxx+1e-12), shading='gouraud', cmap='magma')
ax[2, 0].set_ylim(0, 2000)
ax[2, 0].set_title("Spectrogram - Mixed")
ax[2, 0].set_ylabel("Frequency (Hz)")

f_s, t_s, Sxx = spectrogram(separated, fs, nperseg=512)
ax[2, 1].pcolormesh(t_s, f_s, 10*np.log10(Sxx+1e-12), shading='gouraud', cmap='magma')
ax[2, 1].set_ylim(0, 2000)
ax[2, 1].set_title("Spectrogram - Separated Guitar")

plt.tight_layout()
plt.savefig(os.path.join(output_folder, "results.png"), dpi=150)
plt.show()

print("\n Result in → results.png")
print("The End.")