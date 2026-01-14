from app.models.models_user import User, WorkUnit, UserRole
from sqlmodel import Session, select, func, col
from math import ceil
from typing import Tuple

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
    
    def get_all_users(self, page : int = 1, limit: int = 10) -> Tuple[list[User], int]:
        offset = (page - 1) * limit
        statement = select(User).offset(offset).limit(limit)
        results = self.session.exec(statement).all()
        total = self.session.exec(select(func.count(col(User.id)))).one()
        total_pages = ceil(total / limit)
        return list(results), total_pages
    
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