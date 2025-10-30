import librosa
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
#1 uploading the audio file
audiofile = "333riff.wav"
y, sr = librosa.load(audiofile, sr= None)
#converting audio to mono chanel if it is not
if y.ndim > 1:
    y = librosa.to_mono(y)

#2 cepstral analysis, theoretical background is discussed on readme file

fourier_spectrum = np.fft.rfft(y)
log_spectrum = np.log10(np.abs(fourier_spectrum) +  1e-10)
cepstrum = np.fft.irfft(log_spectrum)

#3 finding the peaks on cepstrum
distance_as_ms = 5 #search for peaks for every 5 ms
distance_as_samples = (distance_as_ms*sr)/1000
peaks_sample, peak_properties = scipy.signal.find_peaks(
    cepstrum,
    prominence= 0.001, #minimum prominence for peaks
    distance= distance_as_samples
)
peak_prominence_values= peak_properties["prominences"]
peaks_ms = (peaks_sample*1000)/sr
#you can check the prominence values for future optimizations

#4 checking whether the peaks are periodic or not, peaks caused by delay effect expected to be periodic
min_delay_value_ms = 50 #there is a peak at the beginning in cepstrum that is not due to delay effect, we are skipping that
tolerance_ratio = 0.01 # we have 1 percent tolerance
max_tolerance_ms = 10 # but we don't want it to exceed 10 ms for higher peak_ms values
max_score= 1
delay_value= 0
candidate_peaks=[]
for p in range(1, len(peaks_ms)):
    if peak_prominence_values[p] < 0.007: #minimum prominence for delay candidates
        continue
    candidate_peaks.append(peaks_sample[p])
    peaks = peaks_ms[p]
    score = 0
    if peaks < min_delay_value_ms:
        continue
    tolerance = min(tolerance_ratio*peaks,max_tolerance_ms)
    for k in range(2,10):
        if peaks*k > 2000: #since guitar delay generally used values under 1 or 2 seconds, we are not interested with that part
            break
        found = False
        for t in peaks_ms:
            if abs(peaks*k - t) < tolerance:
                found= True
                break
        if found:
            score +=1
        else:
            break
    current_score = score
    if current_score >= max_score:
        max_score = current_score
        delay_value= int(peaks)
        print("new delay candidate=" , delay_value , "new high score" , {max_score}, "tolerance=", tolerance, "prominence =", peak_prominence_values[p])

    else:
        print("candidate is eliminated" , int(peaks), "score", current_score, "tolerance=", tolerance ,"prominence=",peak_prominence_values[p] )

print("Delay value is ", delay_value)
#plots

cepstrum_time = (np.arange(len(cepstrum))/sr)*1000
candidate_peaks_array = np.array(candidate_peaks)

plt.figure(figsize=(12, 6))
plt.plot(cepstrum_time, cepstrum, label= "cepstrum")
plt.plot(cepstrum_time[(candidate_peaks_array)],cepstrum[(candidate_peaks_array)], "x", color='gray', label="peaks",markersize=8)
plt.plot(cepstrum_time[int(delay_value*sr/1000)], cepstrum[int(delay_value*sr/1000)], "x", color= "red", label="delay value",markersize= 10)
plt.xlim(0,4000)
plt.legend()
plt.title("Cepstrum")
plt.show()







