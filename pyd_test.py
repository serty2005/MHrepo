import json
import os
from typing import Optional,List
from pydantic import BaseModel, Field

class Equipment(BaseModel):
    uuid: str = Field(alias='UUID')
    title: str
    metaclass: str = Field(alias='metaClass')
    
class InChain(BaseModel):
    uuid: str = Field(alias='UUID')
    title: str

class Company(BaseModel):
    uuid: str = Field(alias='UUID')
    title: str
    equip: List[Equipment] | None = Field(alias='KEsInUse')
    lastmodify: str = Field(alias='lastModifiedDate')
    ourchild: List['Company'] | None = Field(alias='childOUs')
    additionalName: str | None = None

with open('oucompany.json') as f:
    # datax = json.loads(f)
    m = Company.model_validate_json(json_data=f)

# m = Company.model_validate_json(datax)
# dataobject = Company(**datax)
print(type(m))