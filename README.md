# LLM RAG Chatbot for Church Organization

An AI-powered chatbot for the God's Kingdom Society built using LangChain and Hugging Face. Designed to support the God's Kingdom Society (GKS), the chatbot leverages a collection of GKS documents stored in the `data` folder for document retrieval and uses a Gradio interface for interactive deployment. The chatbot is deployed on Hugging Face Spaces.

## Features

- **Retrieval-Augmented Generation (RAG):** Answers questions about GKS doctrines; combines document retrieval with language generation for contextually relevant answers. 
- **PDF Document Integration:** Processes and splits PDF files located in the `data` folder to provide additional context during conversations.
- **Interactive Chat Interface:** Built with Gradio, offering an easy-to-use web interface.
- **Conversational Memory:** Maintains conversation history for a more natural and coherent dialogue.
- **Deployment Ready:** Configured to run on Hugging Face Spaces with minimal modifications.

## Technical Details
- Built with Python
- Uses Chroma for vector storage
- Powered by the LLaMA model via Groq API
- Interface built with Gradio

## Repository Structure

```
ChatGKS/
├── app.py                # Main entry point for launching the Gradio interface
├── config.py             # Configuration file for environment variables and API keys
├── chat_GKS.py      # Main application code containing the chatbot and conversational logic
├── data/                 # Folder containing PDF files for the retrieval process
├── requirements.txt      # List of required Python packages
├── LICENSE               # License file (MIT License recommended)
├── WORK_CONSENT          # The requirements and process for obtaining consent to create and distribute derivative works.
└── README.md             # This readme file
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/WoDauKuro/ChatGKS.git
   cd ChatGKS
   ```

2. **Set up a virtual environment (optional):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   - Create a `.env` file (or set secrets via Hugging Face Spaces settings) with your API keys, for example:
     ```
     groq_api_key=your_groq_api_key
     ```

## Usage

### Local Testing

Run the application locally by executing:

```bash
python app.py
```

This command will launch the Gradio interface, and you can access it in your web browser (typically at `http://localhost:7860`).

### Deployment on Hugging Face Spaces

1. **Create a new Space** on [Hugging Face](https://huggingface.co/spaces) and select the **Gradio** template.
2. **Push your repository** to the Space either via Git or by uploading files.
3. **Set your environment variables** (e.g., `groq_api_key`) in the Space settings under "Secrets".
4. The Space will automatically build and launch your Gradio app.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Derivative Works

**Important:** While the Apache License 2.0 allows derivative works, the author(s) of this project require explicit written consent for any derivative work to be distributed or used publicly.

Please refer to the [Derivative Work Consent](WORK_CONSENT.md) document for instructions on how to request consent.

## Contact

For questions or further information, please contact [Wodaukuro](kurolegz7@gmail.com)

## Acknowledgments
Special thanks to the LangChain community and Hugging Face for providing open-source tools that made this project possible. 
Additionally, gratitude to the God's Kingdom Society for their support and feedback in shaping this chatbot.