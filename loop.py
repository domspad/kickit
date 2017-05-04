import asyncio
import functools
import glob
import os
import simpleaudio


DATADIR = 'drumkit'

BPM = 120
BEAT_RESOLUTION = 4
TIME_BETWEEN = 60 / BPM / BEAT_RESOLUTION


def base_path(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name


PLAY_SOUNDS = {
    base_path(f): simpleaudio.WaveObject.from_wave_file(f)
    for f in glob.glob(DATADIR+'/*.wav')
}


def play_sound(sound_name):
    sound = PLAY_SOUNDS[sound_name]
    sound.play()


DRUM_PATTERN = {
        'hhat': [
            0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0,
            0, 0, 1, 0,
            ],
        'snare': [
            0, 0, 0, 0,
            1, 0, 0, 0,
            0, 0, 0, 0,
            1, 0, 0, 0,
            ],
        'kick': [
            1, 0, 0, 0,
            0, 0, 1, 0,
            1, 0, 0, 0,
            0, 0, 0, 0,
            ],
        }
BEATS_IN_PATTERN = len(DRUM_PATTERN['kick'])


def update_pattern(new_drum_pattern):
    DRUM_PATTERN.update(new_drum_pattern)


def read_pattern_and_schedule(loop):
    for sound, pattern in DRUM_PATTERN.items():
        for idx, has_beat in enumerate(pattern):
            if has_beat:
                loop.call_later(TIME_BETWEEN * idx, functools.partial(play_sound, sound))
    loop.call_later(TIME_BETWEEN * (BEATS_IN_PATTERN), read_pattern_and_schedule, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_soon(read_pattern_and_schedule, loop)
    loop.run_forever()
