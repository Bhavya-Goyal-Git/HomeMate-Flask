import datetime

class Config:
    SECRET_KEY="13cfee28e2e7f43cf73b302f19d36d7e71f870fe45c93cc3b5093f92161dd74d"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI="sqlite:///homemate.sqlite3"
    JWT_SECRET_KEY = "d9a24f717d6902a481a304256d3ef4542ae7bff4d8373fc7c644d04ff0dc236b"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)