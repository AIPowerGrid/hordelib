# horde-engine

[![PyPI Version][pypi-image]][pypi-url]
[![Downloads][downloads-image]][downloads-url]
![GitHub license][license-url]

[![Build][build-image]][build-url]
[![Test Images][main-test-image]][main-test-url]
[![Test Images][pr-test-image]][pr-test-url]
[![All Models][all-model-images]][all-model-url]
[![Release Changelog][changelog-image]][changelog-url]

> Note: This project was formerly known as `hordelib`. The project namespace will be changed in the near future to reflect this change.

`horde-engine` is a wrapper around [ComfyUI](https://github.com/comfyanonymous/ComfyUI) primarily to enable the [AI Horde](https://aihorde.net/) to run inference pipelines designed visually in the ComfyUI GUI.

The developers of `horde-engine` can be found in the AI Horde Discord server: [https://discord.gg/3DxrhksKzn](https://discord.gg/3DxrhksKzn)

Note that `horde-engine` (previously known as `hordelib`) has been the default inference backend library of the [AI Horde](https://aihorde.net/) since `hordelib` v1.0.0.

## Purpose

The goal here is to be able to design inference pipelines in the excellent ComfyUI, and then call those inference pipelines programmatically. Whilst providing features that maintain compatibility with the existing horde implementation.

## Installation

If being installed from pypi, use a requirements file of the form:
```
--extra-index-url https://download.pytorch.org/whl/cu128
hordelib

...your other dependencies...
```

#### Linux Installation

On Linux you will need to install the Nvidia CUDA Toolkit. Linux installers are provided by Nvidia at https://developer.nvidia.com/cuda-downloads

Note if you only have 16GB of RAM and a default /tmp on tmpfs, you will likely need to increase the size of your temporary space to install the CUDA Toolkit or it may fail to extract the archive. One way to do that is just before installing the CUDA Toolkit:
```bash
sudo mount -o remount,size=16G /tmp
```
If you only have 16GB of RAM you will also need swap space. So if you typically run without swap, add some. You won't be able to run this library without it.

## Usage

Horde payloads can be processed simply with (for example):

```python
# import os
# Wherever your models are
# os.environ["AIWORKER_CACHE_HOME"] = "f:/ai/models" # Defaults to `models/` in the current working directory

import hordelib

hordelib.initialise()  # This must be called before any other hordelib functions

from hordelib.horde import HordeLib
from hordelib.shared_model_manager import SharedModelManager

generate = HordeLib()

if SharedModelManager.manager.compvis is None:
    raise Exception("Failed to load compvis model manager")

SharedModelManager.manager.compvis.download_model("Deliberate")
SharedModelManager.manager.compvis.validate_model("Deliberate")


data = {
    "sampler_name": "k_dpmpp_2m",
    "cfg_scale": 7.5,
    "denoising_strength": 1.0,
    "seed": 123456789,
    "height": 512,
    "width": 512,
    "karras": False,
    "tiling": False,
    "hires_fix": False,
    "clip_skip": 1,
    "control_type": None,
    "image_is_control": False,
    "return_control_map": False,
    "prompt": "an ancient llamia monster",
    "ddim_steps": 25,
    "n_iter": 1,
    "model": "Deliberate",
}
pil_image = generate.basic_inference_single_image(data).image

if pil_image is None:
    raise Exception("Failed to generate image")

pil_image.save("test.png")

```

Note that `hordelib.initialise()` will erase all command line arguments from argv. So make sure you parse them before you call that.

See `tests/run_*.py` for more standalone examples.

### Logging

If you don't want `hordelib` to setup and control the logging configuration (we use [loguru](https://loguru.readthedocs.io/en/stable/)) initialise with:

```python
import hordelib
hordelib.initialise(setup_logging=False)
```

## Acknowledgments

`hordelib` depends on a large number of open source projects, and most of these dependencies are automatically downloaded and installed when you install `hordelib`. Due to the nature and purpose of `hordelib` some dependencies are bundled directly _inside_ `hordelib` itself.

### [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
A powerful and modular stable diffusion GUI with a graph/nodes interface. Licensed under the terms of the GNU General Public License v3.0.

The entire purpose of `hordelib` is to access the power of ComfyUI.

### [Controlnet Preprocessors for ComfyUI](https://github.com/Fannovel16/comfy_controlnet_preprocessors)
Custom nodes for ComfyUI providing Controlnet preprocessing capability. Licened under the terms of the Apache License 2.0.

### [ComfyUI Face Restore Node](https://civitai.com/models/24690/comfyui-facerestore-node)

Custom nodes for ComfyUI providing face restoration.

### [ComfyQR](https://gitlab.com/sofuego-comfy-nodes/ComfyQR)

Nodes for generating QR codes

## Development

Requirements:
- `git` (install git)
- `tox` (`pip install tox`)
- Set the environmental variable `AIWORKER_CACHE_HOME` to point to a model directory.

Note the model directory must currently be in the original AI Horde directory structure:
```
<AIWORKER_CACHE_HOME>\
    clip\
    codeformer\
    compvis\
        Deliberate.ckpt
        ...etc...
    controlnet\
    embeds\
    esrgan\
    gfpgan\
    safety_checker\
```

### Running the Tests

Simply execute: `tox` (or `tox -q` for less noisy output)

This will take a while the first time as it installs all the dependencies.

If the tests run successfully images will be produced in the `images/` folder.

#### Running a specific test file

`tox -- -k <filename>` for example `tox -- -k test_initialisation`

#### Running a specific predefined test suite

`tox list`

This will list all groups of tests which are involved in either the development, build or CI proccess. Tests which have the word 'fix' in them will automatically apply changes when run, such as to linting or formatting. You can do this by running:

`tox -e [test_suite_name_here]`

### Directory Structure

`hordelib/pipeline_designs/`
Contains ComfyUI pipelines in a format that can be opened by the ComfyUI web app. These saved directly from the web app.

`hordelib/pipelines/`
Contains the above pipeline JSON files converted to the format required by the backend pipeline processor. These are converted from the web app, see _Converting ComfyUI pipelines_ below.

`hordelib/nodes/` These are the custom ComfyUI nodes we use for `hordelib` specific processing.

### Running ComfyUI Web Application

In this example we install the dependencies in the OS default environment. When using the git version of `hordelib`, from the project root:

`pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu128 --upgrade`

Ensure ComfyUI is installed, one way is running the tests:

`tox -- -k test_comfy_install`

From then on to run ComfyUI:

`cd ComfyUI`
`python main.py`

Then open a browser at: http://127.0.0.1:8188/

### Designing ComfyUI Pipelines

Use the standard ComfyUI web app. Use the "title" attribute to name the nodes, these names become parameter names in the `hordelib`. For example, a KSampler with the "title" of "sampler2" would become a parameter `sampler2.seed`, `sampler2.cfg`, etc. Load the pipeline `hordelib/pipeline_designs/pipeline_stable_diffusion.json` in the ComfyUI web app for an example.

Save any new pipeline in `hordelib/pipeline_designs` using the naming convention "pipeline_\<name\>.json".

Convert the JSON for the model (see _Converting ComfyUI pipelines_ below) and save the resulting JSON in `hordelib/pipelines` using the same filename as the previous JSON file.

That is all. This can then be called from `hordelib` using the `run_image_pipeline()` method in `hordelib.comfy.Comfy()`

### Converting ComfyUI pipelines

In addition to the design file saved from the UI, we need to save the pipeline file in the backend format. This file is created in the `hordelib` project root named `comfy-prompt.json` automatically if you run a pipeline through the ComfyUI version embedded in `hordelib`. Running ComfyUI with `tox -e comfyui` automatically patches ComfyUI so this JSON file is saved.

### Build Configuration

The main config files for the project are: `pyproject.toml`, `tox.ini` and `requirements.txt`

### PyPi Publishing

Pypi publishing is automatic all from the GitHub website.

1. Create a PR from `main` to `releases`
1. Label the PR with "release:patch" (0.0.1) or "release:minor" (0.1.0)
1. Merge the PR with a standard merge commit (not squash)


### Standalone "clean" environment test from Pypi

Here's an example:

Start in a new empty directory. Create requirements.txt:
```
--extra-index-url https://download.pytorch.org/whl/cu128
hordelib
```

Create the directory `images/` and copy the `test_db0.jpg` into it.

Copy `run_controlnet.py` from the `hordelib/tests/` directory.

Build a venv:
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Run the test we copied:
```
python run_controlnet.py

The `images/` directory should have our test images.
```

### Creating a local build of hordelib

This is useful when testing new nodes  via the horde-reGen-worker etc

```bash
python build_helper.py
python -m build --sdist --wheel --outdir dist/ .
python build_helper.py --fix
```

On the venv where you want to install th new version

```bash
python -m pip install /path/to/hordelib/dist/horde_engine-*.whl
```

### Updating the embedded version of ComfyUI

- Change the value in `consts.py` to the desired ComfyUI version.
- Run the test suite via `tox`



<!-- Badges: -->

[pypi-image]: https://badge.fury.io/py/hordelib.svg?branch=main&kill_cache=1
[pypi-url]: https://badge.fury.io/py/horde-engine
[downloads-image]: https://pepy.tech/badge/horde-engine
[downloads-url]: https://pepy.tech/project/horde-engine
[license-url]: https://img.shields.io/github/license/Haidra-Org/hordelib
[build-image]: https://github.com/Haidra-Org/hordelib/actions/workflows/maintests.yml/badge.svg?branch=main
[all-model-images]: https://badgen.net/badge/all-models/images/blue?icon=awesome
[build-url]: https://tests.hordelib.org/
[main-test-image]: https://badgen.net/badge/main/latest-images/blue?icon=awesome
[main-test-url]: https://tests.hordelib.org/
[pr-test-image]: https://badgen.net/badge/develop/latest-images/blue?icon=awesome
[pr-test-url]: https://tests.hordelib.org/unstable/index.html
[all-model-url]: https://tests.hordelib.org/all_models/
[changelog-image]: https://img.shields.io/badge/Release-Changelog-yellow
[changelog-url]: https://github.com/Haidra-Org/hordelib/blob/releases/CHANGELOG.md
