# delay-effect-detection
This project is an implementation of Cepstrum Analysis in order to detect the time parameter of a delay effect on electric guitar.

THEORETICAL BACKGROUND
This analysis generally used in echo detecting algorithms
In our case we assume delayed function as x(t) + ax(t- t0), its fourier transform will be X(JW) + aX(JW)exp(-jwt0) which simplifies to X(JW)(1 + a.exp(-jwt0))
Cepstral analysis seperates the term (1 + a.exp(jwt0)) with taking the logarithm of the magnitude, when its inverse fourier transform is taken, this periodic ripple manifests as a series of sharp peaks (spikes) in the cepstrum at t0, 2t0, 3t0 ... 

PARAMETERS
Prominence parameter is kept low when extracting the peaks initially. Because even though the first delay peak has high prominence, its harmonics have low prominences, since we need those harmonics while considering the periodicty, we should capture them. 

Minimum Delay: Delay is checked after 50 ms since 1 on the term  (1 + a.exp(-jwt0)) gives rise to the cepstrum in the beginning (consider 1 as exp(jw0))
Maximum Delay: Harmonics after 2000ms (2 seconds) are ignored, as this time parameter is outside the range of typical guitar delay usage.

PERIODICITY CHECK
We encountered many false peaks in our cepstrum, in order to seperate the fundemental delay parameter, we checked the periodicity. However, we also apply a second prominence filter (if peak_prominence_values[p] < 0.007: continue) before scoring. This allows us to use a very low initial prominence to catch all harmonics, but ensures we only start scoring peaks that are "strong" enough to be a potential fundamental delay.

TEST
I made different records with different tones, playing styles and delay parameter, and the algorithm was succeed in all of these. You can find my records in audio_files branch.

You can test with your own recordings and send a feedback to me

