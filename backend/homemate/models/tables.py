from . import db, bcrypt, jwt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, ForeignKey, String
import datetime
from typing import List

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=int(identity)).one_or_none()

class User(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(unique=True,nullable=False)
    email_address:Mapped[str] = mapped_column(unique=True,nullable=False)
    password_hash:Mapped[str] = mapped_column(nullable=False)
    role:Mapped[str] = mapped_column(nullable=False)
    date_joined:Mapped[datetime.date] = mapped_column(default=datetime.date.today())

    __table_args__ = (
        CheckConstraint(role.in_(["admin","customer","professional"]), name='User_role_validator'),
    )
    
    customer_data:Mapped["Customer"] = relationship()
    professional_data:Mapped["Professional"] = relationship()

    @property
    def password(self):
        raise AttributeError("Non Accessible attribute")

    @password.setter
    def password(self,password_to_set):
        self.password_hash = bcrypt.generate_password_hash(password_to_set).decode("utf-8")

    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)


class Customer(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"),unique=True)
    name:Mapped[str] = mapped_column(nullable=False)
    base_address:Mapped[str] #address start
    city:Mapped[str] = mapped_column(nullable=False)
    pincode:Mapped[str] = mapped_column(String(6),nullable=True)
    state:Mapped[str] = mapped_column(nullable=False) #address end
    isflagged:Mapped[bool] = mapped_column(default=False)
    
    service_requests:Mapped[List["ServiceRequest"]] = relationship(back_populates="customer")

class ServiceCategory(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(unique=True,nullable=False)

class Service(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(unique=True,nullable=False)
    base_price:Mapped[float] = mapped_column(nullable=False)
    description:Mapped[str]
    category:Mapped[str] = mapped_column(nullable=False)
    
    professionals:Mapped[List["Professional"]] = relationship(back_populates="service_type")

class Professional(db.Model): #service worker
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"),unique=True)
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str]
    base_address:Mapped[str] #address start
    city:Mapped[str] = mapped_column(nullable=False)
    pincode:Mapped[str] = mapped_column(String(6),nullable=True)
    state:Mapped[str] = mapped_column(nullable=False) #address end
    contact_no:Mapped[str] = mapped_column(String(10),nullable=False)
    profile_pic:Mapped[str] = mapped_column(unique=True,nullable=True)
    submitted_doc:Mapped[str] = mapped_column(unique=True,nullable=False)
    isflagged:Mapped[bool] = mapped_column(default=False)
    isverified:Mapped[bool] = mapped_column(default=False) #admin verify by docs
    experience:Mapped[str] = mapped_column(nullable=False) #months
    rating:Mapped[int] = mapped_column(nullable=False,default=0) #rating/raters will be star rating
    num_raters:Mapped[int] = mapped_column(nullable=False,default=0)
    service_id:Mapped[int] = mapped_column(ForeignKey("service.id"))
    fees:Mapped[float] = mapped_column(nullable=False)
    fees_unit:Mapped[str] = mapped_column(nullable=False) #fees is per m2/hour/etc.
    
    service_type:Mapped["Service"] = relationship(back_populates="professionals")
    reviews:Mapped[List["ProfessionalReview"]] = relationship()
    service_requests:Mapped[List["ServiceRequest"]] = relationship(back_populates="professional")
    
class ProfessionalReview(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    customer_id:Mapped[int] = mapped_column(ForeignKey("customer.id"))
    professional_id:Mapped[int] = mapped_column(ForeignKey("professional.id"))
    stars:Mapped[int] = mapped_column(nullable=False)
    review:Mapped[str] = mapped_column(nullable=False)
    dateofreview:Mapped[datetime.date] = mapped_column(default=datetime.date.today())
    
    __table_args__ = (
        CheckConstraint('stars > 0 AND stars <= 5', name='check_stars_between_1_and_5'),
    )
    
    customer:Mapped["Customer"] = relationship()
    
class ServiceRequest(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    customer_id:Mapped[int] = mapped_column(ForeignKey("customer.id"))
    professional_id:Mapped[int] = mapped_column(ForeignKey("professional.id"))
    dateofrequest:Mapped[datetime.date] = mapped_column(default=datetime.date.today())
    dateofcompletion:Mapped[datetime.date] = mapped_column(nullable=True)
    status:Mapped[str] = mapped_column(nullable=False)
    remarks:Mapped[str]
    work_units:Mapped[float] #to be filled by professional
    parts_cost:Mapped[float] #to be filled by professional
    total_bill:Mapped[float] # base price + (work_units * professional fees) + parts cost
    
    customer:Mapped["Customer"] = relationship()
    professional:Mapped["Professional"] = relationship()
    
    __table_args__ = (
        CheckConstraint(status.in_(["booked","accepted","rejected","cancelled","served","completed"]), name='service_status_validator'),
    )
    
class Transaction(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True)
    amount:Mapped[float] = mapped_column(nullable=False) #positive for incoming, negative for outgoing