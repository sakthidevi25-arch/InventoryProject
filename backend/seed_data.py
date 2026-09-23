from backend.database.session import SessionLocal
from backend.models.asset import Asset
from backend.models.api import Api
from backend.models.role import Role
from backend.models.user import User
from backend.security.password_utils import hash_password


def seed_data():
    db = SessionLocal()
    try:
        if db.query(Role).count() == 0:
            admin_role = Role(name="Admin", description="System administrator")
            user_role = Role(name="User", description="Standard application user")
            auditor_role = Role(name="Auditor", description="Audit and compliance viewer")
            db.add_all([admin_role, user_role, auditor_role])
            db.commit()

        if db.query(User).count() == 0:
            admin_role = db.query(Role).filter(Role.name == "Admin").first()
            admin = User(
                username="admin",
                email="admin@example.com",
                full_name="Platform Administrator",
                password_hash=hash_password("Admin@123"),
                is_active=True,
                is_verified=True,
                role_id=admin_role.id,
            )
            db.add(admin)
            db.commit()

        if db.query(Asset).count() == 0:
            db.add_all(
                [
                    Asset(
                        asset_id="ASSET-001",
                        asset_name="Prod-Web-VM-01",
                        asset_category="Virtual Machines",
                        cloud_provider="AWS",
                        account_id="123456789012",
                        region="us-east-1",
                        owner="Platform Team",
                        environment="Production",
                        criticality="High",
                        description="Primary web application VM",
                    ),
                    Asset(
                        asset_id="ASSET-002",
                        asset_name="Payments-DB",
                        asset_category="Databases",
                        cloud_provider="Azure",
                        account_id="AZ-987654",
                        region="eastus",
                        owner="Data Platform",
                        environment="Production",
                        criticality="Critical",
                        description="Core transactional database",
                    ),
                ]
            )
            db.commit()

        if db.query(Api).count() == 0:
            db.add_all(
                [
                    Api(
                        api_name="Customer Profile API",
                        api_path="/api/v1/customers",
                        http_method="GET",
                        application_name="CRM Portal",
                        owner="API Platform",
                        environment="Production",
                        authentication_type="OAuth2",
                        version="v1",
                    ),
                    Api(
                        api_name="Billing Status API",
                        api_path="/api/v1/billing/status",
                        http_method="POST",
                        application_name="Billing Service",
                        owner="Finance Systems",
                        environment="Production",
                        authentication_type="API Key",
                        version="v2",
                    ),
                ]
            )
            db.commit()

        print("Seed data loaded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
