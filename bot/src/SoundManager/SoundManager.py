import os
from pydub import AudioSegment
from pydub.playback import play

def open_sound(s):
    try:
        sound = AudioSegment.from_ogg(s)
        return sound
    except:
        sound = AudioSegment.from_mp3(s)
        return sound


def reverse_sound(s):
    sound = open_sound(s)
    reverse = sound.reverse()
    return reverse.export(s, format="ogg", codec="libopus")


def reverberation_sound(s):
    sound = open_sound(s)
    reverberation = sound.overlay(sound-5,position=100).overlay(sound-10,position=200).overlay(sound-15,position=300)
    return reverberation.export(s, format="ogg",codec="libopus")


def distorsio_sound(s):
    sound = open_sound(s)
    return distorsio.export(s, format="ogg", codec="libopus")