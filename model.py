from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String(25),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    address=Column(String(100))
    is_staff=Column(Boolean,default=False)
    orders=relationship('Order',back_populates='user')


    def __repr__(self):
        return f"<User {self.username}"


class Order(Base):

    ORDER_STATUSES=(
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered')
    )

    DIMENSIONS=(
        ('2 * 2','2 * 2'),
        ('3 * 3','3 * 3'),
        ('4 * 4','4 * 4'),
        ('5 * 5','5 * 5')
    )


    __tablename__='orders'
    id=Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUSES),default="IN-TRANSIT")
    dimensions=Column(ChoiceType(choices=DIMENSIONS),default="2 * 2")
    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}>"



