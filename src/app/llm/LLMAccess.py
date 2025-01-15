from langchain import PromptTemplate
from transformers import pipeline
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.memory import ConversationBufferMemory

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

        case = 'C'

        if case == 'A':

            chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

            # Invoke the chain with a question and the memory
            # will track history
            response = chain.invoke({
                "question" : question,
                "history" : self.memory.load_memory_variables({})["history"]
            })

        elif case == 'B':

            hub_llm = HuggingFaceEndpoint(repo_id = 'tiiuae/falcon-7b-instruct',
                # lower temperature makes the output more deterministic
                temperature = 0.1
            )

            chain = prompt | hub_llm | StrOutputParser()

            # Invoke the chain with a question and the memory
            # will track history
            response = chain.invoke({
                "question" : question,
                "history" : self.memory.load_memory_variables({})["history"]
            })


        elif case == 'C':

            text = '''
                Diabetes mellitus is a chronic metabolic disorder
                characterized by high blood sugar levels, which can lead
                to serious health complications if not effectively
                managed. There are two primary types of diabetes: Type
                1 diabetes, which is an autoimmune condition where the
                immune system mistakenly attacks insulin-producing beta
                cells in the pancreas, leading to little or no insulin
                production; and Type 2 diabetes, which is often
                associated with insulin resistance and is more prevalent
                in adults, though increasingly observed in children and
                adolescents due to rising obesity rates. Risk factors
                for developing Type 2 diabetes include genetic
                predisposition, sedentary lifestyle, poor dietary
                choices, and obesity, particularly visceral fat that
                contributes to insulin resistance. When blood sugar
                levels remain elevated over time, they can cause damage
                to various organs and systems, increasing the risk of
                cardiovascular diseases, neuropathy, nephropathy, and
                retinopathy, among other complications. Management of
                diabetes requires a multifaceted approach, which
                includes regular monitoring of blood glucose levels,
                adherence to a balanced diet rich in whole grains,
                fruits, vegetables, and lean proteins, and engaging in
                regular physical activity. In addition to lifestyle
                modifications, many individuals with Type 2 diabetes
                may require oral medications or insulin therapy to help
                regulate their blood sugar levels. Education about the
                condition is crucial, as it empowers individuals to make
                informed decisions regarding their health. Furthermore,
                the role of technology in diabetes management has grown
                significantly, with continuous glucose monitors and
                insulin pumps providing real-time feedback and improving
                the quality of life for many patients. As research
                continues to advance, emerging therapies such as
                glucagon-like peptide-1 (GLP-1) receptor agonists and
                sodium-glucose cotransporter-2 (SGLT2) inhibitors are
                being explored for their potential to enhance glycemic
                control and reduce cardiovascular risk. Overall, with
                appropriate management strategies and support,
                individuals living with diabetes can lead fulfilling
                lives while minimizing the risk of complications
                associated with the disease.
            '''

            # Define chunk size and overlap size
            chunk_size = 300
            overlap_size = 1  # Number of sentences to overlap

            # Split the text into chunks with overlap
            text_chunks = split_text_with_overlap(
                            text, chunk_size, overlap_size)

            # Print the resulting chunks
            for i, chunk in enumerate(text_chunks):
                print(f"Chunk {i+1}:\n{chunk}\n")


            # creates an DocArrayInMemorySearch store and
            # insert data
            vectorstore = DocArrayInMemorySearch.from_texts(
                text_chunks,
                embedding = OpenAIEmbeddings(),
            )

            retriever = vectorstore.as_retriever()

            template = """Answer the question based only on the
                following context: {context}
                Question: {question}
            """

            # uses a model from OpenAI
            model = ChatOpenAI(model = "gpt-4o-mini")

            # creates the prompt
            prompt = ChatPromptTemplate.from_template(template)

            # creats the output parser
            output_parser = StrOutputParser()

            # RunnableParallel is used to run multiple processes or
            # operations in parallel
            setup_and_retrieval = RunnableParallel(
                {
                    "context": retriever,
                    "question": RunnablePassthrough()
                }
            )

            # creating the chain
            chain = setup_and_retrieval | prompt | model | output_parser

            # Invoke the chain with a question and the memory
            # will track history
            response = chain.invoke(question)


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


def split_text_with_overlap(text, chunk_size, overlap_size):
    # Split the text into sentences
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Check if adding this sentence exceeds the chunk size
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            if current_chunk:  # If it's not the first sentence
                current_chunk += ". "
            current_chunk += sentence
        else:
            # Store the current chunk
            chunks.append(current_chunk.strip())
            # Create a new chunk with the overlap
            # Add the last `overlap_size` sentences from
            # the current chunk
            overlap_sentences = \
                current_chunk.split('. ')[-overlap_size:]
            current_chunk = '. '.join(overlap_sentences) + \
                            ". " + sentence

    # Add any remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
