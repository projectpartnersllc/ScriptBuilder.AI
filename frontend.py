import streamlit as st
import requests
from typing import Dict, List, Union, Optional

# Configuration
BASE_URL = "http://127.0.0.1:8000"
SESSION_TYPES = [
    "Expert One", 
    "Expert Two", 
    "Expert Three", 
    "Expert Four", 
    "Expert Five", 
    "Expert Six", 
    "Expert Seven", 
    "Expert Eight"
]

def send_message(session_type: str, message: str) -> str:
    """
    Send message to backend and get response.
    
    Args:
        session_type (str): The type of session for context.
        message (str): The user's message to send.
    
    Returns:
        str: The response from the server or an error message.
    """
    endpoint = f"{BASE_URL}/chat/{session_type}"
    
    try:
        response = requests.post(endpoint, json={"user_message": message}, timeout=10)
        
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_data = response.json()
        return response_data.get("message", "No response received.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return f"Error: Unable to communicate with the server. {str(e)}"
    except ValueError as e:
        st.error(f"Response parsing error: {str(e)}")
        return "Error: Unable to parse server response."

def edit_message(section_id: str, updated_message: str) -> Union[Dict, str]:
    """
    Edit the most recent AI message.
    
    Args:
        section_id (str): The ID of the section to edit.
        updated_message (str): The updated message content.
    
    Returns:
        Union[Dict, str]: The server response or an error message.
    """
    endpoint = f"{BASE_URL}/edit-ai-message/"
    
    try:
        response = requests.put(endpoint, json={
            "section_id": section_id,
            "updated_message": updated_message
        }, timeout=10)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return f"Error: Unable to edit message. {str(e)}"
    except ValueError as e:
        st.error(f"Response parsing error: {str(e)}")
        return "Error: Unable to parse server response."

def initialize_conversations() -> Dict[str, List[Dict[str, str]]]:
    """
    Initialize conversation history for all session types.
    
    Returns:
        Dict[str, List[Dict[str, str]]]: A dictionary of conversations.
    """
    return {session: [] for session in SESSION_TYPES}

def main():
    """Main Streamlit application function."""
    st.set_page_config(page_title="SRS Generation Chat", layout="wide")
    
    # Initialize edit mode in session state if not exists
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    # Sidebar for session type selection and context
    with st.sidebar:
        st.header("Configuration")
        
        # File upload moved to top of sidebar
        st.subheader("File Upload")
        uploaded_file = st.file_uploader("Browse files", label_visibility="collapsed")
        
        st.divider()
        
        session_type = st.selectbox(
            "Select Relevant expert",
            SESSION_TYPES,
            help="Choose the context for your SRS generation"
        )
        st.divider()
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Select the appropriate session type for your current task
        - Keep context consistent within a session
        - Use clear and specific prompts
        """)
    
    st.title("🤖 Multi Agent Document Generation Assistant with RAG and Voice input functionality")
    
    # Initialize conversation history storage if not already present
    if "conversations" not in st.session_state:
        st.session_state.conversations = initialize_conversations()
    
    # Retrieve messages for the current session type
    messages = st.session_state.conversations[session_type]
    
    # Container for chat messages with scrolling
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages from history for the selected session type
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if uploaded_file is not None:
            st.session_state.conversations[session_type].append(
                {"role": "user", "content": f"Uploaded file: {uploaded_file.name}"}
            )
            st.success(f"File {uploaded_file.name} uploaded successfully!")
    
    # Spacer to push chat input to bottom
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    
    # Chat input area FIXED AT BOTTOM
    st.divider()
    
    # Chat input with mic button and edit option at very bottom
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        prompt = st.chat_input(f"Ask about {session_type} in SRS generation")
    with col2:
        mic_clicked = st.button("🎙️")
    with col3:
        edit_clicked = st.button("✏️")
    
    # Mic button functionality (simple recording placeholder)
    if mic_clicked:
        st.info("Mic button clicked! (Recording functionality to be implemented)")
    
    # Edit message functionality
    if edit_clicked:
        # Toggle edit mode
        st.session_state.edit_mode = not st.session_state.edit_mode
    
    # Display edit interface when edit mode is active
    if st.session_state.edit_mode:
        # Check if there are messages to edit
        if st.session_state.conversations[session_type]:
            # Get the last message
            last_message = st.session_state.conversations[session_type][-1]
            
            # Only allow editing of assistant messages
            if last_message["role"] == "assistant":
                st.markdown("### 📝 Edit Last Message")
                
                # Create an edit area with the current message content
                edit_message_text = st.text_area(
                    "Edit Message", 
                    value=last_message["content"],
                    height=200
                )
                
                # Columns for save and cancel buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Save Changes"):
                        if edit_message_text.strip():
                            # Call edit message function
                            result = edit_message(session_type, edit_message_text)
                            
                            if isinstance(result, dict):
                                # Update the last message in session state
                                st.session_state.conversations[session_type][-1]["content"] = edit_message_text
                                st.success("Message updated successfully!")
                                st.session_state.edit_mode = False
                                st.rerun()
                            else:
                                st.error(result)
                
                with col2:
                    if st.button("Cancel"):
                        # Exit edit mode
                        st.session_state.edit_mode = False
            else:
                st.warning("Only the last assistant message can be edited.")
        else:
            st.info("No messages to edit.")
    
    # Process user prompt
    if prompt:
        # Add user message to chat history
        st.session_state.conversations[session_type].append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Show a loading spinner while getting response
        with st.spinner("Generating response..."):
            response = send_message(session_type, prompt)
        
        # Add AI response to chat history
        st.session_state.conversations[session_type].append({"role": "assistant", "content": response})
        
        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Rerun to refresh the page and scroll to bottom
        st.rerun()

if __name__ == "__main__":
    main()


