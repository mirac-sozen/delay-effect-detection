# Guitar Delay Parameter Detection using Cepstrum Analysis

## Overview
This project implements **Cepstrum Analysis** to automatically detect the time parameter ($t_0$) of a delay effect applied to an electric guitar signal. By analyzing the "quefrency" domain, the algorithm separates the original signal from the echo to pinpoint the precise delay time, regardless of the guitar tone or playing style.

## Theoretical Background
Cepstrum analysis is widely used in echo detection and speech processing (e.g., pitch detection).

Mathematically, we model a signal with a single echo as:
$$y(t) = x(t) + \alpha x(t - t_0)$$

Where:
* $x(t)$ is the original signal.
* $\alpha$ is the attenuation factor of the echo (typically $< 1$).
* $t_0$ is the delay time.

Taking the **Fourier Transform** of this equation:
$$Y(j\omega) = X(j\omega) + \alpha X(j\omega)e^{-j\omega t_0} = X(j\omega)(1 + \alpha e^{-j\omega t_0})$$

The **Power Cepstrum** is obtained by taking the squared magnitude, the logarithm, and then the Inverse Fourier Transform (or Inverse DFT). The logarithm turns the multiplication into addition:
$$\log|Y(j\omega)| = \log|X(j\omega)| + \log|1 + \alpha e^{-j\omega t_0}|$$

When the inverse transform is taken to move into the **Quefrency domain**, the term $\log(1 + \alpha e^{-j\omega t_0})$ manifests as a periodic ripple. This results in a series of sharp peaks (spikes) in the cepstrum occurring at indices corresponding to $t_0, 2t_0, 3t_0, \dots$.

## Algorithm & Parameters

To ensure robustness against noise and false positives, the algorithm utilizes a multi-stage filtering process:

### 1. Adaptive Prominence Filtering
We utilize a **two-pass prominence strategy**:
* **Initial Extraction (High Sensitivity):** The prominence parameter is kept intentionally low to extract a wide range of peaks. This is crucial because while the fundamental delay peak ($t_0$) usually has high prominence, its harmonics ($2t_0, 3t_0$) often decay in strength. We need to capture these weaker harmonics to verify periodicity.
* **Scoring Filter (High Specificity):** Before calculating the final score, a second filter is applied (e.g., `peak_prominence > 0.007`). This ensures that we only consider peaks "strong" enough to be potential candidates for the fundamental delay, while still having the history of the smaller peaks for verification.

### 2. Time Window Constraints
* **Minimum Delay (50ms):** The analysis ignores the first 50ms of the cepstrum. This acts as a high-pass lifter to remove the DC component and low-quefrency features inherent to the source signal (the "1" in the logarithmic term).
* **Maximum Delay (2000ms):** Harmonics and peaks beyond 2 seconds are ignored, as this falls outside the standard usage range for guitar delay effects.

### 3. Periodicity Check
A raw cepstrum often contains spurious peaks caused by the guitar's harmonic content. To isolate the true delay time, the algorithm checks for **periodicity**. It looks for a sequence of peaks spaced evenly ($t_0, 2t_0, \dots$) to confirm the fundamental delay time rather than relying on the single highest magnitude peak.

## Testing & Results
The algorithm has been tested against various recordings featuring:
* Different guitar tones (clean, overdrive).
* Various playing styles (strumming, picking).
* Different delay time settings.

The implementation successfully detected the delay parameter in all test cases.

> **Note:** Test recordings can be found in the `audio_files` branch of this 

