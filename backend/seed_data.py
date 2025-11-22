from .database import SessionLocal, engine, Base
from . import models

def seed_database():
    """Seed the database with sample electronics warehouse data"""
    # Create all tables first
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_products = db.query(models.Product).first()
        if existing_products:
            print("Database already seeded")
            return
        
        # Create warehouses
        warehouse_a = models.Warehouse(
            name="Electronics Warehouse A",
            location="Building A - Tech District"
        )
        warehouse_b = models.Warehouse(
            name="Electronics Warehouse B",
            location="Building B - Tech District"
        )
        db.add(warehouse_a)
        db.add(warehouse_b)
        db.commit()
        db.refresh(warehouse_a)
        db.refresh(warehouse_b)
        
        # Sample PC Parts and Electronics
        products_data = [
            # CPUs
            {"name": "Intel Core i9-14900K", "sku": "CPU-INT-14900K", "category": "Processors", "unit": "units", "qty": 45},
            {"name": "AMD Ryzen 9 7950X", "sku": "CPU-AMD-7950X", "category": "Processors", "unit": "units", "qty": 38},
            {"name": "Intel Core i7-14700K", "sku": "CPU-INT-14700K", "category": "Processors", "unit": "units", "qty": 62},
            {"name": "AMD Ryzen 7 7800X3D", "sku": "CPU-AMD-7800X3D", "category": "Processors", "unit": "units", "qty": 55},
            
            # GPUs
            {"name": "NVIDIA RTX 4090", "sku": "GPU-NV-4090", "category": "Graphics Cards", "unit": "units", "qty": 12},
            {"name": "NVIDIA RTX 4080 Super", "sku": "GPU-NV-4080S", "category": "Graphics Cards", "unit": "units", "qty": 28},
            {"name": "AMD Radeon RX 7900 XTX", "sku": "GPU-AMD-7900XTX", "category": "Graphics Cards", "unit": "units", "qty": 22},
            {"name": "NVIDIA RTX 4070 Ti", "sku": "GPU-NV-4070TI", "category": "Graphics Cards", "unit": "units", "qty": 35},
            
            # Motherboards
            {"name": "ASUS ROG Maximus Z790 Hero", "sku": "MB-ASUS-Z790", "category": "Motherboards", "unit": "units", "qty": 18},
            {"name": "MSI MPG X670E Carbon WiFi", "sku": "MB-MSI-X670E", "category": "Motherboards", "unit": "units", "qty": 25},
            {"name": "Gigabyte B650 AORUS Elite", "sku": "MB-GB-B650", "category": "Motherboards", "unit": "units", "qty": 42},
            
            # RAM
            {"name": "Corsair Vengeance DDR5 32GB", "sku": "RAM-COR-DDR5-32", "category": "Memory", "unit": "units", "qty": 150},
            {"name": "G.Skill Trident Z5 RGB 64GB", "sku": "RAM-GS-DDR5-64", "category": "Memory", "unit": "units", "qty": 88},
            {"name": "Kingston FURY Beast DDR5 16GB", "sku": "RAM-KIN-DDR5-16", "category": "Memory", "unit": "units", "qty": 210},
            
            # Storage
            {"name": "Samsung 990 Pro 2TB NVMe", "sku": "SSD-SAM-990P-2TB", "category": "Storage", "unit": "units", "qty": 95},
            {"name": "WD Black SN850X 1TB NVMe", "sku": "SSD-WD-SN850X-1TB", "category": "Storage", "unit": "units", "qty": 120},
            {"name": "Crucial P5 Plus 500GB NVMe", "sku": "SSD-CRU-P5-500GB", "category": "Storage", "unit": "units", "qty": 180},
            {"name": "Seagate Barracuda 4TB HDD", "sku": "HDD-SEA-4TB", "category": "Storage", "unit": "units", "qty": 75},
            
            # Power Supplies
            {"name": "Corsair RM1000x 1000W", "sku": "PSU-COR-1000W", "category": "Power Supplies", "unit": "units", "qty": 48},
            {"name": "EVGA SuperNOVA 850W", "sku": "PSU-EVG-850W", "category": "Power Supplies", "unit": "units", "qty": 65},
            {"name": "Seasonic Focus GX 750W", "sku": "PSU-SEA-750W", "category": "Power Supplies", "unit": "units", "qty": 92},
            
            # Cases
            {"name": "NZXT H7 Flow", "sku": "CASE-NZXT-H7", "category": "Cases", "unit": "units", "qty": 34},
            {"name": "Lian Li O11 Dynamic EVO", "sku": "CASE-LL-O11D", "category": "Cases", "unit": "units", "qty": 28},
            {"name": "Fractal Design Meshify 2", "sku": "CASE-FD-M2", "category": "Cases", "unit": "units", "qty": 41},
            
            # Cooling
            {"name": "Noctua NH-D15 CPU Cooler", "sku": "COOL-NOC-NHD15", "category": "Cooling", "unit": "units", "qty": 58},
            {"name": "Corsair iCUE H150i Elite LCD", "sku": "COOL-COR-H150I", "category": "Cooling", "unit": "units", "qty": 45},
            {"name": "Arctic Liquid Freezer II 280", "sku": "COOL-ARC-LF280", "category": "Cooling", "unit": "units", "qty": 52},
            
            # Peripherals
            {"name": "Logitech G Pro X Superlight", "sku": "MOUSE-LOG-GPXS", "category": "Peripherals", "unit": "units", "qty": 110},
            {"name": "Razer BlackWidow V4 Pro", "sku": "KB-RAZ-BWV4", "category": "Peripherals", "unit": "units", "qty": 78},
            {"name": "SteelSeries Arctis Nova Pro", "sku": "HS-SS-ANP", "category": "Peripherals", "unit": "units", "qty": 62},
            
            # Monitors
            {"name": "LG 27GR95QE-B 27\" OLED 240Hz", "sku": "MON-LG-27GR95", "category": "Monitors", "unit": "units", "qty": 15},
            {"name": "ASUS ROG Swift PG279QM 27\"", "sku": "MON-ASUS-PG279", "category": "Monitors", "unit": "units", "qty": 22},
            {"name": "Dell S2722DGM 27\" 165Hz", "sku": "MON-DELL-S2722", "category": "Monitors", "unit": "units", "qty": 38},
            
            # Complete PCs
            {"name": "Gaming PC - RTX 4090 Build", "sku": "PC-GAME-4090", "category": "Complete Systems", "unit": "units", "qty": 8},
            {"name": "Workstation PC - Threadripper", "sku": "PC-WORK-TR", "category": "Complete Systems", "unit": "units", "qty": 5},
            {"name": "Office PC - Budget Build", "sku": "PC-OFF-BUD", "category": "Complete Systems", "unit": "units", "qty": 32},
            
            # Low Stock Items
            {"name": "Thermal Paste - Arctic MX-6", "sku": "ACC-TH-MX6", "category": "Accessories", "unit": "tubes", "qty": 8},
            {"name": "RGB LED Strips 2m", "sku": "ACC-LED-2M", "category": "Accessories", "unit": "units", "qty": 5},
        ]
        
        # Create products and inventory
        for item in products_data:
            product = models.Product(
                name=item["name"],
                sku=item["sku"],
                category=item["category"],
                unit_of_measure=item["unit"]
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            
            # Create inventory entries for both warehouses
            # Split inventory between warehouse A and B
            qty_a = item["qty"] // 2
            qty_b = item["qty"] - qty_a
            
            inventory_a = models.Inventory(
                product_id=product.id,
                warehouse_id=warehouse_a.id,
                quantity=qty_a
            )
            inventory_b = models.Inventory(
                product_id=product.id,
                warehouse_id=warehouse_b.id,
                quantity=qty_b
            )
            db.add(inventory_a)
            db.add(inventory_b)
        
        db.commit()
        print(f"✅ Successfully seeded database with {len(products_data)} electronics products!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
