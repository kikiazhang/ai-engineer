import time

from google import genai
from google.genai import errors

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_response(prompt: str) -> str:
    client = genai.Client()

    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    latency = time.perf_counter() - start_time

    print(f"The latency is {latency:.3f} seconds")
    print(f"The usage metadata is {response.usage_metadata}")

    return response.text


def main():
    try:
        response_text = generate_response(
            "Explain what a software license is in one sentence."
        )

        print(f"Response: {response_text}")
    except errors.APIError as error:
        if error.code == 400:  # fail fast
            print(
                "400 Bad Request: The request is invalid. "
                "Check the prompt, model, or request configuration."
            )

        elif error.code in (401, 403):  # fail fast
            print(
                f"{error.code} Authentication/Permission Error: "
                "Check the API key and permissions."
            )

        elif error.code == 404:  # fail fast
            print("404 Not Found: The requested model or resource could not be found.")

        elif error.code == 429:  # inspect before retry
            print(
                "429 Rate Limit/Quota Error: The request was rejected "
                "because of a rate limit or quota issue. "
                "Do not blindly retry until we know which one."
            )

        elif error.code == 503:  # potentially retry
            print(
                "503 Service Unavailable: The model provider is temporarily "
                "unavailable or overloaded. This may be retryable."
            )

        elif error.code in (500, 502, 504):  # potentially retry
            print(
                f"{error.code} Server Error: The provider encountered "
                "a temporary server-side failure. This may be retryable."
            )

        else:
            print(f"LLM API Error {error.code}: {error.message or 'Unknown API error'}")


if __name__ == "__main__":
    main()
