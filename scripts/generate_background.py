import torch
from modelscope import FluxPipeline
import os

pipe = FluxPipeline.from_pretrained("/FLUX.1-dev", torch_dtype=torch.bfloat16)

pipe = pipe.to("cuda")
save_dir = "../results/backgrounds/"
os.makedirs(save_dir, exist_ok=True)
prompt = "A beautiful modern snowy landscape, with a city view at the center of the composition. "
negative_prompt = "oil painting, digital art, illustration, sketch, drawing, cartoon, stylized, canvas, brush strokes"

num_images = 4  
result = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    height=1600,
    width=1200,
    guidance_scale=5,
    num_inference_steps=50,
    max_sequence_length=512,
    num_images_per_prompt=num_images,  
    generator=torch.Generator("cuda").manual_seed(0)
)

for i, image in enumerate(result.images):
    image.save(save_dir + f"flux_{i+1}.png")
    print(f"save {i+1}/{num_images}: {save_dir}flux_{i+1}.png")