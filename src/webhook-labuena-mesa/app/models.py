from pydantic import BaseModel, EmailStr

class MemberRequest(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str

class MemberResponse(BaseModel):
    success: bool
    message: str
    voucher_code: str = None
    is_new: bool = False
