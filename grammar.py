from richard.core.constants import E1, E2, E3, e1, e2, e3


def get_grammar():
    return [
        {
            "syn": "s() -> command()",
            "sem": lambda command: command,
            "dialog": [("format", "canned"), ("format_canned", "OK")],
        },
        {
            "syn": "command() -> 'play' 'some' artist()",
            "sem": lambda artist: [('play', artist)],
        },
        {
            "syn": "artist() -> /[\w]+(-[\w]+)*/",
            "sem": lambda artist: artist,
        },
    ]
