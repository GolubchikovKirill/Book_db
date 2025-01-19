import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_table, Publisher, Book, Shop, Stock, Sale
from datetime import date
from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла
load_dotenv()

class DatabaseManager:
    def __init__(self, DNS):
        self.engine = sq.create_engine(DNS)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Метод создания таблиц."""
        create_table(self.engine)

    def add_records(self, records):
        """Добавление записей."""
        session = self.Session()
        try:
            session.add_all(records)
            session.commit()
            print("Records added successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error adding records: {e}")
        finally:
            session.close()

    def query_records(self, model, filters=None, join_models=None, distinct=False):
        """Универсальный метод для выборки данных."""
        session = self.Session()
        try:
            query = session.query(model)
            if join_models:
                for join_model in join_models:
                    query = query.join(join_model)
            if filters:
                query = query.filter(*filters)
            if distinct:
                query = query.distinct()
            return query.all()
        except Exception as e:
            print(f"Error querying records: {e}")
            return []
        finally:
            session.close()


if __name__ == "__main__":
    # Чтение строки подключения из .env файла
    DNS = os.getenv("DATABASE_URL")

    if not DNS:
        print("Database URL not found in environment variables.")
        exit(1)

    db_manager = DatabaseManager(DNS)
    db_manager.create_tables()

    # Добавление данных
    publisher1 = Publisher(name="ПИТЕР")
    publisher2 = Publisher(name="O'Reilly Media")

    book1 = Book(title="Изучаем Python", publisher=publisher2)
    book2 = Book(title="Чистый код", publisher=publisher1)

    shop1 = Shop(name="Буквоед")
    shop2 = Shop(name="Подписные Издания")

    stock1 = Stock(book=book1, shop=shop1, count=10)
    stock2 = Stock(book=book2, shop=shop2, count=5)

    sale1 = Sale(price=100.0, date_sale=date.today(), stock=stock1, count=2)
    sale2 = Sale(price=200.0, date_sale=date.today(), stock=stock2, count=1)

    db_manager.add_records([publisher1, publisher2, book1, book2, shop1, shop2, stock1, stock2, sale1, sale2])

    # Универсальный запрос: найти магазины, продающие книги целевого издателя
    publisher_name = input("Enter publisher name: ").strip()
    results = db_manager.query_records(
        model=Shop,
        filters=[Publisher.name == publisher_name],
        join_models=[Stock, Book, Publisher],
        distinct=True
    )

    if results:
        print(f"Shops selling books by publisher '{publisher_name}':")
        for shop in results:
            print(shop.name)
    else:
        print(f"No shops found for publisher '{publisher_name}'.")