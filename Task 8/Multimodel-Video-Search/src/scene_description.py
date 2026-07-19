from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

from frames_extractor import extract_frames

MODEL_NAME = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"

processor = AutoProcessor.from_pretrained(MODEL_NAME)

model = AutoModelForImageTextToText.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
    device_map="auto",
    attn_implementation="eager"
)

def generate_scene_description(frames_metadata: list):
    results = []

    for frame in frames_metadata:
        image = Image.open(frame["image_path"])

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image
                    },
                    {
                        "type": "text",
                        "text": (
                            "Describe this video scene.\n"
                            "Focus on:\n"
                            "- People\n"
                            "- Objects\n"
                            "- Actions\n"
                            "- Environment\n"
                            "- Visible text\n"
                            "Keep the description concise."
                        )
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
            max_new_tokens=128,
            do_sample=False
        )

        description = processor.batch_decode(
            generated_ids,
            skip_special_tokens=True
        )[0]

        description = description.split("Assistant:")[-1].strip()

        scene_info = frame.copy()
        scene_info["description"] = description

        results.append(scene_info)

    return results


