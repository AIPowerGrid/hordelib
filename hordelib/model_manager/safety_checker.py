import typing

import torch
from diffusers.pipelines.stable_diffusion.safety_checker import (
    StableDiffusionSafetyChecker,
)
from loguru import logger
from typing_extensions import override

from hordelib.consts import MODEL_CATEGORY_NAMES, MODEL_DB_NAMES
from hordelib.model_manager.base import BaseModelManager


class SafetyCheckerModelManager(BaseModelManager):  # FIXME # TODO?
    def __init__(self, download_reference=False):
        super().__init__(
            model_category_name=MODEL_CATEGORY_NAMES.safety_checker,
            download_reference=download_reference,
        )
