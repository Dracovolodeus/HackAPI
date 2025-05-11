import asyncio
from sqlalchemy import inspect, text
from alembic.config import Config
from alembic import command

from crud.any_user import create_any_user
from crud.role import create_role
from database.db_helper import db_helper
from schemas.any_user import UserCreate
from schemas.role import RoleCreate


async def clear_db():
    # Удаляем все таблицы
    async for session in db_helper.session_getter():
        async with session.begin():
            tables = await session.run_sync(
                lambda sync_session: inspect(sync_session.connection()).get_table_names()
            )
            
            for table in tables:
                await session.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                print(f"Таблица {table} удалена")

    # Принудительно помечаем текущую миграцию как примененную
    alembic_cfg = Config("alembic.ini")
    await asyncio.to_thread(command.stamp, alembic_cfg, "head")
    
    # Генерируем и применяем новые миграции
    await asyncio.to_thread(
        command.revision,
        alembic_cfg,
        autogenerate=True,
        message="Initial after clear"
    )
    
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
    
    await db_helper.dispose()


async def main():
    await clear_db()

    async for session in db_helper.session_getter():
        # Создание ролей
        await create_role(session=session, role_create=RoleCreate(name="user"))
        await create_role(session=session, role_create=RoleCreate(name="resp_pers"))
        await create_role(session=session, role_create=RoleCreate(name="root"))

        # Создание пользователей
        await create_any_user(
            session=session,
            any_user_create=UserCreate(
                first_name="MyFirstName1",
                second_name="MySecondName1",
                last_name="MyLastName1",
                email="mymail@example.com",
                telegram_id=123123,
                password="qwertypasswd",
                phone="+79059323209",
            ),
            role_id=1,
        )
        await create_any_user(
            session=session,
            any_user_create=UserCreate(
                first_name="MyFirstName2",
                second_name="MySecondName2",
                last_name="MyLastName2",
                email="myemail@example.com",
                telegram_id=11212313,
                password="password",
                phone="+79134329402",
            ),
            role_id=2,
        )
        await create_any_user(
            session=session,
            any_user_create=UserCreate(
                first_name="MyFirstName3",
                second_name="MySecondName3",
                last_name="MyLastName3",
                email="email@example.com",
                telegram_id=9548513,
                password="qwerty",
                phone="+79134936402",
            ),
            role_id=3,
        )

    await db_helper.dispose()


if __name__ == "__main__":
    asyncio.run(main())
