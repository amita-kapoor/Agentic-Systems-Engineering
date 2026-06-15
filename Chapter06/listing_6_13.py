import os
import json
import time
import hashlib
from typing import Any, Callable, Literal, Optional, TypedDict
from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel, Field
from google.colab import userdata  #A

try:  # B
    OPENAI_API_KEY = userdata.get("OPENAI_API_KEY")
except Exception:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

USE_REAL_LLM = bool(OPENAI_API_KEY)
print(f"Using real LLM: {USE_REAL_LLM}")
