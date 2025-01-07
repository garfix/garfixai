from pygame import mixer
from music.play_sound import play_artist, play_sound, stop_play
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class MusicModule(SomeModule):
    """
    See https://www.geeksforgeeks.org/play-sound-in-python/
    """

    config: dict

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config

        mixer.init()

        self.add_relation(Relation("play_music", query_function=self.play))
        self.add_relation(Relation("stop_music", query_function=self.stop))


    def play(self, values: list, context: ExecutionContext) -> list[list]:
        artist = values[0]

        # playsound('/home/patrick/Music/A-ha/Hunting High and Low/01.Take On Me.mp3', False)
        # play_sound('/home/patrick/Music/A-ha/Hunting High and Low/01.Take On Me.mp3')
        play_artist(artist, self.config['my_music_folder'])

        return [
            [None]
        ]


    def stop(self, values: list, context: ExecutionContext) -> list[list]:
        stop_play()

        return [
            []
        ]
