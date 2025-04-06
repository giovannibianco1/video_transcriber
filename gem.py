from openai import OpenAI


def chat(messages):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        extra_body={},
        model="google/gemini-2.0-flash-001",
        messages=messages
    )
    return completion.choices[0].message.content
