"""LiteLLM must use its bundled cost map on every tokview import path.

LiteLLM decides at first import whether to download the live cost map from
GitHub. tokview.logger imports LiteLLM at module load, so before the switch
moved into the package __init__, importing the logger first silently used the
live map: prices and model lookups drifted with whatever was on GitHub that day.
"""

import os
import subprocess
import sys


def _run(code: str) -> str:
    env = {k: v for k, v in os.environ.items() if k != "LITELLM_LOCAL_MODEL_COST_MAP"}
    out = subprocess.run(
        [sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True
    )
    return out.stdout.strip()


def test_importing_logger_first_pins_the_bundled_cost_map():
    code = "import os, tokview.logger\nprint(os.environ.get('LITELLM_LOCAL_MODEL_COST_MAP'))"
    assert _run(code) == "True"


def test_explicit_user_setting_is_respected():
    env = {**os.environ, "LITELLM_LOCAL_MODEL_COST_MAP": "False"}
    out = subprocess.run(
        [
            sys.executable,
            "-c",
            "import os, tokview; print(os.environ['LITELLM_LOCAL_MODEL_COST_MAP'])",
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert out.stdout.strip() == "False"
