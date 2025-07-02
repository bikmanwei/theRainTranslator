


          
# Rain Translator

A creative web application that converts user input characters into rain-themed poetry using the ChatGPT API. Transform random character strings into imaginative rain-themed poems.

## Project Overview

Rain Translator is a creative text processing tool that can:
- Accept user input of up to 15 characters
- Convert characters into rain-themed poetry through ChatGPT API
- Provide real-time progress bar display
- Support auto-submission (at 15 characters) or manual submission (Enter key)
- Display conversion history

## Quick Start Guide

### 1. Environment Setup

Ensure your system has:
- Python 3.7+
- pip (Python package manager)

### 2. Get OpenAI API Key

1. Visit [OpenAI Official Website](https://platform.openai.com/)
2. Register and log into your account
3. Obtain your API key

### 3. Project Configuration

1. **Clone or download the project locally**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root directory and add the following:
   ```
   OPENAI_API_KEY=your_OpenAI_API_key
   PROMPT_TEXT=your_custom_prompt_text (optional, has default value)
   ```

### 4. Start the Service

Run in the project root directory:
```bash
python theRainTranslator.py
```

Seeing the following information indicates successful startup:
```
🌧️ 雨滴翻译器启动中...
✅ ChatGPT客户端初始化成功
🚀 服务器启动在 http://localhost:5001
```

### 5. Using the Web Interface

1. **Open your browser** and visit: `http://localhost:5001`

2. **Usage**:
   - Enter up to 15 characters in the left input box
   - Method 1: Auto-submit after entering 15 characters
   - Method 2: Enter any characters and press Enter to submit
   - The right side will display the conversion process and results

3. **Features**:
   - Real-time character count and progress bar
   - Loading animation during conversion
   - Auto-save of the last 10 conversion records
   - Each record shows input content, conversion result, and timestamp

## Troubleshooting

### Common Issues

1. **Service startup failure**
   - Check if Python version is 3.7+
   - Confirm all dependencies are installed: `pip install -r requirements.txt`

2. **API call failure**
   - Check if `OPENAI_API_KEY` in `.env` file is correct
   - Confirm OpenAI account has sufficient API quota
   - Check if network connection is normal

3. **Web page inaccessible**
   - Confirm service has started successfully
   - Check if port 5001 is occupied
   - Try accessing: `http://127.0.0.1:5001`

### Health Check

Visit `http://localhost:5001/api/health` to check service status

## Technical Architecture

- **Frontend**: HTML + CSS + JavaScript
- **Backend**: Python Flask
- **AI Service**: OpenAI ChatGPT API
- **Main Files**:
  - `index.html` - Web interface
  - `script.js` - Frontend interaction logic
  - `style.css` - Style file
  - `theRainTranslator.py` - Backend service
  - `ChatGPT_SDK.py` - ChatGPT API wrapper
  - `get_prompt.py` - Prompt management
        