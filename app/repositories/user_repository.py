from app.models.models_user import User, WorkUnit, UserRole
from sqlmodel import Session, select 

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create_user(self, name: str, email: str, hash_password: str, role: UserRole = UserRole.OPERATOR, work_unit_id: int | None = None) -> User:
        user = User(name = name, email = email, hash_password = hash_password, role = role, work_unit_id = work_unit_id)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_user_by_email(self, email:str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result
    
    def get_user_by_id(self, user_id: int) -> User | None:
        user = self.session.get(User, user_id)
        return user
    
    def get_all_users(self) -> list[User]:
        statement = select(User)
        results = self.session.exec(statement).all()
        return list(results)
    
    def update_user(self, user_id: int,**kwargs) -> User | None:
        user = self.session.get(User, user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return user        