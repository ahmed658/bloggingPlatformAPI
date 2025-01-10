from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashedpassword: str):
    return pwd_context.verify(plain_password, hashedpassword)

def remove_attribute(model: BaseModel, attribute: str):
    """
    Removes the specified attribute from the Pydantic model (if it exists) 
    and returns the model's dictionary representation.
    
    :param model: A Pydantic BaseModel instance.
    :param attribute: The attribute to remove from the model.
    :return: A dictionary representation of the model without the attribute.
    """
    if hasattr(model, attribute):
        delattr(model, attribute)
    
    # Using `.dict()` for compatibility with older Pydantic versions.
    # Replace `.dict()` with `.model_dump()` for Pydantic v2+.
    return model