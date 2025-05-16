import asyncio

from sqlalchemy import MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Прямо указываем URL базы данных
DATABASE_URL = "postgresql+asyncpg://root:ytrewq@localhost:5432/library"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=False)

# Создаем сессию
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    async with async_session() as session:
        # Получаем асинхронное соединение
        async with engine.connect() as conn:
            # Получаем метаданные
            metadata = MetaData()
            await conn.run_sync(metadata.reflect)

            # Перебираем все таблицы и выводим их содержимое
            for table in metadata.sorted_tables:
                print(f"\nТаблица: {table.name}")
                result = await conn.execute(select(table))
                rows = result.fetchall()
                for ind, row in enumerate(rows):
                    print("\n" if ind != 0 else "" + f"\tНомер строки: {ind + 1}")
                    for column, value in zip(table.columns, row):
                        print(f"\t{column.name}, Тип: {type(value)} Значение: {value}")


if __name__ == "__main__":
    asyncio.run(main())
