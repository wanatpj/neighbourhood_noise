import logging
import time
import os
import scipy.io.wavfile
import sounddevice
from concurrent.futures import ThreadPoolExecutor

DUMP_DIR = os.path.join(os.getenv("HOME"), "noise_dump")
EXECUTOR = ThreadPoolExecutor(max_workers=7)
AUDIO_LENGTH_SEC = 10.0
SAMPLE_RATE = 44100

LOGGER = logging.getLogger("measure_noise")
LOGGER.setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

def record_audio(file_name: str, seconds: float):
    LOGGER.warning(f"directory_check file_name={file_name}, seconds={seconds}")
    myrecording = sounddevice.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=2)
    sounddevice.wait()
    scipy.io.wavfile.write(file_name, SAMPLE_RATE, myrecording)

def dump_loop():
    LOGGER.warning("executing_main_loop")
    start_time = time.time()
    while True:
        EXECUTOR.submit(
            record_audio,
            file_name=os.path.join(DUMP_DIR, f"{time.time()}.wav"),
            seconds=AUDIO_LENGTH_SEC,
        )
        time.sleep(AUDIO_LENGTH_SEC - ((time.time() - start_time) % AUDIO_LENGTH_SEC))

if __name__ == "__main__":
    LOGGER.warning(f"directory_check dir={DUMP_DIR}")
    os.makedirs(DUMP_DIR, exist_ok=True)
    dump_loop()
