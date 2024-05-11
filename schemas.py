from pydantic import BaseModel,ConfigDict
from datetime import datetime

class CompanyModel(BaseModel):
    id : str
    title : str


    model_config = ConfigDict(
        from_attributes=True
    )


# class DirtyCompany(BaseModel):