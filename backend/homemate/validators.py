from .models.tables import User, Service
from datetime import datetime
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

def service_title_validator(val):
    length_validator(val,5)
    serv = Service.query.filter_by(title=val).one_or_none()
    if serv:
        raise ValueError(f"Service with title {val} already exists")
    return val

def service_title_validator_old(val):
    length_validator(val,5)
    return val

def price_validator(val):
    try:
        val = float(val)
    except:
        raise ValueError("Price must be a floating point number")
    if val<=0:
        raise ValueError("Price must be a positive number")
    return val

def mobile_num_validator(val):
    pattern = r"^[0-9]+$"
    if len(val)!=10 or not re.fullmatch(pattern,val):
        raise ValueError("Mobile number must be 10 digit numeric")
    return val

def validate_pincode(val):
    pattern = r"^[0-9]+$"
    if len(val)!=6 or not re.fullmatch(pattern,val):
        raise ValueError("Pincode must be 6 digit numeric")
    return val

def clean_searchquery(val):
    return "%" + "".join([char for char in val if char.isalnum()]) + "%"

def date_validator(val):
    pattern = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    if not re.fullmatch(pattern,val):
        raise ValueError("Invalid date sent Regex")
    try:
        val = datetime.strptime(val, '%Y-%m-%d').date()
    except ValueError as e:
        print(f"Error: {e}")
        raise ValueError("Invalid date sent Convert")
    return val