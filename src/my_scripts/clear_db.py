import asyncio

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine


async def main():
    DATABASE_URL = "postgresql+asyncpg://root:ytrewq@localhost:5432/library"
    engine = create_async_engine(DATABASE_URL)

    async with engine.connect() as conn:
        # Получаем список всех таблиц
        inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

        # Удаляем все таблицы с каскадом
        for table in inspector:
            await conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
            print(f"Таблица {table} удалена")

        await conn.commit()

    await engine.dispose()


asyncio.run(main())
