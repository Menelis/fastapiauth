from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.book import Book
from ..schemas.book_schemas import BookCreate, BookResponse

class BookRepository:
    # Constructor(DI) for db session
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def add_book(self, book_create: BookCreate) -> BookResponse:
        book = Book(**book_create.model_dump())
        self.db_session.add(book)
        await self.db_session.commit()
        await self.db_session.refresh(book)
        book_response = BookResponse.model_validate(book)
        return book_response
    
    async def update_book(self, book_id:int, book_update: BookCreate) -> Optional[BookResponse]:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db_session.execute(stmt)
        existing_book = result.scalar_one_or_none()
        
        if existing_book is None:
            return None
        for key, value in book_update.model_dump().items:
            setattr(existing_book, key, value)
        await self.db_session.commit()
        await self.db_session.refresh(existing_book)
        
        return existing_book
    
    async def delete_book(self, book_id:int) -> Optional[BookResponse]:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db_session.execute(stmt)
        existing_book = result.scalar_one_or_none()
        
        if existing_book is None:
            return None
        await self.db_session.delete(existing_book)
        await self.db_session.commit()
        return BookResponse.model_validate(existing_book)
    
    async def get_book(self, book_id:int) -> Optional[BookResponse]:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db_session.execute(stmt)
        book = result.scalar_one_or_none();
        if book is None:
            return None
        return BookResponse.model_validate(book)
    
    async def get_books(self) -> List[BookResponse]:
        result = await self.db_session.execute(select(Book))
        books = result.all()
        return [BookResponse.model_validate(book) for book in books] 
        
        
        
    
    
