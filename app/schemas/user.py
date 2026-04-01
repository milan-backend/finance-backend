from pydantic import BaseModel

class UpdateUserRole(BaseModel):
    role: str