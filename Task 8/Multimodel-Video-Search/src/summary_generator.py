from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

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

        
    prompt = f"""
You are an AI assistant that understands videos.

Below is the transcript of the video.

Transcript
----------
{transcript}

Visual Scene Information
------------------------
{scene_context}

Task
----

You are an expert at understanding and summarizing educational videos.

You are given two inputs:

1. Transcript
   - This is the primary source of information.
   - It contains the spoken content of the video.

2. Scene Descriptions
   - These describe the visual content of keyframes.
   - Use them only to provide visual context when they add useful information.

Instructions

1. Use the transcript as the primary source of information.
2. Use scene descriptions only when they improve the understanding of the content.
3. Focus on what the speaker is explaining, teaching, or discussing.
4. Do not repeatedly describe the speaker, audience, podium, or camera angle unless it is important to the content.
5. Generate a concise but informative summary.
6. Divide the video into meaningful chapters based on topic changes, not simply scene changes.
7. Each chapter should have:
   - title
   - start_time (in seconds)
   - short description

Return ONLY valid JSON in the following format:

{
    "summary": "...",
    "chapters": [
        {
            "title": "...",
            "start_time": 0.0,
            "description": "..."
        }
    ]
}
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

    return output

