from enum import Enum

class UserRole(str,Enum):
    USER="user"
    ADMIN="admin"
    

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"