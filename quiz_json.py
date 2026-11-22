import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

# 1. Ask the user
topic = input("Enter a topic: ").strip()

try:
    count = int(input("How many questions (1-10)? "))
except ValueError:
    print("That was not a number, so I will use 5.")
    count = 5

if count < 1 or count > 10:
    print("Number out of range, so I will use 5.")
    count = 5

# 2. Build the prompt, describing the exact JSON we want
prompt = f"""
Create {count} multiple-choice questions on {topic}.

Return a JSON list. Each item must be an object with these keys:
- "question": the question text
- "options": a list of exactly 4 option texts (without A/B/C/D labels)
- "answer": the letter of the correct option, one of "A", "B", "C", "D"

Rules:
- Only one option is correct.
- Make the questions suitable for a first-year college student.
"""

# 3. Send it, asking for JSON output
print("\nGenerating your quiz...\n")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

# 4. Turn the JSON text into Python data
quiz = json.loads(response.text)

# 5. Show it neatly, reading each part separately
letters = ["A", "B", "C", "D"]

for number, item in enumerate(quiz, start=1):
    print(f"Q{number}. {item['question']}")
    for letter, option in zip(letters, item["options"]):
        print(f"   {letter}. {option}")
    print(f"   Correct answer: {item['answer']}\n")