""" Make SQLite database from Galton files
"""

from pathlib import Path

import pandas as pd
import sqlalchemy as sa

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, event


Base = declarative_base()


class Family(Base):
    __tablename__ = 'families'

    family = Column(String(10), primary_key=True)
    father = Column(Float)
    mother = Column(Float)


class Child(Base):
    __tablename__ = 'children'

    child_id = Column(Integer, primary_key=True)
    child_number = Column(Integer)
    gender = Column(String(10))
    height = Column(Float)
    family = Column(String(10), ForeignKey('families.family'))


keys_path = Path('galton_keys.db')
if keys_path.exists():
    keys_path.unlink()
db_key = sa.create_engine(f'sqlite:///{keys_path}')

Base.metadata.create_all(db_key)

db_no_key = sa.create_engine('sqlite:///galton_no_keys.db')

table_defs = {
    'children': 'galton_children.csv',
    'families': 'galton_families.csv',
}

for name, csv in table_defs.items():
    df = pd.read_csv(csv)
    if name == 'children':
        df = df.reset_index(names='child_id')
    df.to_sql(name, db_no_key, index=False, if_exists='replace')
    df.to_sql(name, db_key, index=False, if_exists='append')
