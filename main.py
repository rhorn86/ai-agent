import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(client, messages, args):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("No usage object was returned in the response")

    message = response.choices[0].message

    if args.verbose:
        print("User prompt:")
        print(args.user_prompt)
        print(f"\nPrompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}\n")
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] == "":
                raise Exception("Error: tool message has an empty 'content' field")
            if args.verbose:
                print(f"-> {result_message['content']}")

    else:
        print("Response:")
        print(response.choices[0].message.content)

def main() -> None:

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("No API key was provided")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args)


if __name__ == "__main__":
    main()
