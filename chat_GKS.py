# Description: Chatbot for the God's Kingdom Society (GKS).
# The interface allows users to ask questions about the GKS and its doctrines.
# The chatbot provides responses based on the input questions.

import os
import textwrap
import gradio as gr
from typing import List, Tuple, Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from config import settings
import warnings
warnings.filterwarnings('ignore')

groq_api_key = settings.groq_api_key

# Directory containing PDF files
pdf_directory = "data"

# Create `data` directory if it doesn't exist
os.makedirs(pdf_directory, exist_ok=True)

# Directory to store the Chroma database
persist_directory = "chroma_db"
os.makedirs(persist_directory, exist_ok=True)

# Get list of PDF files
pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Load documents
documents = []
for file_path in pdf_files:
    try:
        loader = PyPDFLoader(file_path)
        doc = loader.load()
        documents.extend(doc)
        print(f"Successfully loaded: {file_path}")
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")

# Text splitting
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Embeddings and vector store
embeddings = HuggingFaceEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=persist_directory)
retriever = vectordb.as_retriever(k=7)

# LLM initialization
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, groq_api_key=groq_api_key)

# Custom prompt template
template = """
    You are a knowledgeable and helpful AI assistant for the God's Kingdom Society (GKS).
    Use the following pieces of context to answer the question, but do not mention or refer to the context/documents in your response.
    Instead, respond as if the knowledge is part of your own understanding. If you do not have an answer, you can say so.

Context: {context}

Current conversation:
{chat_history}

Question: {question}

Helpful Answer:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=['context', 'chat_history', 'question'])

# Conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", output_key="answer", return_messages=True)

# Conversational chain
conv_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    combine_docs_chain_kwargs={'prompt': QA_PROMPT},
    memory=memory,
    verbose=True
)

class ChatInterface:
    def __init__(self, conversation_chain):
        self.conv_chain = conversation_chain

    def process_message(self, message: str, history: list) -> tuple:
        try:
            response = self.conv_chain.invoke({"question": message, "chat_history": history})
            return response['answer'], history + [(message, response['answer'])]
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            print(f"Error: {error_msg}")
            return error_msg, history + [(message, error_msg)]

    def create_interface(self) -> gr.Interface:
        with gr.Blocks(title="Chat GKS") as interface:
            gr.Markdown(
                """<div style="text-align: center; font-size: 2.5em;">
                <strong>
                Chat GKS
                </strong>
                </div>
                """
                )
            gr.Markdown("Hail Jehovah and Jesus Christ 🙏🏿!")
            gr.Markdown("Ask me anything about the GKS and Her doctrines, I'm here to help.")
            gr.Markdown(
                """<span style="font-size: 1.3em;">
                <strong>Please NOTE—this bot may make errors, ALWAYS verify sensitive information by
                <a href="https://www.mountaingks.org/contact/">Contacting the GKS
                </a></strong>
                </span>.
                """
                )

            chatbot = gr.Chatbot(height=400, show_label=False, container=True, bubble_full_width=False)
            msg = gr.Textbox(placeholder="Type your question here...", show_label=False, container=False, scale=5)
            submit = gr.Button("Send", scale=1, variant="primary")
            clear = gr.Button("Clear Chat")
            state = gr.State([])

            submit.click(
                self.process_message,
                inputs=[msg, state],
                outputs=[chatbot, state],
                api_name="submit"
            )
            msg.submit(
                self.process_message,
                inputs=[msg, state],
                outputs=[chatbot, state],
                api_name="submit_message"
            )
            clear.click(lambda: ([], []), outputs=[chatbot, state], api_name="clear")
            submit.then(lambda: "", None, msg)
            msg.submit(lambda: "", None, msg)

        return interface