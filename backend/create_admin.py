"""
Create initial admin user for testing
Run this script to create a test admin account
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import SessionLocal, engine
from backend.models import User, Base
import bcrypt

# Create tables
Base.metadata.create_all(bind=engine)

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.email == "admin@stockmaster.com").first()
        if existing:
            print("Admin user already exists!")
            return
        
        # Create admin user with bcrypt
        password = "admin123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        admin = User(
            email="admin@stockmaster.com",
            full_name="Admin User",
            hashed_password=hashed.decode('utf-8'),
            role="manager"
        )
        
        db.add(admin)
        db.commit()
        print("✓ Admin user created successfully!")
        print("Email: admin@stockmaster.com")
        print("Password: admin123")
        print("\nYou can now login with these credentials.")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
