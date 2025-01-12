from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class LLMAccess:

    def enter(self, message: str):

        template = '''
            Question: {question}
            Answer:
        '''

        prompt = PromptTemplate(
            template = template,
            input_variables = ['question']
        )

        model = ChatOpenAI(model="gpt-4o-mini")

        output_parser = StrOutputParser()

        # create the chain
        chain = prompt | model | output_parser

        r = chain.invoke({"question": message})
        return r

