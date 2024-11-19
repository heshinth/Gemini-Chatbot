import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner


def main():
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY is not set.")
        sys.exit(1)

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        chat = model.start_chat(history=[])
    except Exception as e:
        print(f"Error initializing GenerativeModel: {e}")
        sys.exit(1)

    history = []
    console = Console()

    try:
        while True:
            prompt = input("Ask me anything: ")
            if prompt.lower() == "exit":
                break
            if not prompt.strip():
                print("Input cannot be empty. Please try again.")
                continue
            history.append({"role": "user", "content": prompt})

            with console.status("[bold green]Loading..."):
                response = chat.send_message(prompt, stream=True)
                response_text = ""
                for chunk in response:
                    if chunk.text:
                        response_text += chunk.text

            history.append({"role": "assistant", "content": response_text})
            console.print(Markdown(response_text))
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error during chat: {e}")


if __name__ == "__main__":
    main()
