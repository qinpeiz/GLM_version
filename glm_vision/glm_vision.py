#!/usr/bin/env python3
"""GLM-4.6V vision bridge — call GLM multimodal model for image recognition."""

import requests
import sys
import json
import os

# Fix encoding on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

API_KEY = os.environ.get("GLM_API_KEY", "请在此处输入您的API key") #!!!请在此处输入您的API key!!!
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "glm-4.6v"


def call_vision(image_url: str, prompt: str, thinking: bool = False) -> str:
    content = []
    if image_url:
        # If it's a local file path, read and convert to base64
        if not image_url.startswith("http://") and not image_url.startswith("https://"):
            import base64
            import mimetypes
            mime_type = mimetypes.guess_type(image_url)[0] or "image/png"
            with open(image_url, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{b64}"}
            })
        else:
            content.append({
                "type": "image_url",
                "image_url": {"url": image_url}
            })

    content.append({"type": "text", "text": prompt})

    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
    }
    if thinking:
        body["thinking"] = {"type": "enabled"}

    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python glm_vision.py <image_url_or_path> [prompt] [--thinking]")
        print("  image_url_or_path: URL or local file path to the image")
        print("  prompt: text prompt (default: 'Describe this image in detail.')")
        print("  --thinking: enable thinking mode")
        sys.exit(1)

    image = sys.argv[1]
    prompt = "Describe this image in detail."
    thinking = False

    for arg in sys.argv[2:]:
        if arg == "--thinking":
            thinking = True
        else:
            prompt = arg

    result = call_vision(image, prompt, thinking)
    print(result)
