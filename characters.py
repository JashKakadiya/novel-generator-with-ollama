import os
from pdfminer.high_level import extract_text
from langchain_community.llms import Ollama
from langchain.chains import LLMChain

class MainCharacterChain:

    PROMPT = """
    You are provided with the resume of a person. 
    Describe the person's profile in a few sentences and include that person's name.

    Resume: {text}

    Profile:"""

    def __init__(self) -> None:

        self.llm = Ollama()
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )

        self.chain.verbose = True


    def run(self, file_name):
        resume = extract_text(file_name)
        return self.chain.run(resume)
