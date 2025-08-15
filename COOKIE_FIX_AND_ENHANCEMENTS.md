# Cookie Size Fix and Model Enhancements

This document describes the changes made to address the session cookie size limitation and enhance the model's generation capabilities.

## Problem Description

The application was experiencing issues where:

1. **Session Cookie Size Limitation**: The session cookie was too large (4969 bytes) exceeding the browser limit (4093 bytes), causing browsers to silently ignore these cookies. This resulted in session data being lost and model responses disappearing.

2. **Limited Context Generation**: The model was configured with a small context window size (2048 tokens) and default token generation limit (256 tokens), which restricted its ability to handle complex queries and generate detailed responses.

## Solution Implementation

### 1. Server-Side Session Storage

To address the cookie size issue, we implemented server-side session storage using the existing `shelve` database approach:

- **Session ID in Cookie**: Only a small session identifier is stored in the browser cookie (well under the 4KB limit)
- **Server-Side Storage**: All chat history and timings data are stored on the server in the `sessions.db` file
- **Enhanced Session Functions**: Updated session management functions to handle both history and timings data:
  - `save_session(session_id, history, timings='')`
  - `load_session(session_id)` returns `(history, timings)`
  - Added `cleanup_old_sessions()` function to manage disk space

### 2. Model Context Window Enhancement

Increased the model's context window size to allow for more complex conversations:

- **Before**: `n_ctx=2048`
- **After**: `n_ctx=4096`
- **Benefit**: Allows the model to process longer prompts and maintain more conversation history

### 3. Token Generation Limit Enhancement

Increased the default token generation limit to allow for more detailed responses:

- **Frontend Default**: Updated from 256 to 512 tokens
- **Backend Default**: Updated from 256 to 512 tokens
- **Max Limit**: Increased from 1024 to 2048 tokens
- **Benefit**: Users can generate longer, more detailed responses without manually adjusting settings

### 4. Dependency Management

Added the missing `llama-cpp-python` dependency to the requirements file:

- **Before**: Only `ctransformers` was listed
- **After**: Both `ctransformers` and `llama-cpp-python` are listed
- **Benefit**: Ensures proper installation of all required libraries

### 5. Error Handling Improvements

Enhanced error handling in the response generation function:

- **Before**: No specific error handling for model generation issues
- **After**: Added try/except block around model generation to catch and report errors
- **Benefit**: Provides better feedback when issues occur and prevents application crashes

## Files Modified

1. **`app_chat.py`**:
   - Implemented server-side session storage functions
   - Updated session management routes to use new functions
   - Increased model context window from 2048 to 4096 tokens
   - Added error handling to response generation
   - Updated default max_tokens value in ask route

2. **`templates/index.html`**:
   - Updated default max_tokens value in form from 256 to 512
   - Increased max_tokens input maximum from 1024 to 2048

3. **`requirements_py310.txt`**:
   - Added `llama-cpp-python==0.2.56` dependency

## Testing

A test script (`test_cookie_fix.py`) has been created to verify all changes:

1. **Server-Side Session Storage**: Tests saving, loading, and deleting sessions
2. **Model Parameters**: Verifies the model loading function and context window size
3. **Frontend Defaults**: Checks that the default values in the HTML template are correct
4. **Requirements**: Ensures the llama-cpp-python dependency is in the requirements file

## Benefits

These changes provide several key benefits:

1. **Eliminates Cookie Size Issues**: Session data is no longer stored in browser cookies
2. **Enables Longer Contexts**: Model can now handle more complex conversations
3. **Generates More Detailed Responses**: Higher default token limits allow for richer output
4. **Better Error Handling**: Users receive feedback when issues occur
5. **Improved Session Management**: Sessions are properly saved and loaded with timings data

## Usage

After implementing these changes, users should:

1. Reinstall dependencies:
   ```bash
   pip install -r requirements_py310.txt
   ```

2. Restart the application:
   ```bash
   python app_chat.py
   ```

3. The enhanced capabilities will be available immediately:
   - Longer conversation history
   - More detailed responses by default
   - Proper session persistence
   - Better error reporting

## Future Considerations

1. **Session Cleanup**: The `cleanup_old_sessions()` function can be called periodically to remove old sessions and prevent disk space issues
2. **Further Context Enhancement**: The context window could be increased further (up to 8192 tokens) if needed
3. **Token Limit Adjustment**: The default token generation limit could be adjusted based on user feedback
