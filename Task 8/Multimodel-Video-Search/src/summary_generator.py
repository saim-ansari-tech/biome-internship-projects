import re
import torch
import json
from transformers import AutoProcessor, AutoModelForImageTextToText


MODEL_NAME = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"

processor = AutoProcessor.from_pretrained(MODEL_NAME)

model = AutoModelForImageTextToText.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
    device_map="auto",
    attn_implementation="eager"
)


def generate_summary(transcript: str, scenes_metadata: list):
    scene_context = ""
    for scene in scenes_metadata:
        scene_context += (
            f"Scene {scene['scene_id']}\n"
            f"Timestamp: {scene['timestamp']:.2f} seconds\n"
            f"Description: {scene['description']}\n\n"
        )

    prompt = f"""You are an AI assistant that
understands videos.

Below is the transcript of the video.

Transcript
----------
{transcript}

Visual Scene Information
------------------------
{scene_context}

Task
----

You are an expert at understanding and
summarizing educational videos.

You are given two inputs:

1. Transcript
   - This is the primary source of information.
   - It contains the spoken content of the video.

2. Scene Descriptions
   - These describe the visual content of keyframes.
   - Use them only to provide visual context when
   they add useful information.

Instructions

1. Use the transcript as the primary source of information.
2. Use scene descriptions only when they improve the
understanding of the content.
3. Focus on what the speaker is explaining, teaching,
or discussing.
4. Do not repeatedly describe the speaker, audience,
podium, or camera angle unless it is important to the content.
5. Generate a concise but informative summary.
6. Divide the video into meaningful chapters based
on topic changes, not simply scene changes.
7. Each chapter should have:
   - title
   - start_time (in seconds)
   - short description

Return ONLY valid JSON in the following format:

{{
    "summary": "...",
    "chapters": [
        {{
            "title": "...",
            "start_time": 0.0,
            "description": "..."
        }}
    ]
}}
"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    generated_ids = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False
    )

    output = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    json_match = re.search(r'\{[\s\S]*\}', output)

    if json_match:
        json_str = json_match.group(0)
        try:
            parsed = json.loads(json_str)
            if "summary" in parsed and "chapters" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass
    try:
        start_idx = output.find('{')
        end_idx = output.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = output[start_idx:end_idx+1]
            parsed = json.loads(json_str)
            if "summary" in parsed and "chapters" in parsed:
                return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    print(
        "Warning: VLM did not return valid JSON."
        "Attempting to extract content."
    )
    summary_match = re.search(r'"summary"\s*:\s*"([^"]+)"', output)
    summary = summary_match.group(1) if summary_match else output[:500]

    chapters = []
    chapter_matches = re.findall(
        r'"title"\s*:\s*"([^"]+)"[\s\S]*?"start_time"\s*:\s*([\d.]+)'
        r'[\s\S]*?"description"\s*:\s*"([^"]+)"',
        output
    )
    for match in chapter_matches:
        chapters.append({
            "title": match[0],
            "start_time": float(match[1]),
            "description": match[2]
        })

    if not chapters:
        chapters = [{
            "title": "Full Video",
            "start_time": 0.0,
            "description": "Complete video content"
        }]

    return {
        "summary": summary,
        "chapters": chapters
    }
