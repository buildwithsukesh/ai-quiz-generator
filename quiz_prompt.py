from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

topic = "photosynthesis"

prompt = f"""
Create 5 multiple-choice questions on {topic}.

Rules:
- Each question has 4 options labeled A, B, C and D.
- Only one option is correct.
- After each question, write: Answer: <letter>
- Make the questions suitable for a first-year college student.
"""

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)