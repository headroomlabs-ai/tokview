"""tokview: drop-in LLM proxy + dashboard for exact token cost tracking."""

import os

# Use the cost map bundled in the pinned LiteLLM wheel, never the live copy on
# GitHub. LiteLLM reads this switch once, when it is first imported, and some
# modules (tokview.logger) import it at load time. Setting it here, before any
# submodule loads, covers every entry point, not only the proxy server.
# See the SECURITY note in tokview.server for why the live fetch is refused.
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")

__version__ = "0.0.7"
__all__ = ["__version__"]
