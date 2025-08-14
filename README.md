# Conversational AI with Phi-2 and GraphRAG for UAT Testing

This project is a Flask-based web application that provides a chat interface for interacting with a Phi-2 GGUF model. It includes features for session management, conversation history, and dynamic prompt template configuration. Additionally, it incorporates GraphRAG technology for User Acceptance Testing (UAT) to automatically generate test cases from user stories.

## Features

*   **Conversational Interface:** A user-friendly chat interface for interacting with the AI.
*   **Session Management:** Chat sessions are automatically saved and can be revisited later.
*   **Chat History:** View and manage previous chat sessions.
*   **Session Deletion:** Users can delete unwanted chat sessions.
*   **Customizable Prompt Template:** The prompt template used to instruct the AI can be modified through the settings page.
*   **UAT Testing with GraphRAG:** Generate test cases from user stories using GraphRAG technology.
*   **Test Case Management:** View, save, and configure generated test cases.
*   **Variable Configuration:** Identify and configure test variables for execution.
*   **Knowledge Base:** Store test cases in ChromaDB for future reference and similarity matching.

## Project Structure

The project is organized into the following files and directories:

*   `app_chat.py`: The main Flask application file. It contains the server-side logic for handling chat requests, session management, and rendering the web pages.
*   `templates/`: This directory contains the HTML templates for the web interface.
    *   `index.html`: The main chat page.
    *   `settings.html`: The settings page for configuring the prompt template.
*   `static/`: This directory contains the CSS stylesheet for the web interface.
    *   `style.css`: The stylesheet for the application.
*   `sessions.db`: A `shelve` database file used to store chat session data. This file is created automatically when the application is run for the first time.
*   `phi-2.Q4_K_M.gguf`: The GGUF model file. This file must be present in one of the possible paths defined in `app_chat.py`.

## Setup and Installation

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements_py310.txt
    ```

2.  **Download the Model:**
    Download the `phi-2.Q4_K_M.gguf` model file and place it in the project's root directory, or one of the other specified paths in `app_chat.py`.

3.  **Run the Application:**
    ```bash
    python app_chat.py
    ```
    The application will be available at `http://127.0.0.1:8080` by default.

## How It Works

### Session Management

The application uses a `shelve` database (`sessions.db`) to store chat sessions. Each session is a dictionary containing the chat history.

*   **New Chat:** A new chat session is created when the user clicks the "+ New Chat" button.
*   **Saving a Session:** The current chat session is saved when the user clicks the "Save Session" button. The session is named based on the first user prompt.
*   **Loading a Session:** Clicking on a session in the chat history loads the conversation into the chat window.
*   **Deleting a Session:** Clicking the "x" button next to a session will delete it from the database.

### Prompt Template

The AI's responses are guided by a prompt template, which can be customized in the settings page. The `{prompt}` placeholder in the template is replaced with the user's input.

### UAT Testing with GraphRAG

The application includes a specialized UAT testing module that uses GraphRAG technology to automatically generate test cases from user stories. This feature can be accessed through the "UAT" button in the main chat interface.

#### How It Works

1. **User Story Input**: Users provide user stories in the standard format (e.g., "As a [user role], I want to [goal] so that [benefit]")
2. **Entity Extraction**: The system extracts relevant entities from the user story (user roles, functional areas, test types, etc.)
3. **Similar Case Retrieval**: ChromaDB is queried for similar historical test cases
4. **Test Case Generation**: GraphRAG generates new test cases based on the user story and similar cases
5. **Variable Identification**: The system identifies test variables that need to be configured
6. **Test Execution**: Users can configure variables and execute tests (planned for future enhancement)

#### GraphRAG Components

*   `graph_rag.py`: Contains the GraphRAG implementation including entity extraction, knowledge graph construction, and test case generation
*   `templates/uat.html`: The UAT testing interface
*   `test_graphrag.py`: A test script to verify GraphRAG functionality
*   `UAT_TESTING_README.md`: Detailed documentation for the UAT testing module

For more detailed information about the UAT testing functionality, please refer to the `UAT_TESTING_README.md` file.
