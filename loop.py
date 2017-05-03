import asyncio
import functools
import glob
import os
import simpleaudio
import time

DATADIR = 'drumkit'

BPM = 200 
TIME_BETWEEN = 60 / BPM

def base_path(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name

PLAY_SOUNDS = { base_path(f) : simpleaudio.WaveObject.from_wave_file(f) 
                    for f in glob.glob(DATADIR+'/*.wav') }

def play_sound(sound_name):
    sound = PLAY_SOUNDS[sound_name]
    sound.play()


DRUM_PATTERN = {
        'hhat': [0, 1, 0, 1, 0, 1, 0, 1],
        'kick': [1, 0, 1, 0, 1, 1, 1, 1],
        }
BEATS_IN_PATTERN = 8

def read_pattern_and_schedule(loop):
    for sound, pattern in DRUM_PATTERN.items():
        for idx, has_beat in enumerate(pattern):
            if has_beat:
                loop.call_later(TIME_BETWEEN * idx, functools.partial(play_sound, sound))
    loop.call_later(TIME_BETWEEN * BEATS_IN_PATTERN, read_pattern_and_schedule, loop)

loop = asyncio.get_event_loop()
loop.call_soon(read_pattern_and_schedule, loop)
loop.run_forever()

