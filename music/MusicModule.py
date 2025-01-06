from music.play_sound import playsound
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class MusicModule(SomeModule):
    """
    See https://www.geeksforgeeks.org/play-sound-in-python/
    """

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("play", query_function=self.play))


    def play(self, values: list, context: ExecutionContext) -> list[list]:
        artist = values[0]

        playsound('/home/patrick/Music/A-ha/Hunting High and Low/01.Take On Me.mp3')

        return [
            [None]
        ]
