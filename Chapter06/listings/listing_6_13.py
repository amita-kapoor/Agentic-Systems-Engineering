# Listing 6.13 is the chapter's shared prelude. The imports below are used by
# the listings that follow rather than by this file, so F401 is suppressed
# here. Removing them breaks every later listing when the chapter is run in
# order.
import hashlib  # noqa: F401
import json  # noqa: F401
import os
import time  # noqa: F401
from dataclasses import dataclass, field  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, Callable, Literal, Optional, TypedDict  # noqa: F401

from pydantic import BaseModel, Field  # noqa: F401

# Set your API key here, or leave it as an empty string to use the mock client.
try:
    # In case you are running it on Google Colab. The import lives inside the
    # try so the listing still runs outside Colab, where google.colab is absent.
    from google.colab import userdata

    OPENAI_API_KEY = userdata.get("OPENAI_API_KEY")
except Exception:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

USE_REAL_LLM = bool(OPENAI_API_KEY)
print(f"Using real LLM: {USE_REAL_LLM}")
