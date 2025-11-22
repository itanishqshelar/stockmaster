from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/operations",
    tags=["operations"],
)

# RECEIPT OPERATIONS - Incoming goods from suppliers
@router.post("/receipts/", response_model=schemas.OperationResponse)
def create_receipt(receipt: schemas.ReceiptCreate, db: Session = Depends(get_db)):
    """
    Create a receipt operation (incoming goods).
    Increases inventory only when status is COMPLETED.
    """
    try:
        # Validate product exists
        product = db.query(models.Product).filter(models.Product.id == receipt.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate warehouse exists
        warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == receipt.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        
        # Only update inventory if status is COMPLETED
        current_quantity = 0
        if receipt.status == "COMPLETED":
            # Update or create inventory record
            inventory = db.query(models.Inventory).filter(
                models.Inventory.product_id == receipt.product_id,
                models.Inventory.warehouse_id == receipt.warehouse_id
            ).first()
            
            if inventory:
                inventory.quantity += receipt.quantity
                current_quantity = inventory.quantity
            else:
                inventory = models.Inventory(
                    product_id=receipt.product_id,
                    warehouse_id=receipt.warehouse_id,
                    quantity=receipt.quantity
                )
                db.add(inventory)
                current_quantity = receipt.quantity
        
        # Create transaction record
        transaction = models.Transaction(
            product_id=receipt.product_id,
            warehouse_id=receipt.warehouse_id,
            transaction_type="receipt",
            quantity=receipt.quantity,
            reference=f"Receipt from {receipt.supplier_name}",
            notes=receipt.notes,
            status=receipt.status,
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        
        db.commit()
        db.refresh(transaction)
        
        status_msg = f"Receipt created with status: {receipt.status}"
        if receipt.status == "COMPLETED":
            status_msg += f". Inventory increased by {receipt.quantity} {product.unit_of_measure}"
        
        return {
            "success": True,
            "message": status_msg,
            "transaction_id": transaction.id,
            "new_quantity": current_quantity
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# DELIVERY OPERATIONS - Outgoing goods to customers
@router.post("/deliveries/", response_model=schemas.OperationResponse)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    """
    Create a delivery operation (outgoing goods).
    Decreases inventory only when status is SHIPPED.
    """
    try:
        # Validate product exists
        product = db.query(models.Product).filter(models.Product.id == delivery.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate warehouse exists
        warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == delivery.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        
        # Get current inventory
        inventory = db.query(models.Inventory).filter(
            models.Inventory.product_id == delivery.product_id,
            models.Inventory.warehouse_id == delivery.warehouse_id
        ).first()
        
        current_quantity = inventory.quantity if inventory else 0
        
        # Only decrease inventory if status is SHIPPED
        if delivery.status == "SHIPPED":
            if not inventory or inventory.quantity < delivery.quantity:
                available = inventory.quantity if inventory else 0
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient stock. Available: {available}, Requested: {delivery.quantity}"
                )
            
            # Decrease inventory
            inventory.quantity -= delivery.quantity
            current_quantity = inventory.quantity
        
        # Create transaction record
        transaction = models.Transaction(
            product_id=delivery.product_id,
            warehouse_id=delivery.warehouse_id,
            transaction_type="delivery",
            quantity=-delivery.quantity,  # Negative for outgoing
            reference=f"Delivery to {delivery.customer_name}",
            notes=delivery.notes,
            status=delivery.status,
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        
        db.commit()
        db.refresh(transaction)
        
        status_msg = f"Delivery created with status: {delivery.status}"
        if delivery.status == "SHIPPED":
            status_msg += f". Inventory decreased by {delivery.quantity} {product.unit_of_measure}"
        
        return {
            "success": True,
            "message": status_msg,
            "transaction_id": transaction.id,
            "new_quantity": current_quantity
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# TRANSFER OPERATIONS - Internal movement between warehouses
@router.post("/transfers/", response_model=schemas.OperationResponse)
def create_transfer(transfer: schemas.TransferCreate, db: Session = Depends(get_db)):
    """
    Create a transfer operation (internal movement).
    Moves stock between warehouses.
    """
    try:
        if transfer.from_warehouse_id == transfer.to_warehouse_id:
            raise HTTPException(status_code=400, detail="Cannot transfer to the same warehouse")
        
        # Validate product exists
        product = db.query(models.Product).filter(models.Product.id == transfer.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate both warehouses exist
        from_warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == transfer.from_warehouse_id).first()
        to_warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == transfer.to_warehouse_id).first()
        
        if not from_warehouse or not to_warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        
        # Check source inventory
        from_inventory = db.query(models.Inventory).filter(
            models.Inventory.product_id == transfer.product_id,
            models.Inventory.warehouse_id == transfer.from_warehouse_id
        ).first()
        
        if not from_inventory or from_inventory.quantity < transfer.quantity:
            available = from_inventory.quantity if from_inventory else 0
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock in source warehouse. Available: {available}, Requested: {transfer.quantity}"
            )
        
        # Decrease from source
        from_inventory.quantity -= transfer.quantity
        
        # Increase at destination
        to_inventory = db.query(models.Inventory).filter(
            models.Inventory.product_id == transfer.product_id,
            models.Inventory.warehouse_id == transfer.to_warehouse_id
        ).first()
        
        if to_inventory:
            to_inventory.quantity += transfer.quantity
        else:
            to_inventory = models.Inventory(
                product_id=transfer.product_id,
                warehouse_id=transfer.to_warehouse_id,
                quantity=transfer.quantity
            )
            db.add(to_inventory)
        
        # Create transaction records (one for each warehouse)
        transaction_out = models.Transaction(
            product_id=transfer.product_id,
            warehouse_id=transfer.from_warehouse_id,
            transaction_type="transfer_out",
            quantity=-transfer.quantity,
            reference=f"Transfer to {to_warehouse.name}",
            notes=transfer.notes,
            status="DONE",
            timestamp=datetime.utcnow()
        )
        
        transaction_in = models.Transaction(
            product_id=transfer.product_id,
            warehouse_id=transfer.to_warehouse_id,
            transaction_type="transfer_in",
            quantity=transfer.quantity,
            reference=f"Transfer from {from_warehouse.name}",
            notes=transfer.notes,
            status="DONE",
            timestamp=datetime.utcnow()
        )
        
        db.add(transaction_out)
        db.add(transaction_in)
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Transfer created: {transfer.quantity} {product.unit_of_measure} from {from_warehouse.name} to {to_warehouse.name}",
            "transaction_id": transaction_in.id,
            "new_quantity": to_inventory.quantity
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ADJUSTMENT OPERATIONS - Fix mismatches between recorded and physical count
@router.post("/adjustments/", response_model=schemas.OperationResponse)
def create_adjustment(adjustment: schemas.AdjustmentCreate, db: Session = Depends(get_db)):
    """
    Create an adjustment operation (fix inventory discrepancies).
    Updates inventory to match physical count.
    """
    try:
        # Validate product exists
        product = db.query(models.Product).filter(models.Product.id == adjustment.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Validate warehouse exists
        warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == adjustment.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")
        
        # Get current inventory
        inventory = db.query(models.Inventory).filter(
            models.Inventory.product_id == adjustment.product_id,
            models.Inventory.warehouse_id == adjustment.warehouse_id
        ).first()
        
        old_quantity = inventory.quantity if inventory else 0
        difference = adjustment.counted_quantity - old_quantity
        
        if inventory:
            inventory.quantity = adjustment.counted_quantity
        else:
            inventory = models.Inventory(
                product_id=adjustment.product_id,
                warehouse_id=adjustment.warehouse_id,
                quantity=adjustment.counted_quantity
            )
            db.add(inventory)
        
        # Create transaction record
        transaction = models.Transaction(
            product_id=adjustment.product_id,
            warehouse_id=adjustment.warehouse_id,
            transaction_type="adjustment",
            quantity=difference,
            reference=f"Stock adjustment: {adjustment.reason}",
            notes=f"Old: {old_quantity}, New: {adjustment.counted_quantity}. {adjustment.notes or ''}",
            status="DONE",
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        
        db.commit()
        db.refresh(transaction)
        
        return {
            "success": True,
            "message": f"Adjustment created: {'+' if difference >= 0 else ''}{difference} {product.unit_of_measure} ({old_quantity} → {adjustment.counted_quantity})",
            "transaction_id": transaction.id,
            "new_quantity": adjustment.counted_quantity
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# GET recent operations
@router.get("/recent/", response_model=List[schemas.TransactionHistory])
def get_recent_operations(limit: int = 50, db: Session = Depends(get_db)):
    """Get recent operations/transactions"""
    transactions = db.query(models.Transaction)\
        .order_by(models.Transaction.timestamp.desc())\
        .limit(limit)\
        .all()
    
    result = []
    for t in transactions:
        result.append({
            "id": t.id,
            "product_name": t.product.name,
            "warehouse_name": t.warehouse.name,
            "transaction_type": t.transaction_type,
            "quantity": t.quantity,
            "reference": t.reference,
            "notes": t.notes,
            "status": t.status,
            "timestamp": t.timestamp
        })
    
    return result


# UPDATE TRANSACTION STATUS
@router.patch("/{transaction_id}/status", response_model=schemas.OperationResponse)
def update_transaction_status(
    transaction_id: int, 
    status_update: schemas.StatusUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update transaction status and adjust inventory accordingly.
    For receipts: Only COMPLETED status adds to inventory
    For deliveries: Only SHIPPED status removes from inventory
    """
    try:
        transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        old_status = transaction.status
        new_status = status_update.status
        
        # Get inventory record
        inventory = db.query(models.Inventory).filter(
            models.Inventory.product_id == transaction.product_id,
            models.Inventory.warehouse_id == transaction.warehouse_id
        ).first()
        
        product = transaction.product
        
        # Handle receipt status changes
        if transaction.transaction_type == "receipt":
            if old_status != "COMPLETED" and new_status == "COMPLETED":
                # Add to inventory when changing to COMPLETED
                if inventory:
                    inventory.quantity += transaction.quantity
                else:
                    inventory = models.Inventory(
                        product_id=transaction.product_id,
                        warehouse_id=transaction.warehouse_id,
                        quantity=transaction.quantity
                    )
                    db.add(inventory)
            elif old_status == "COMPLETED" and new_status != "COMPLETED":
                # Remove from inventory when changing from COMPLETED
                if inventory:
                    inventory.quantity -= transaction.quantity
        
        # Handle delivery status changes
        elif transaction.transaction_type == "delivery":
            if old_status != "SHIPPED" and new_status == "SHIPPED":
                # Remove from inventory when changing to SHIPPED
                if not inventory or inventory.quantity < abs(transaction.quantity):
                    available = inventory.quantity if inventory else 0
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient stock. Available: {available}, Required: {abs(transaction.quantity)}"
                    )
                inventory.quantity -= abs(transaction.quantity)
            elif old_status == "SHIPPED" and new_status != "SHIPPED":
                # Add back to inventory when changing from SHIPPED
                if inventory:
                    inventory.quantity += abs(transaction.quantity)
        
        # Update transaction status
        transaction.status = new_status
        
        db.commit()
        
        current_quantity = inventory.quantity if inventory else 0
        
        return {
            "success": True,
            "message": f"Status updated from {old_status} to {new_status}",
            "transaction_id": transaction.id,
            "new_quantity": current_quantity
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
