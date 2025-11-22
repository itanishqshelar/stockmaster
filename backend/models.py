from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class TransactionType(str, enum.Enum):
    RECEIPT = "RECEIPT"
    DELIVERY = "DELIVERY"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="staff") # manager, staff
    reset_otp = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    
    inventory = relationship("Inventory", back_populates="warehouse")
    transactions = relationship("Transaction", back_populates="warehouse")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    unit_of_measure = Column(String)
    
    inventory = relationship("Inventory", back_populates="product")
    transactions = relationship("Transaction", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    quantity = Column(Float, default=0.0)
    
    product = relationship("Product", back_populates="inventory")
    warehouse = relationship("Warehouse", back_populates="inventory")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=True)
    transaction_type = Column(String, index=True)  # receipt, delivery, transfer_in, transfer_out, adjustment
    quantity = Column(Float)
    reference = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    status = Column(String, default="ORDER_PLACED")  # For receipts: ORDER_PLACED, IN_TRANSIT, COMPLETED; For deliveries: ORDER_RECEIVED, SHIPPING, SHIPPED
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("Product", back_populates="transactions")
    warehouse = relationship("Warehouse")
