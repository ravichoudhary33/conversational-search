from langchain.chains.conversation.memory import ConversationBufferWindowMemory

conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True,
        input_key='input',
        output_key="output"
)