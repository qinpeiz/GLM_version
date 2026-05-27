---
name: glm-vision
description: Use GLM-4.6V multimodal model for image recognition. Call when user provides an image and asks what's in it, or needs visual analysis of any image.
---

# GLM Vision

Bridge to GLM-4.6V multimodal model via `glm_vision.py` for image understanding tasks.

## When to use

- User provides a local image path (e.g., `photo.jpg`, `screenshot.png`) and asks what's in it
- User provides an image URL and asks for visual analysis
- User asks about image content without specifying a model — default to this
- User needs object detection, grounding coordinates, OCR, or scene description from an image
- User pastes a screenshot and asks a question about it

## Workflow

### 1. Detect image and intent

The user may provide:
- A bare filename: `23.jpg` → assume it's in the project root
- An absolute path: `C:\Users\...\image.png`
- A URL: `https://example.com/photo.png`
- No explicit prompt means "describe this image in detail"

### 2. Build prompt

- If the user asks a specific question, use it verbatim as the prompt
- If the user just sends an image with no question, use: `"详细描述这张图片的内容"`
- If the task is grounding/localization, prompt for coordinates: `"Where is X? Provide [[xmin,ymin,xmax,ymax]] format"`
- If the task is OCR, prompt for text extraction

### 3. Call GLM

```bash
cd "<project_root>" && python glm_vision.py "<image_path_or_url>" "<prompt>"
```

- Encoding is handled internally (UTF-8), no extra flags needed
- Timeout: 120 seconds (GLM thinking mode can take time)
- The script auto-converts local images to base64, URLs pass through directly

### 4. Relay results

- Present GLM's response clearly to the user
- If coordinates are returned, format them in a readable way
- If the image is unrecognizable, report honestly
- Do not fabricate visual details beyond what GLM returns

## Script reference

`glm_vision.py` accepts:
```
python glm_vision.py <image_url_or_path> [prompt]
```

Arguments:
- `image_url_or_path`: URL or local file path (local files auto-encoded to base64)
- `prompt`: text question (defaults to general description prompt)
- Image format support: PNG, JPG, JPEG, GIF, WEBP, BMP
- Environment variable `GLM_API_KEY` can override the built-in key
