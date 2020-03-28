revision:
	PYTHONPATH=. alembic revision --autogenerate

upgrade:
	PYTHONPATH=. alembic upgrade head

downgrade:
	PYTHONPATH=. alembic downgrade head

test:
	flake8
