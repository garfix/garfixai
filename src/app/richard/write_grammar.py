def get_write_grammar():
    return [
        {
            "syn": "s() -> 'OK'",
            "if": [('output_type', 'ok')],
        },
    ]

