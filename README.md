# Guitar Sound Separation Using Python

## Overview

This project demonstrates a basic approach to extracting a guitar-like signal from a mixture of three synthetic instruments: guitar, piano, and violin.

The audio signals are generated in Python, combined into one track, and passed through a Butterworth band-pass filter. The script then compares the filtered output with the original guitar signal and creates plots to help visualize the process.

## Results

The script saves a visualization of the experiment as `output_results/results.png`.

![Guitar separation results](output_results/results.png)

**Where to add the image:** Run `guitar_separation.py` first. It will create the `output_results` folder and save `results.png` inside it. Commit that image to GitHub at the same relative path shown above. Once the image is in your repository, GitHub will display it here automatically.

## Features

- Generate synthetic guitar, piano, and violin signals.
- Mix the three signals into a single audio track.
- Apply a Butterworth band-pass filter to the mixed signal.
- Save the individual, mixed, and filtered signals as WAV files.
- Evaluate the filtered signal using correlation and Mean Squared Error (MSE).
- Plot the waveforms, frequency spectrum, and spectrograms.

## Requirements

- Python 3
- NumPy
- SciPy
- Matplotlib

Install the required packages with:

```bash
pip install numpy scipy matplotlib
```

## Getting Started

Clone the repository:

```bash
git clone https://github.com/ma-bgh/Guitar-Sound-Separation.git
```

Move into the project directory:

```bash
cd Guitar-Sound-Separation
```

Run the script:

```bash
python guitar_separation.py
```

The script creates an `output_results` folder automatically. It saves the generated WAV files and the visualization there.

## How It Works

### 1. Signal Generation

The script creates synthetic signals for guitar, piano, and violin. Each signal is built from fundamental frequencies and harmonics, with an exponential amplitude envelope.

### 2. Mixing

The three instrument signals are combined using different volume weights. The resulting mixture is normalized before filtering.

### 3. Band-Pass Filtering

A Butterworth band-pass filter is applied to the mixed signal, with cutoff frequencies of 80 Hz and 1100 Hz. The filtered signal is treated as the estimated guitar output.

### 4. Evaluation

The estimated guitar signal is compared with the original synthetic guitar signal using:

- **Correlation coefficient:** indicates how closely the two signals vary together.
- **Mean Squared Error (MSE):** measures the average squared difference between the two signals.

### 5. Visualization

The generated figure includes the mixed waveform, its frequency spectrum, a comparison of the original and filtered guitar signals, the evaluation metrics, and spectrograms of the mixed and filtered signals.

## Output Files

After running the script, the `output_results` folder contains:

| File | Description |
|---|---|
| `01_guitar_original.wav` | Original synthetic guitar signal |
| `02_piano.wav` | Synthetic piano signal |
| `03_violin.wav` | Synthetic violin signal |
| `04_mixed.wav` | Mixture of all three instruments |
| `05_guitar_separated.wav` | Filtered output |
| `results.png` | Visualization of the signals and evaluation |

## Notes and Limitations

This is a small educational experiment in digital signal processing, not a complete music source-separation system. A band-pass filter selects a frequency range; it does not identify which instrument produced each frequency. Since the instruments' frequency ranges can overlap, piano and violin components may remain in the filtered output.

The instrument sounds in this project are synthesized from sine waves and harmonics rather than taken from real recordings. The results should therefore be understood as a demonstration of filtering, not as evidence of reliable separation on real-world music.

## License

No license has been specified for this project yet.
