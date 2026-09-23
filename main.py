import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
from openai.types.chat import ChatCompletion

def call_model(client: OpenAI, messages: list) -> ChatCompletion:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    return response

def generate_content(response: ChatCompletion, messages: list, verbose: bool) -> bool:

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens if response.usage else "Unkown")
        print("Response tokens:", response.usage.completion_tokens if response.usage else "Unkown")

    message = response.choices[0].message
    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return False

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")
        messages.append(result_message)
        if verbose:
            print(f"-> {result_message['content']}")
    return True

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        response = call_model(client, messages)
        message = response.choices[0].message
        messages.append(message)
        if not generate_content(response, messages, args.verbose):
            break
    else:
        print("Error: Maximium number of iterations occurred with no response")
        exit(1)


if __name__ == "__main__":
    main()
