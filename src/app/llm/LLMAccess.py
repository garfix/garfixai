from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class LLMAccess:
    # see https://www.codemag.com/Article/2501051/Exploring-LangChain-A-Practical-Approach-to-Language-Models-and-Retrieval-Augmented-Generation-RAG

    memory: ConversationBufferMemory


    def __init__(self):
        # Set up conversational memory
        self.memory = ConversationBufferMemory()


    def enter(self, question: str):

        # Define the prompt template
        template = '''
            Previous conversation: {history}
            Question: {question}
            Answer:
        '''

        # Create the PromptTemplate with history
        prompt = PromptTemplate(
            template = template,
            input_variables = ['history', 'question']
        )

        chain = prompt | \
                ChatOpenAI(model="gpt-4o-mini") | \
                StrOutputParser()

        # Invoke the chain with a question and the memory
        # will track history
        response = chain.invoke({
            "question" : question,
            "history" : self.memory.load_memory_variables({})["history"]
        })

        self.memory.save_context({
            "question": question
        }, {
            "answer": response
        })

        return response

