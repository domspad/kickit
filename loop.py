
import glob
import os
import simpleaudio
import time

DATADIR = 'drumkit'

def base_path(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name

PLAY_SOUNDS = { base_path(f) : simpleaudio.WaveObject.from_wave_file(f) 
                    for f in glob.glob(DATADIR+'/*.wav') }

def play_sound(sound_name):
    sound = PLAY_SOUNDS[sound_name]
    sound.play()

play_sound("kick")
time.sleep(0.5)
play_sound("kick")
time.sleep(1)
