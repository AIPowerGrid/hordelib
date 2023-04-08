# This tests running hordelib standalone, as an external caller would use it.
# Call with: python -m test.run_img2img_hires
# You need all the deps in whatever environment you are running this.
import os

import hordelib

hordelib.initialise()

from PIL import Image

from hordelib.horde import HordeLib
from hordelib.shared_model_manager import SharedModelManager

generate = HordeLib()
SharedModelManager.loadModelManagers(compvis=True)
SharedModelManager.manager.load("Deliberate")

data = {
    "sampler_name": "k_dpmpp_2m",
    "cfg_scale": 7.5,
    "denoising_strength": 0.3,
    "seed": 250636385744582,
    "height": 1024,
    "width": 1024,
    "karras": False,
    "tiling": False,
    "hires_fix": True,
    "clip_skip": 1,
    "control_type": "canny",
    "image_is_control": False,
    "return_control_map": False,
    "prompt": "a dinosaur",
    "ddim_steps": 25,
    "n_iter": 1,
    "model": "Deliberate",
    "source_image": Image.open("images/horde_text_to_image.png"),
}
pil_image = generate.text_to_image(data)
pil_image.save("images/test.png")
