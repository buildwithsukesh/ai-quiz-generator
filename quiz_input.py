from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

# 1. Ask the user for the topic
topic = input("Enter a topic: ").strip()

# 2. Ask for the number of questions (and check it is a valid number)
try:
    count = int(input("How many questions (1-10)? "))
except ValueError:
    print("That was not a number, so I will use 5.")
    count = 5

if count < 1 or count > 10:
    print("Number out of range, so I will use 5.")
    count = 5

# 3. Build the prompt using the user's answers
prompt = f"""
Create {count} multiple-choice questions on {topic}.

Rules:
- Each question has 4 options labeled A, B, C and D.
- Only one option is correct.
- After each question, write: Answer: <letter>
- Make the questions suitable for a first-year college student.
"""

# 4. Send it to Gemini and show the result
print("\nGenerating your quiz...\n")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

print(response.text)