from pydantic import BaseModel , EmailStr ,Field, field_validator
from typing import Optional

class AddLead(BaseModel):
    # the frontend sometimes sends an existing leadId; ignore it if provided
    leadId: Optional[str] = None
    name: str
    phone: str = Field(..., pattern=r'^\d{10,15}$')
    email: EmailStr
    source: str
    status: str
    budget: int = Field(..., ge=0)
    notes: Optional[str] = None

    # validator should reference the actual field name ("phone")
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        return value

# if you want a model that includes the generated id, keep this
class LeadWithID(AddLead):
    leadId: str
    
