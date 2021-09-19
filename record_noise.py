import asyncio
import logging
import os
import time
from dataclasses import dataclass

import numpy
import scipy.io.wavfile
import sounddevice
# from concurrent.futures import ThreadPoolExecutor

DUMP_DIR = "/home/pawel/noise_dump"
# EXECUTOR = ThreadPoolExecutor(max_workers=7)
AUDIO_LENGTH_SEC = 10 * 60.0
SAMPLE_RATE = 44100  # 44.1 kHz

LOGGER = logging.getLogger("measure_noise")
LOGGER.setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)


@dataclass
class Recording:
    target_file: str
    recording: numpy.ndarray

def save_recording(recording: Recording):
    LOGGER.warning(f"save_recording recording.target_file={recording.target_file} recording.recording.len={recording.recording.size}")
    scipy.io.wavfile.write(
        recording.target_file,
        SAMPLE_RATE,
        recording.recording
    )

def record_audio(seconds: float) -> Recording:
    LOGGER.warning(f"record_audio seconds={seconds}")
    recording = sounddevice.rec(int(seconds * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sounddevice.wait()
    return recording

def dump_loop():
    LOGGER.info("executing_main_loop")
    recording = None
    while True:
        timestamp = time.time_ns()
        results = asyncio.get_event_loop().run_until_complete(asyncio.gather(
            asyncio.get_event_loop().run_in_executor(
                None,
                record_audio,
                AUDIO_LENGTH_SEC,
            ),
            *(
                []
                if recording is None
                else [
                    asyncio.get_event_loop().run_in_executor(
                        None,
                        save_recording,
                        recording,
                    )
                ]
            )
        ))

        recording = Recording(
            target_file=os.path.join(DUMP_DIR, f"{timestamp}.wav"),
            recording=results[0],
        )

if __name__ == "__main__":
    LOGGER.warning(f"directory_check dir={DUMP_DIR}")
    os.makedirs(DUMP_DIR, exist_ok=True)
    dump_loop()
