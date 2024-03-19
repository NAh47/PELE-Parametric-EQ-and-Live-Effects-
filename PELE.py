import numpy as np
import pyaudio
import wave
import threading
from scipy.signal import butter, lfilter

class RealTimeAudioProcessor:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.wf = wave.open(wav_file, 'rb')
        self.sample_rate = self.wf.getframerate()
        self.num_channels = self.wf.getnchannels()
        self.audio_format = pyaudio.paInt16

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_format,
                                  channels=self.num_channels,
                                  rate=self.sample_rate,
                                  output=True,
                                  frames_per_buffer=2048) 

        # Parameters
        self.volume = 1.0
        self.bass_gain = 0.0
        self.mid_gain = 0.0
        self.treble_gain = 0.0
        self.compression_threshold = 0.5 
        self.compression_ratio = 4 
        # Compute max amplitude
        frames = self.wf.readframes(self.wf.getnframes())
        self.max_amplitude = np.max(np.abs(np.frombuffer(frames, dtype=np.int16)))
        self.wf.rewind()  # Rewind

        self.running = False

    def start(self):
        self.running = True
        audio_thread = threading.Thread(target=self.process_audio)
        audio_thread.start()

        while self.running:
            self.handle_user_input()

        audio_thread.join()

    def stop(self):
        self.running = False

    def process_audio(self):
        while self.running:
            data = self.wf.readframes(8192)
            if len(data) == 0:  
                self.stop()
                break

            audio_samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / self.max_amplitude

            processed_samples = self.apply_effects(audio_samples)

            self.stream.write((processed_samples * self.max_amplitude).astype(np.int16).tobytes())

    def apply_effects(self, audio_samples):
        audio_samples *= self.volume

        audio_samples = self.apply_eq(audio_samples)

        audio_samples = self.apply_compression(audio_samples)

        return audio_samples

    def apply_eq(self, audio_samples):
        bass_filtered = self.apply_filter(audio_samples, self.bass_gain, [100], 'low')
        mid_filtered = self.apply_filter(audio_samples, self.mid_gain, [250, 4000], 'band')
        treble_filtered = self.apply_filter(audio_samples, self.treble_gain, [4000], 'high')

        return bass_filtered + mid_filtered + treble_filtered

    def apply_filter(self, data, gain, cutoff_freq, btype='low'):
        nyq = 0.5 * self.sample_rate
        norm_cutoff = [freq / nyq for freq in cutoff_freq]
        b, a = butter(2, norm_cutoff, btype=btype)
        filtered = lfilter(b, a, data)
        return filtered * (1 + gain)

    def apply_compression(self, audio_samples):
        max_amp = np.max(np.abs(audio_samples))
        if max_amp > self.compression_threshold:
            compression_gain = 1 - 1 / self.compression_ratio
            audio_samples *= (1 - compression_gain)
        return audio_samples

    def handle_user_input(self):
        print("Current parameters:")
        print(f"Volume: {self.volume}")
        print(f"Bass gain: {self.bass_gain}")
        print(f"Mid gain: {self.mid_gain}")
        print(f"Treble gain: {self.treble_gain}")

        cmd = input("Enter command ('volume', 'bass', 'mid', 'treble', 'quit'): ").lower()
        if cmd == 'quit':
            self.stop()
        elif cmd == 'volume':
            target_volume = float(input("Enter target volume level (0.0 - 1.0): "))
            self.smooth_volume_transition(target_volume)
        elif cmd in ['bass', 'mid', 'treble']:
            self.adjust_gain(cmd)
        else:
            print("Invalid command. Try again.")

    def smooth_volume_transition(self, target_volume):
        current_volume = self.volume
        step = 0.01 if target_volume > current_volume else -0.01
        while round(current_volume, 2) != target_volume:
            current_volume += step
            self.volume = round(current_volume, 2)

    def adjust_gain(self, cmd):
        gain = float(input(f"Enter {cmd} gain (-1.0 to 1.0): "))
        if cmd == 'bass':
            self.bass_gain = gain
        elif cmd == 'mid':
            self.mid_gain = gain
        elif cmd == 'treble':
            self.treble_gain = gain

if __name__ == "__main__":
    filename = input("Enter the path to the WAV file: ")
    eq = RealTimeAudioProcessor(filename)
    eq.start()

