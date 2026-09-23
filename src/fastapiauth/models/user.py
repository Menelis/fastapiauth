from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger
from src.fastapiauth.database.database import Base

class User(Base):
    __tablename__ = 'users'
    
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    firstname: Mapped[str] = mapped_column(String(200))
    lastname: Mapped[str] = mapped_column(String(200))
    email_address: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))
        