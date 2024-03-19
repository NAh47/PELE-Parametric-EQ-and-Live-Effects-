# Pele: Parametric EQ

**Description:**
Pele is a Python project designed for real-time audio processing, offering parametric equalization (EQ) for WAV files. Users can adjust volume, bass, mid, and treble parameters during playback, enhancing the listening experience.

**Building and Running the Project:**
1. Ensure Python is installed along with the required dependencies: NumPy, PyAudio, and SciPy.
2. Download or clone the Pele project repository.
3. Navigate to the project directory in your terminal or command prompt.
4. Run the Python script `pele.py`.
5. When prompted, enter the path to the WAV file you want to process.

**Testing:**
- Unit tests verify the correctness of individual components.
- Integration tests validate interactions between modules.

**Example:**
1. Run `pele.py`.
2. Enter the path or name of the WAV file.
3. Select an option from the EQ menu (volume, bass, mid, treble).
4. Enter the desired value for the selected option.
5. Pele applies the specified EQ settings in real-time.

**Feedback and Future Improvements:**
While the project implements parametric EQ, playback quality remains a challenge. Future improvements may optimize buffer sizes, refine processing algorithms, employe advanced audio filtering and processing methdologis(in order to mitgate the current issues), as well as conduct further testing for optimal performance.

**Audio source**
https://uppbeat.io/browse/music/majestic-beats 
Title: Breaking Ideas