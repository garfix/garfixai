from pygame import mixer

def play_sound(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.play()


def stop_play():
    mixer.music.stop()

