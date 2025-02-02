from richard.core.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from app.llm.LLMAccess import LLMAccess
from app.richard.system import create_system

class GarfixAI:
    richard: Pipeline
    llm_access: LLMAccess


    def __init__(self):
        # todo initialize the pipeline here
        self.llm_access = LLMAccess()
        self.use_richard = True

    def send(self, message: str):

        if self.use_richard:

            system = create_system()
            request = SentenceRequest(message)
            system.enter(request)
            response = system.read_output()

        else:

            response = self.llm_access.enter(message)

        return response

