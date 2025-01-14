from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from transformers import pipeline
from langchain_huggingface import HuggingFaceEndpoint

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

        if False:

            chain = prompt | \
                ChatOpenAI(model="gpt-4o-mini") | \
                StrOutputParser()

        else:

            hub_llm = HuggingFaceEndpoint(repo_id = 'tiiuae/falcon-7b-instruct',
                # lower temperature makes the output more deterministic
                temperature = 0.1
            )

            cha in = prompt | hub_llm | StrOutputParser()

        # Invoke the chain with a question and the memory
        # will track history
        response = chain.invoke({
            "question" : question,
            "history" : self.memory.load_memory_variables({})["history"]
        })

        self.memory.save_context({"question": question}, {"answer": response})

        # if more then 4 messages, summarize the history
        if len(self.memory.chat_memory.messages) > 8:
            self.summarize_history()

        return response


    def summarize_history(self):
        long_history = self.memory.load_memory_variables({})["history"]

        # load the model to perform summarization
        summarizer = pipeline("summarization",
                            model="facebook/bart-large-cnn")
        summary = summarizer(long_history,
                            max_length=150,
                            min_length=30,
                            do_sample=False)

        # clear the memory after summarizing
        self.memory.clear()

        # Save summarized context
        self.memory.save_context(
            { "summary": summary[0]['summary_text'] },
            { "answer": "" })
