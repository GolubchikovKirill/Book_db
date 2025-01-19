import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(60), nullable=False)

    # Двусторонняя связь
    books = relationship("Book", back_populates="publisher")

    def __str__(self):
        return f"Publisher {self.name}: {self.id}"

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(50), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"))

    # Двусторонняя связь
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

    def __str__(self):
        return f"Book {self.title}: {self.id_publisher}"

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    count = sq.Column(sq.Integer, nullable=False)

    # Двусторонняя связь
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

    def __str__(self):
        return f"Stock {self.id_book}: {self.id_shop}, quantity - {self.count}"

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(60), unique=True, nullable=False)

    # Двусторонняя связь
    stocks = relationship("Stock", back_populates="shop")

    def __str__(self):
        return f"Shop {self.name}: {self.id}"

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer, nullable=False)

    # Двусторонняя связь
    stock = relationship("Stock", back_populates="sales")

    def __str__(self):
        return f"Sale {self.date_sale}: {self.id}"

def create_table(engine):
    Base.metadata.create_all(engine)