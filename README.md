# micsens

Microphone-based vibration sensing using Arduino and Python.  
This project logs raw microphone sensor data and derives threshold-based
binary events on the Python side for behavioral analysis (e.g., rat water drinking detection).

---

## Quick Start

### Hardware Setup
1. Prepare an Arduino board.
2. Connect a microphone sensor module  
   (example: https://amzn.to/48TqD1U).
3. Adjust the sensitivity using the onboard trimmer (see notes below).

### Arduino
1. Open `micsens.ino` with Arduino IDE  
   https://www.arduino.cc/en/software
2. Upload the sketch to the Arduino.

The Arduino continuously sends **raw sensor values only** via serial
(no timestamps).

### Python
1. Install dependencies:
   ```bash
   pip install pyserial

2. run
 python micsens_logger.py

# A CSV file will be created in the logs/ directory.

Stopping the Program

Press Ctrl + C to safely stop logging.
The serial port will be closed and the CSV file will be finalized.

### CSV Output

Each row is logged at a fixed sampling rate and contains:
	•	time_ms – elapsed time since Python start (milliseconds)
	•	raw – raw microphone sensor value
	•	over_value – sensor value only when above threshold, otherwise 0
	•	over_flag – binary flag (1 = above threshold interval, 0 = otherwise)

### Sensor Sensitivity Adjustment

The microphone board includes a small trimmer screw:
	•	Turn clockwise → decrease sensitivity
	•	Turn counter-clockwise → increase sensitivity

## Important:
The sensor is highly sensitive. If set too high, it may respond to
human voices or distant environmental sounds.
Sensitivity tuning is very sharp and should be adjusted carefully
while monitoring raw values.
