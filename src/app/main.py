from configuration import get_config
from music.MusicModule import MusicModule
from richard.block.TryFirst import TryFirst
from richard.module.BasicSentenceContext import BasicSentenceContext
from richard.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from richard.processor.responder.SimpleResponder import SimpleResponder
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.AtomExecutor import AtomExecutor
from richard.core.Model import Model
from richard.entity.SentenceRequest import SentenceRequest
from richard.core.Pipeline import Pipeline
from richard.processor.parser.BasicParser import BasicParser
from src.app.grammar import get_grammar

def talk_to_computer():

    sentence_context = BasicSentenceContext()
    config = get_config()
    music_module = MusicModule(config)

    model = Model([
        sentence_context,
        music_module
    ])

    grammar = get_grammar()
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

    while True:

        text = input('> ')

        if text == "exit":
            break

        if text == "aha":
            text = "Play some A-ha"

        request = SentenceRequest(text)
        response = pipeline.enter(request)
        print(response)

if __name__ == '__main__':
    talk_to_computer()
