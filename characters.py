import os
# from langchain.document_loaders import PyPDFLoader
from pdfminer.high_level import extract_text
#from langchain.chat_models import ChatOpenAI
#from langchain_community.llms import LlamaCpp
from langchain_community.llms import Ollama
from langchain.chains import LLMChain

class MainCharacterChain:

    PROMPT = """
    You are provided with the resume of a person. 
    Describe the person's profile in a few sentences and include that person's name.

    Resume: {text}

    Profile:"""

    def __init__(self) -> None:

#        self.llm = LlamaCpp()
        self.llm = Ollama()
#        self.llm = ChatOpenAI()
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )

        self.chain.verbose = True

    # def load_resume(self, file_name):
    #     folder = 'docs'
    #     file_path = os.path.join(folder, file_name)
    #     loader = PyPDFLoader(file_path)
    #     docs = loader.load_and_split()
    #     return docs

    def run(self, file_name):
        # docs = self.load_resume(file_name)
        # resume = '\n\n'.join([doc.page_content for doc in docs])
        resume = extract_text(file_name)
        return self.chain.run(resume)
