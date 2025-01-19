import json
import os
from dotenv import load_dotenv
from models import Publisher, Book, Shop, Stock, Sale
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sq

# Загрузка переменных окружения
load_dotenv()

class DatabaseManager:
    def __init__(self, DNS):
        # Подключение к базе данных
        self.engine = sq.create_engine(DNS)
        self.Session = sessionmaker(bind=self.engine)

    def load_data_from_json(self, filepath):
        """Загружает данные из JSON и добавляет их в базу."""
        session = self.Session()
        try:
            # Открываем JSON файл
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Маппинг моделей
            model_mapping = {
                "publisher": Publisher,
                "book": Book,
                "shop": Shop,
                "stock": Stock,
                "sale": Sale,
            }

            # Обрабатываем каждую запись из JSON
            for item in data:
                model_name = item["model"]
                model_class = model_mapping.get(model_name)
                if not model_class:
                    print(f"Unknown model: {model_name}")
                    continue

                # Преобразуем данные в формат, подходящий для создания записи
                record = model_class(**item["fields"])
                session.add(record)

            # Коммитим изменения
            session.commit()
            print(f"Data from {filepath} loaded successfully.")
        except Exception as e:
            # В случае ошибки откатываем изменения
            session.rollback()
            print(f"Error loading data from {filepath}: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    # Чтение строки подключения из .env файла
    DNS = os.getenv("DATABASE_URL")

    if not DNS:
        print("Database URL not found in environment variables.")
        exit(1)

    db_manager = DatabaseManager(DNS)

    # Загрузка данных из JSON файла
    db_manager.load_data_from_json('tests_data.json')