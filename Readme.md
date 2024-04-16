# Ollama Test

## Installation

1. Install Ollama in your respective OS by visiting [ollama.com](https://ollama.com/).

2. Run the following command to retrieve llama2 from Ollama:

    ```
    ollama run llama2
    ```

    Press `Ctrl + Z` to exit the prompt.

3. Clone this repository:

    ```
    git clone https://github.com/JashKakadiya/Ollama_test.git
    ```

4. Create a virtual environment (requires Python 3.10):

    ```
    python3 -m venv venv 
    source venv/bin/activate
    ```

5. Install dependencies:

    ```
    pip install langchain python-docx pypdf llama-cpp-python==0.2.61 python-dotenv langchain-community pdfminer-six
    ```

## Usage

Run the application:

- python app.py