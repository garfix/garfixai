import os
import random
import re
import pygame


def sound_init():
    pygame.init()
    pygame.mixer.init()


def play_sound(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def stop_play():
    pygame.mixer.music.stop()


def play_artist(artist: str, music_folder: str):
    """
    Presumes this directory schema:
        music_folder
            artist_name
                album_name
                    song_name
    """

    pygame.mixer.music.stop()

    path = os.path.expanduser(music_folder)
    artists = os.listdir(path)
    artist_found = False
    for an_artist in artists:
        if simplify_name(an_artist) == simplify_name(artist):
            artist_found = True
            artist = an_artist
            break

    if not artist_found:
        print("Artist not found: " + artist)
        return

    path = f"{path}/{artist}"

    albums = os.listdir(path)
    if len(albums) == 0:
        print(artist + " has no albums")
        return

    album = random.choice(albums)
    path = f"{path}/{album}"

    songs = os.listdir(path)
    if len(songs) == 0:
        print(album + " has no songs")
        return

    song = random.choice(songs)
    path = f"{path}/{song}"
    play_sound(path)

    print(f"Playing {song} from the album {album} by {artist}")


def simplify_name(name) -> str:
    return re.sub('[._\- ]+', '', name.lower())
