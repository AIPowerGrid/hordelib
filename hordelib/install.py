# install.py
# Fetch a specific version of the upstream ComfyUI project
import os
import subprocess
from loguru import logger


class Installer:
    def __init__(self):
        self.ourdir = os.path.dirname(os.path.realpath(__file__))

    def get_commit_hash(self):
        head_file = os.path.join(self.ourdir, "ComfyUI", ".git", "HEAD")
        if not os.path.exists(head_file):
            return "NOT FOUND"
        try:
            with open(head_file, "r") as f:
                head_contents = f.read().strip()

            if not head_contents.startswith("ref:"):
                return head_contents

            ref_path = os.path.join(".git", *head_contents[5:].split("/"))

            with open(ref_path, "r") as f:
                commit_hash = f.read().strip()

            return commit_hash
        except Exception:
            return ""

    def _run(self, command, subdir=None):
        if not subdir:
            directory = self.ourdir
        else:
            directory = os.path.join(self.ourdir, subdir)
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, cwd=directory
        )
        if result.returncode:
            logger.error(result.stderr)
            return

    def install(self, comfy_version):

        # Install if ComfyUI is missing completely
        if not os.path.exists(f"{self.ourdir}/ComfyUI"):
            self._run("git clone https://github.com/comfyanonymous/ComfyUI.git")
            self._run(f"git checkout {comfy_version}", "ComfyUI")
            return

        # If it's installed, is it up to date?
        version = self.get_commit_hash()
        if version == comfy_version:
            # Yes, all done
            return

        # Update comfyui
        logger.info(
            f"Current ComfyUI version {version[:8]} requires {comfy_version[:8]}"
        )
        self._run(f"git checkout {comfy_version}", "ComfyUI")
