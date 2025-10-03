# models.py
from pydantic import BaseModel, Field
from typing import Optional, Any
import json
import datetime

class TelemetryIn(BaseModel):
    device_id: str
    ts: str  # ISO timestamp or epoch string; we store as text
    temp: float
    lat: Optional[float] = None
    lon: Optional[float] = None
    raw: Optional[Any] = None

class TelemetryOut(BaseModel):
    id: int
    device_id: str
    ts: str
    temp: float
    lat: Optional[float] = None
    lon: Optional[float] = None
    raw: Optional[Any] = None