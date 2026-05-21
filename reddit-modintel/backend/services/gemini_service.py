import os
from google import genai


def generate_tldr(text: str) -> dict:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""Summarize the following Reddit post.

Return your answer in this exact format:

One-liner: <one sentence summary>
Bullets:
- <bullet 1>
- <bullet 2>
- <bullet 3>
Tone: <overall tone>

Post:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    lines = raw.split("\n")
    one_liner = ""
    bullets = []
    tone = ""

    for line in lines:
        if line.lower().startswith("one-liner"):
            one_liner = line.split(":", 1)[1].strip()

        elif line.startswith("-"):
            bullets.append(
                line.lstrip("- ").strip()
            )

        elif line.lower().startswith("tone"):
            tone = line.split(":", 1)[1].strip()

    return {
        "one_liner": one_liner,
        "bullets": bullets[:3],
        "tone": tone
    }