from richard.core.constants import E1, E2, E3, e1, e2, e3


def get_music_grammar():
    return [
        {
            "syn": "s() -> command()",
            "sem": lambda command: command,
        },
        {
            "syn": "command() -> 'play' 'some' artist()",
            "sem": lambda artist: [('intent_play_music', artist)],
        },
        {
            "syn": "command() -> 'stop'",
            "sem": lambda: [('intent_stop_music',)],
        },
        {
            "syn": "artist() -> /[\w]+([ -.][\w]+)*[.]?/",
            "sem": lambda artist: artist,
        },
    ]
