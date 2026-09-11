from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.user import User
from ..schemas.user_schemas import UserCreate, UserUpdate, UserLogin
from ..security.auth import get_password_hash, verify_password


class UserRepository:
    # Constructor(DI) for db session
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def get_all(self):
        result = await self.db_session.execute(select(User))
        return result.scalars().all()
    
    async def get_by_id(self, id:int):
        result = await self.db_session.execute(
            select(User).filter(User.id == id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email:str):
        result = await self.db_session.execute(select(User)
                                               .filter(User.email_address == email))
        return result.scalar_one_or_none()
    
    async def register(self, user: UserCreate):
        password = get_password_hash(user.password)
        new_user = User(firstname=user.firstname,
                        lastname=user.lastname,
                        email_address=user.email_address,
                        password=password)
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user
    
    async def update(self, usr_from_db: User, user: UserUpdate):
        usr_from_db.email_address = user.email_address
        usr_from_db.firstname = user.firstname
        usr_from_db.lastname = user.lastname
        if user.password:
            usr_from_db.password = get_password_hash(user.password)
        await self.db_session.commit()
        await self.db_session.refresh(usr_from_db)
        return usr_from_db
    
    async def delete(self, user: User):
        await self.db_session.delete(user)
        await self.db_session.commit()
        
    async def authenticate(self, user: UserLogin):
        usr_from_db = self.get_by_email(user.email_address)
        if usr_from_db and verify_password(user.password, usr_from_db.password):
            return usr_from_db
        return None
