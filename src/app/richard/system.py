import os
import pathlib
from richard.block.TryFirst import TryFirst
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.core.BasicGenerator import BasicGenerator
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.System import System
from richard.processor.parser.BasicParser import BasicParser
from richard.module.InferenceModule import InferenceModule
from app.richard.module.music.MusicModule import MusicModule
from app.richard.write_grammar import get_write_grammar
from app.richard.module.music.read_grammar import get_music_grammar


def create_system():

    path = str(pathlib.Path(__file__).parent.resolve()) + "/"

    # define the intents

    inferences = InferenceModule()
    inferences.import_rules(path + "module/music/intents.pl")

    # a data source for facts that only last a sentence

    sentence_context = BasicSentenceContext()

    # define the model

    music_module = MusicModule(os.getenv('MY_MUSIC_FOLDER'))

    model = Model([
        sentence_context,
        music_module,
        inferences
    ])

    # define the pipeline

    grammar = []
    grammar.extend(get_music_grammar())
    parser = BasicParser(SimpleGrammarRulesParser().parse_read_grammar(grammar))

    composer = SemanticComposer(parser)
    executor = AtomExecutor(composer, model)

    write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_write_grammar())
    generator = BasicGenerator(write_grammar, model, sentence_context)

    # define the system

    system = System(
        model=model,
        input_pipeline=[
            TryFirst(parser),
            TryFirst(composer),
            TryFirst(executor),
        ],
        output_generator=generator
    )

    return system

