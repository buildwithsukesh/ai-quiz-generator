# AI Quiz Generator

A web app that creates multiple-choice quizzes on any topic using the Google Gemini API.

## Features
- Type any topic and get a quiz in seconds
- Choose the number of questions (1-10) and the difficulty
- Instant scoring with a short explanation for every answer
- Validates the AI's output and retries automatically if the API is busy

## Setup
1. Get a free API key from https://aistudio.google.com/apikey
2. Create a file named `.env` in the project folder containing:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Install the requirements:
   ```
   pip3 install -r requirements.txt
   ```
4. Run the app:
   ```
   python3 -m streamlit run app.py
   ```

## How it works
- `quiz_core.py` sends a prompt to Gemini, asks for JSON, validates it, and retries on errors.
- `app.py` is the Streamlit web page that shows the quiz and marks the answers.

## Tech
Python, Streamlit, Google Gemini API