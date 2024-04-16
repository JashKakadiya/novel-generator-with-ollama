from langchain.chains import LLMChain
from langchain.globals import set_debug
#from langchain.chat_models import ChatOpenAI
#from langchain_community.llms import LlamaCpp
from langchain_community.llms import Ollama

set_debug(True)

# ollama pull llama2 to download first - smallest test model - others based on name

#n_gpu_layers = -1  # -1 all GPUs 
#n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

class BaseStructureChain:

    PROMPT = ''

    def __init__(self) -> None:

#        self.llm = LlamaCpp()
        self.llm = Ollama()
#        self.llm = ChatOpenAI()

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True


class BaseEventChain:
    
    PROMPT = ''

    def __init__(self) -> None:

        self.llm = Ollama('llama2:13b') #llama2:13b
#        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k') # NEED LOCAL MODEL
#        self.llm = LlamaCpp(
#                 model_path='Norocetacean/norocetacean-20b-10k.Q8_0.gguf', 
#                 n_gpu_layers=n_gpu_layers, 
#                 n_batch=n_batch, 
#                 temperature=0.75, 
#                 n_ctx=2048, 
#                 max_tokens=2000, 
#                 top_p=1, 
#                 f16_kv=True, 
#                 verbose=True) #

        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )

        self.chain.verbose = True
