from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/warehouses",
    tags=["warehouses"],
)

@router.post("/", response_model=schemas.Warehouse)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = db.query(models.Warehouse).filter(models.Warehouse.name == warehouse.name).first()
    if db_warehouse:
        raise HTTPException(status_code=400, detail="Warehouse with this name already exists")
    new_warehouse = models.Warehouse(**warehouse.dict())
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse

@router.get("/", response_model=List[schemas.Warehouse])
def read_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    warehouses = db.query(models.Warehouse).offset(skip).limit(limit).all()
    return warehouses


@router.get("/inventory")
def get_warehouse_inventory(db: Session = Depends(get_db)):
    """Get inventory summary for all warehouses"""
    warehouses = db.query(models.Warehouse).all()
    
    result = []
    for warehouse in warehouses:
        inventories = db.query(models.Inventory).filter(
            models.Inventory.warehouse_id == warehouse.id
        ).all()
        
        total_items = len(inventories)
        total_quantity = sum([inv.quantity for inv in inventories])
        
        result.append({
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "total_items": total_items,
            "total_quantity": int(total_quantity)
        })
    
    return result


@router.get("/{warehouse_id}/items")
def get_warehouse_items(warehouse_id: int, db: Session = Depends(get_db)):
    """Get all items in a specific warehouse"""
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    inventories = db.query(models.Inventory).filter(
        models.Inventory.warehouse_id == warehouse_id
    ).all()
    
    result = []
    for inv in inventories:
        product = inv.product
        result.append({
            "product_name": product.name,
            "sku": product.sku,
            "category": product.category,
            "quantity": int(inv.quantity)
        })
    
    return result

