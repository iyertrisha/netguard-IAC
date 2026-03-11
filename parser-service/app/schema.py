from typing import List, Dict
from pydantic import BaseModel

class Rule(BaseModel):
    port: str
    protocol: str
    cidr: str

class Resource(BaseModel):
    resource_id: str
    resource_type: str
    provider: str
    properties: Dict
    inbound_rules: List[Rule] = []
    outbound_rules: List[Rule] = []
    tags: Dict = {}