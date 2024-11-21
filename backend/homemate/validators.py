from .models.tables import User
import re

def length_validator(key,num):
    if len(key)<num:
        raise ValueError(f"Length must not be less than {num}")
    
def username_validator(username):
    length_validator(username,5)
    pattern = r"^[a-zA-Z][a-zA-Z0-9_]+$"
    if not re.fullmatch(pattern,username):
        raise ValueError("Username must not contain special characters")
    user = User.query.filter_by(username=username).one_or_none()
    if user:
        raise ValueError("Username already exists")
    return username

def email_validator(email):
    pattern = r"^[a-zA-Z][a-zA-Z0-9_.]+@[a-zA-Z0-9_]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(pattern,email):
        raise ValueError("Email Address is not valid")
    user = User.query.filter_by(email_address=email).one_or_none()
    if user:
        raise ValueError("Email Address already registered with different account")
    return email

def password_validator(passwd):
    length_validator(passwd,8)
    return passwd

def role_validator(role):
    if role in ['customer','professional']:
        return role
    raise ValueError("Role is invalid")


add_data = ["base_address","pincode","city","state"]
def address_validator(val):
    if not isinstance(val, dict):
        raise ValueError("Address must be a dictionary.")
    for key in add_data:
        if key not in val:
            raise ValueError(f"Missing {key} in address.")
        if not val[key]:
            raise ValueError(f"{key} must be a non-empty string.")
    return val

def name_validator(val):
    length_validator(val,2)
    return val