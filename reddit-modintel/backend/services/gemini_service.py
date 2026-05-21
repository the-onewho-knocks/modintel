import os
import google.generativeai as genai


def generate_tldr(text: str) -> dict:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

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
    resp = model.generate_content(prompt)
    raw = resp.text.strip()

    lines = raw.split("\n")
    one_liner = ""
    bullets = []
    tone = ""

    for line in lines:
        if line.lower().startswith("one-liner"):
            one_liner = line.split(":", 1)[1].strip()
        elif line.startswith("-"):
            bullets.append(line.lstrip("- ").strip())
        elif line.lower().startswith("tone"):
            tone = line.split(":", 1)[1].strip()

    return {"one_liner": one_liner, "bullets": bullets[:3], "tone": tone}