import uvicorn
from fastapi import FastAPI, HTTPException, Path, UploadFile, File
from pydantic import BaseModel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, AIMessage, BaseChatMessageHistory
from typing import List, Dict, Optional
from prompts import *  # Ensure you have this import

# Initialize the LLM
llm = ChatGroq(
    model_name="llama3-8b-8192",
    api_key='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'
)



# Create a template for synonyms generation
synonym_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that generates synonyms. Only provide a comma-separated list of synonyms."),
    ("human", "Generate synonyms for this word: {word}")
])

# Create the synonym chain
synonym_chain = synonym_template | llm

# Function to get synonyms
async def get_synonyms(word: str) -> str:
    """Get synonyms for a given word."""
    try:
        response = await synonym_chain.ainvoke({"word": word})
        return response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating synonyms: {str(e)}")


# Initialize FastAPI app
app = FastAPI(
    title="Comprehensive SRS Generation App",
    version="1.0",
    description="Advanced Software Requirements Specification Generation Assistant"
)

# Storage
chat_store: Dict[str, ChatMessageHistory] = {}
long_term_memory: Dict[str, List[str]] = {}

# Memory inheritance map with expert identifiers
memory_inheritance = {
    "expert1": ["expert1"],
    "expert2": ["expert1"],
    "expert3": ["expert2"],
    "expert4": ["expert2", "expert3"],
    "expert5": ["expert1", "expert2", "expert4"],
    "expert6": ["expert3", "expert2", "expert4"],
    "expert7": ["expert3", "expert2", "expert4"],
    "expert8": ["expert2", "expert3"]
}

chat_inheritance = memory_inheritance.copy()

def get_chat_history(session_id: str) -> BaseChatMessageHistory:
    """Get chat history for a session, including inherited messages."""
    if session_id not in chat_store:
        chat_store[session_id] = ChatMessageHistory()
    
    session_history = chat_store[session_id]
    
    if session_id in chat_inheritance:
        for inherited_session in chat_inheritance[session_id]:
            if inherited_session in chat_store:
                last_message = get_last_conversation(inherited_session)
                if last_message:
                    session_history.add_message(
                        AIMessage(content=f"Inherited from {inherited_session}: {last_message.content}")
                    )
    
    return session_history

def get_last_conversation(session_id: str) -> BaseMessage:
    """Get the last message from a session's conversation history."""
    history = chat_store.get(session_id)
    if history and history.messages:
        return history.messages[-1]
    return None

def create_chat_prompt_template(template_name: str) -> ChatPromptTemplate:
    """Create a chat prompt template with the given system message."""
    return ChatPromptTemplate.from_messages([
        ("system", template_name),
        ("system", "Long-term memory: {long_term_memory}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

# Create prompt templates
prompt_templates = {
    "expert1": create_chat_prompt_template(expert1),
    "expert2": create_chat_prompt_template(expert2),
    "expert3": create_chat_prompt_template(expert3), 
    "expert4": create_chat_prompt_template(expert4),
    "expert5": create_chat_prompt_template(expert5),
    "expert6": create_chat_prompt_template(expert6),
    "expert7": create_chat_prompt_template(expert7),
    "expert8": create_chat_prompt_template(expert8)
}

# Create chains
chains = {
    session_type: RunnableWithMessageHistory(
        prompt_templates[session_type] | llm,
        get_chat_history,
        input_messages_key="input",
        history_messages_key="history"
    ) for session_type in prompt_templates.keys()
}

def get_long_term_memory(session_id: str) -> str:
    """Get long-term memory for a session, including inherited memories."""
    memories = []
    
    if session_id in long_term_memory:
        memories.append(f"Session {session_id} memory: {'. '.join(long_term_memory[session_id])}")
    
    if session_id in memory_inheritance:
        for inherited_session in memory_inheritance[session_id]:
            if inherited_session in long_term_memory:
                memories.append(f"Inherited from {inherited_session}: {'. '.join(long_term_memory[inherited_session])}")
    
    return "\n".join(memories)

def update_long_term_memory(session_id: str, input: str, output: str):
    """Update long-term memory for a session."""
    if session_id not in long_term_memory:
        long_term_memory[session_id] = []
    if len(input) > 20:
        long_term_memory[session_id].append(f"User said: {input}")
    if len(long_term_memory[session_id]) > 5:
        long_term_memory[session_id] = long_term_memory[session_id][-5:]

# Request models
class UserMessage(BaseModel):
    user_message: str

class EditMessageRequest(BaseModel):
    section_id: str
    updated_message: str


# Supported session types
SUPPORTED_SESSION_TYPES = {
    "expert1", "expert2", "expert3", "expert4",
    "expert5", "expert6", "expert7", "expert8"
}

# # Variables to store mic and file inputs (You can adjust this based on your need)
# microphone_input: Optional[str] = None
# file_input: Optional[UploadFile] = None

# # Function to simulate microphone input handling (this can be later replaced with real microphone input handling logic)
# def set_microphone_input(mic_input: str):
#     """Simulate setting microphone input."""
#     global microphone_input
#     microphone_input = mic_input
#     return {"message": f"Microphone input received: {microphone_input}"}

# # Function to handle file upload input
# async def set_file_input(file: UploadFile = File(...)):
#     """Handle file upload and store the file."""
#     global file_input
#     file_input = file
#     return {"message": f"File uploaded: {file.filename}"}

async def chat(input_text: str, session_id: str) -> str:
    """Process a chat message using the appropriate chain."""
    if session_id not in chains:
        raise HTTPException(status_code=400, detail=f"Invalid session ID: {session_id}")
    
    chain = chains[session_id]
    long_term_mem = get_long_term_memory(session_id)
    
    try:
        response = await chain.ainvoke(
            {"input": input_text, "long_term_memory": long_term_mem},
            config={"configurable": {"session_id": session_id}}
        )
        
        update_long_term_memory(session_id, input_text, response.content)
        return response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

# Function to edit the most recent AI message
def edit_most_recent_ai_message(chat_store, section_id: str, updated_message: str):
    """Fetches the most recent AI message from a specified section, allows editing, and updates it in the chat store."""
    if section_id not in chat_store:
        return {"error": f"Section ID '{section_id}' not found in chat store."}

    section_messages = chat_store[section_id].messages

    for message in reversed(section_messages):
        if message.type == 'ai':
            message.content = updated_message
            return {"message": f"Message updated to: {message.content}"}

    return {"error": "No AI message found to edit in the specified section."}

# Chat endpoint
@app.post("/chat/{session_type}")
async def handle_chat(
    session_type: str = Path(..., description="The type of chat session"),
    request: UserMessage = None,
):
    """Unified chat endpoint with session type passed as a URL parameter."""
    try:
        # Validate session type
        if session_type not in SUPPORTED_SESSION_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid session type: {session_type}. Supported types are {', '.join(SUPPORTED_SESSION_TYPES)}.",
            )
        
        # Process the chat request
        message = await chat(request.user_message, session_type)
        return {"message": message}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to edit the most recent AI message
@app.put("/edit-ai-message/")
async def edit_ai_message(request: EditMessageRequest):
    result = edit_most_recent_ai_message(chat_store, request.section_id, request.updated_message)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])
    return result


# Function to run the server
def run_backend():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    run_backend()