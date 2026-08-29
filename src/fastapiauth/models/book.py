from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger
from ..database.database import Base


class Book(Base):
    __tablename__ = "books"
    
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(50), nullable=False)
    author:Mapped[str] = mapped_column(String(50), nullable=False)