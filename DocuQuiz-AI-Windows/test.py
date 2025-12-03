# from openai import OpenAI
# from config import *

# client = OpenAI(api_key=api_key_)

# prompt = """
# Output a Blooket CSV for 10 math questions.
# Columns: Question #,Question Text,Answer 1,Answer 2,Answer 3 (Optional),Answer 4 (Optional),Time Limit (sec),Correct Answer(s)
# Time Limit: 20
# Output ONLY CSV rows, no explanations or code blocks.
# """

# response = client.chat.completions.create(
#     model="gpt-4",
#     messages=[{"role": "user", "content": prompt}]
# )

# csv_text = response.choices[0].message.content

# with open("blooket_quiz.csv", "w", encoding="utf-8") as f:
#     f.write(csv_text)


from PIL import Image

img = Image.open("logo\docuquiz_logo.png").convert("RGB")
img.save("output.pdf")