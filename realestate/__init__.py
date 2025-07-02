import pymysql
pymysql.install_as_MySQLdb()

# realestate/__init__.py

from .celery import app as celery_app

__all__ = ('celery_app',)
