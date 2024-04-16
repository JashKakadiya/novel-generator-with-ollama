from langchain.chains import LLMChain
from langchain.globals import set_debug
from langchain_community.llms import Ollama

set_debug(True)
class BaseStructureChain:

    PROMPT = ''

    def __init__(self) -> None:


        self.llm = Ollama('llama2')


        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True


class BaseEventChain:
    
    PROMPT = 'hello'

    def __init__(self) -> None:

        self.llm = Ollama(model='llama2') 

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True
        
