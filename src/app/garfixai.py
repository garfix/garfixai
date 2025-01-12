from richard.core.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from app.llm.LLMAccess import LLMAccess
from app.richard.pipeline import create_pipeline

class GarfixAI:
    richard: Pipeline
    llm_access: LLMAccess


    def __init__(self):
        # todo initialize the pipeline here
        self.llm_access = LLMAccess()
        self.use_richard = True

    def send(self, message: str):

        if self.use_richard:

            richard = create_pipeline()
            request = SentenceRequest(message)
            response = richard.enter(request)

        else:

            response = self.llm_access.enter(message)

        return response

