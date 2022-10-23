from pydub import AudioSegment
from pydub.playback import play


sound = AudioSegment.from_ogg("/app/audios/new_file.ogg")
play(sound)
#play(sound.set_frame_rate(4000))

#play(sound.set_sample_width(1))
#play(sound + 10)


played_togther = sound.overlay(sound-5,position=100).overlay(sound-10,position=200).overlay(sound-15,position=300)
played_togther2 = sound.overlay(sound,position=100).overlay(sound,position=200).overlay(sound,position=300)

play(played_togther2)
play(played_togther)

# Manually override the frame_rate. This tells the computer how many
# samples to play per second
speed=1.5
sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
play(sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate))

#play(sound.reverse())