from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict


class SourceConfig(BaseModel):
    name: str
    url: HttpUrl
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, str]] = None


class IngestRequest(BaseModel):
    sources: List[SourceConfig]