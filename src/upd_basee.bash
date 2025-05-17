python3 my_scripts/clear_db.py
rm -fr alembic/versions/*
alembic revision --autogenerate -m "init"
alembic upgrade head