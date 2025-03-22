from chat_GKS import ChatInterface
from chat_GKS import conv_chain  # Import your conversation chain

# Initialize the chat interface
chat_interface = ChatInterface(conv_chain)

# Create and launch the interface
interface = chat_interface.create_interface()
interface.launch()