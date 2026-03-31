from google import genai

API_KEY = "YOUR API KEY BRO"

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-2.5-flash"

print("Gemini Chat started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye 👋")
        break

    response = client.models.generate_content(
        model=MODEL,
        contents=user_input
    )

    print("Gemini:", response.text, "\n")



