# UAT Testing with GraphRAG

This application extends the conversational AI with GraphRAG capabilities for User Acceptance Testing (UAT). It allows users to input user stories and automatically generate test cases using GraphRAG technology.

## Features

1. **Conversational AI Interface**: Chat with the Phi-2 model
2. **UAT Testing Module**: Generate test cases from user stories using GraphRAG
3. **Test Case Management**: View, save, and configure test cases
4. **Variable Configuration**: Identify and configure test variables
5. **Knowledge Base**: Store test cases in ChromaDB for future reference

## Prerequisites

1. Python 3.10
2. Required Python packages (see `requirements_py310.txt`)
3. Phi-2 GGUF model file (`phi-2.Q4_K_M.gguf`)

## Setup Instructions

1. Install the required Python packages:
   ```bash
   python3.10 -m pip install -r requirements_py310.txt
   ```

2. Download the Phi-2 GGUF model file and place it in the `uat_test` directory:
   - Model file: `phi-2.Q4_K_M.gguf`
   - The application expects this file to be in the same directory as `app_chat.py`

3. Run the application:
   ```bash
   python3.10 app_chat.py
   ```

4. Access the application in your browser:
   - The application will start on `http://127.0.0.1:8080` by default
   - In CDSW, it will automatically use the appropriate IP and port

## Usage

1. **Chat Interface**:
   - Use the main chat interface to interact with the Phi-2 model
   - Save chat sessions for future reference
   - Adjust prompt templates in the settings

2. **UAT Testing**:
   - Click the "UAT" button in the top right corner to access the UAT testing module
   - Enter a user story in the provided text area
   - Click "Generate Test Cases" to create test cases using GraphRAG
   - View generated test cases and configure test variables
   - Save test cases to the knowledge base for future use

## GraphRAG Implementation

The GraphRAG implementation includes:

1. **Local Embedding Generation**: Creates embeddings without external API calls
2. **Knowledge Graph Construction**: Uses NetworkX to build knowledge graphs from UAT documents
3. **Entity Extraction**: Identifies UAT-related entities (user roles, functional areas, test types, etc.)
4. **Test Case Generation**: Creates test cases based on user stories and historical data
5. **Variable Identification**: Extracts and categorizes test variables from test cases
6. **ChromaDB Integration**: Stores and retrieves test cases using vector database

## File Structure

- `app_chat.py`: Main Flask application with both chat and UAT functionality
- `graph_rag.py`: GraphRAG implementation for UAT testing
- `templates/index.html`: Main chat interface
- `templates/settings.html`: Settings interface
- `templates/uat.html`: UAT testing interface
- `static/style.css`: Shared CSS styles
- `requirements_py310.txt`: Python package requirements
- `phi-2.Q4_K_M.gguf`: Phi-2 model file (needs to be downloaded separately)

## How It Works

1. **User Story Input**: Users provide user stories in the standard format
2. **Entity Extraction**: The system extracts relevant entities from the user story
3. **Similar Case Retrieval**: ChromaDB is queried for similar historical test cases
4. **Test Case Generation**: GraphRAG generates new test cases based on the user story and similar cases
5. **Variable Identification**: The system identifies test variables that need to be configured
6. **Test Execution**: Users can configure variables and execute tests (future enhancement)

## Future Enhancements

1. Integration with test execution frameworks
2. Enhanced natural language processing for better entity extraction
3. More sophisticated similarity matching in ChromaDB
4. Test result tracking and reporting
5. Integration with CI/CD pipelines
