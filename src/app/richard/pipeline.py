import os
from app.richard.module.music.MusicModule import MusicModule
from richard.block.TryFirst import TryFirst
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.core.Pipeline import Pipeline
from richard.processor.parser.BasicParser import BasicParser
from app.richard.module.music.grammar import get_music_grammar


def create_pipeline():
    sentence_context = BasicSentenceContext()
    music_module = MusicModule(os.getenv('MY_MUSIC_FOLDER'))

    model = Model([
        sentence_context,
        music_module
    ])

    grammar = []
    grammar.extend(get_music_grammar())

    parser = BasicParser(SimpleGrammarRulesParser().parse(grammar))
    composer = SemanticComposer(parser)
    executor = AtomExecutor(composer, model)
    responder = SimpleResponder(model, executor)

    pipeline = Pipeline([
        TryFirst(parser),
        TryFirst(composer),
        TryFirst(executor),
        TryFirst(responder)
    ])

    return pipeline

