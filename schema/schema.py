from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class AddLead(BaseModel):
    leadId: Optional[str] = None
    name: str
    phone: str = Field(..., pattern=r'^\d{10,15}$')
    email: EmailStr
    source: str
    status: str
    budget: int = Field(..., ge=0)
    notes: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        return value


class LeadWithID(AddLead):
    leadId: str


class AddCustomer(BaseModel):
    customerId: Optional[str] = None
    Name: str
    PhoneNumber: str = Field(..., pattern=r'^\d{10,15}$')
    Email: EmailStr
    Source: str
    Budget: int = Field(..., ge=0)
    Notes: Optional[str] = None

    @field_validator("PhoneNumber")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        return value


class CustomerWithID(AddCustomer):
    customerId: str