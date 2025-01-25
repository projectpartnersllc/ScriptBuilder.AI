# Multi-Agent Document Generation Assistant

A sophisticated document generation system leveraging multiple AI agents, [RAG (Retrieval-Augmented Generation)](https://www.pinecone.io/learn/retrieval-augmented-generation/), and voice input functionality for creating comprehensive documentation.

## Features

- **Multi-Expert System**: 8 specialized AI agents working in harmony:
    - Content Strategist
    - Technical Writer
    - Editor
    - Fact Checker
    - Format Specialist
    - Research Assistant
    - Voice Processing Expert
    - Quality Assurance Agent
- **Voice Input Integration**: High-accuracy audio transcription using [Deepgram API](https://deepgram.com/docs/api-reference)
- **Memory Inheritance**: Sophisticated context management between experts using LangChain's memory modules
- **Real-time Editing**: Edit generated content on the fly with version control
- **File Upload Support**: Process multiple document formats (PDF, DOCX, TXT) for additional context
- **Interactive UI**: [Streamlit](https://streamlit.io)-based user interface with real-time chat functionality

## Architecture

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) server with [LangChain](https://python.langchain.com/) integration for AI orchestration
- **Frontend**: Streamlit interface with dynamic components
- **Voice Processing**: Deepgram API integration for real-time transcription
- **LLM**: [Groq](https://groq.com/) LLM integration for high-speed inference

## Installation

```bash
# Clone the repository
git clone <repository-url>

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GROQ_API_KEY="your-groq-api-key"
export DEEPGRAM_API_KEY="your-deepgram-api-key"
```

## Usage

1. Start the backend server:
```bash
uvicorn backend:app --reload --port 8000
```

2. Launch the frontend:
```bash
streamlit run frontend.py
```

3. Access the application at `http://localhost:8501`

## API Endpoints

- `POST /chat/{session_type}`: Process chat messages with different expert agents
- `PUT /edit-ai-message/`: Edit and version control generated content
- `POST /upload-file/`: Process document uploads
- `POST /transcribe-audio/`: Handle voice input transcription
- `GET /session-history/`: Retrieve chat history and context

## System Requirements

- Python 3.8+
- FastAPI 0.68+
- Streamlit 1.10+
- LangChain 0.1+
- Deepgram SDK 2.11+
- 4GB RAM minimum
- Internet connection for API access

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed changes.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Documentation

Detailed documentation is available in the [/docs](./docs) directory.

