from sqlalchemy import create_engine

from rtl433db.conf import postgresql_url

# создаем движок SqlAlchemy
# engine = create_engine(postgresql_url, echo=True)
engine = create_engine(postgresql_url)
