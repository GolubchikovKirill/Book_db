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


def get_shops(session, publisher_info):
    """
    Функция для поиска магазинов, продающих книги заданного публициста
    :param session: сессия для работы с базой данных
    :param publisher_info: имя или ID публициста
    """
    query = (
        session.query(
            Book.title,  # Название книги
            Shop.name,  # Название магазина
            Sale.price,  # Цена продажи
            Sale.date_sale,  # Дата продажи
        )
        .select_from(Sale)
        .join(Stock)
        .join(Book)
        .join(Publisher)
        .join(Shop)
    )

    if publisher_info.isdigit():  # Если введенное значение состоит из цифр
        result = query.filter(Publisher.id == int(publisher_info)).all()
    else:
        result = query.filter(Publisher.name == publisher_info).all()

    if not result:
        print("Данные не найдены.")
        return

    # Таблица для вывода данных
    header = ["Название книги", "Магазин", "Цена", "Дата"]
    widths = [40, 20, 10, 15]
    separator = "+" + "+".join("-" * w for w in widths) + "+"

    print(separator)
    print("|" + "|".join(f"{header[i]:^{widths[i]}}" for i in range(len(header))) + "|")
    print(separator)

    for title, shop_name, price, date_sale in result:
        row = [
            f"{title:<{widths[0]}}",
            f"{shop_name:<{widths[1]}}",
            f"{price:<{widths[2]}}",
            f"{date_sale.strftime('%d-%m-%Y'):<{widths[3]}}",
        ]
        print("|" + "|".join(row) + "|")

    print(separator)


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

    book1 = Book(title="Изучаем Python", publisher=publisher1)
    book2 = Book(title="Чистый код", publisher=publisher1)
    book3 = Book(title="PostgreSQL - Administration", publisher=publisher2)

    shop1 = Shop(name="Буквоед")
    shop2 = Shop(name="Подписные Издания")

    stock1 = Stock(book=book1, shop=shop1, count=10)
    stock2 = Stock(book=book2, shop=shop2, count=5)
    stock3 = Stock(book=book3, shop=shop2, count=15)

    sale1 = Sale(price=100.0, date_sale=date.today(), stock=stock1, count=2)
    sale2 = Sale(price=200.0, date_sale=date.today(), stock=stock2, count=1)
    sale3 = Sale(price=500.0, date_sale=date.today(), stock=stock3, count=3)

    db_manager.add_records([publisher1, publisher2, book1, book2, book3, shop1, shop2, stock1, stock2, stock3, sale1, sale2, sale3])

    # Создаем сессию
    session = db_manager.Session()

    try:
        publisher_info = input("Введите имя или ID публициста: ").strip()
        get_shops(session, publisher_info)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        session.close()