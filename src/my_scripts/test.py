import asyncio

import asyncpg


async def update_refresh_token():
    # Подключение к базе данных
    conn = await asyncpg.connect("postgresql://root:ytrewq@localhost:5432/library")

    try:
        # Обновление данных в таблице any_user
        await conn.execute(
            """
            UPDATE "any_user"
            SET refresh_token = $1
            WHERE id = $2
        """,
            "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoicmVmcmVzaCIsInN1YiI6IjEiLCJqdGkiOiIyMDI1MTg0ODQ2MTI4MjcxOTQ2IiwiaWQiOjF9.pz9g_HdNh6VPJ9XdgSkXGmwOUp3dbv3kIKdQRdr-xFxrph-zCKEs4CYdTeYNkiOfu0yqfH3DUAqlo-xOb6AnMJIe9KePcZBp_51nuHyT3rxCsrrXKhcRZmAi9wKcnWlI6Cl2xUaW66FN7cJ28sI59lGvmtFwg5e6wIhz22LMVcGsZqEWJluHHsA2reg3nOppJ4h5ElPr2oCX1cAg-_rtCvynbjjs7SmnzhHPvHVrK18rItE8r-jgertaJFInXYwa311Q0axTetbkMFxcnjZwX2dC-KlVt6WZfibtnXHVA4B3QUdxjkXJ4qFxUx5z3Y0NihGxIXtx-L0X9OdMbpWbAQ",
            1,
        )

        print("Данные успешно обновлены.")
    except Exception as e:
        print("Произошла ошибка:", e)
    finally:
        # Закрытие соединения
        await conn.close()


# Запуск асинхронной функции
asyncio.run(update_refresh_token())
