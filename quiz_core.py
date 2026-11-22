import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

MODEL = "gemini-3.5-flash-lite"
LETTERS = ["A", "B", "C", "D"]


def build_prompt(topic, count, difficulty):
    return f"""
Create {count} multiple-choice questions on {topic}
at {difficulty} difficulty, for a first-year college student.

Return a JSON list. Each item must be an object with these keys:
- "question": the question text
- "options": a list of exactly 4 option texts (without A/B/C/D labels)
- "answer": the letter of the correct option, one of "A", "B", "C", "D"
- "explanation": one sentence explaining the correct answer

Rules:
- Only one option is correct.
- The wrong options must be believable, not silly.
"""


def is_valid(quiz):
    """Check that the quiz has the structure our code expects."""
    if not isinstance(quiz, list) or len(quiz) == 0:
        return False
    for item in quiz:
        if not isinstance(item, dict):
            return False
        for key in ("question", "options", "answer", "explanation"):
            if key not in item:
                return False
        if not isinstance(item["options"], list) or len(item["options"]) != 4:
            return False
        if str(item["answer"]).strip().upper() not in LETTERS:
            return False
    return True


def generate_quiz(topic, count=5, difficulty="medium", attempts=3):
    """Ask Gemini for a quiz. Retry if something goes wrong."""
    prompt = build_prompt(topic, count, difficulty)
    last_error = ""

    for attempt in range(1, attempts + 1):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            quiz = json.loads(response.text)
            if is_valid(quiz):
                return quiz
            last_error = "The AI returned the quiz in the wrong format."
        except json.JSONDecodeError:
            last_error = "The AI returned invalid JSON."
        except Exception as error:
            last_error = f"API problem: {error}"

        if attempt < attempts:
            time.sleep(3 * attempt)  # wait a little longer each time

    raise RuntimeError(
        f"Could not create the quiz after {attempts} tries. {last_error}"
    )