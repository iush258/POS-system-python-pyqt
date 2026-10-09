from app.database.models.user import User, UserRole
from app.database.session import SessionLocal
from app.security.password import hash_password


db = SessionLocal()

try:
    existing_user = db.query(User).filter(
        User.email == "admin@example.com"
    ).first()

    if existing_user is not None:
        print("Admin user already exists.")
    else:
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("Admin user created successfully.")
finally:
    db.close()