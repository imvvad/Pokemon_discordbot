from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.schema import ForeignKey

import SQLAlchemy_config as config
import pandas as pd

user     = config.DB_USER
password = config.PASSWORD
host     = config.HOST
db_name  = config.DATABASE

# engineの設定
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{db_name}')

# セッションの作成
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

# テーブルを作成する
Base        = declarative_base()
Base.query  = db_session.query_property()

# テーブルを定義する
# Baseを継承
class raidInfo(Base):
    # テーブル名
    __tablename__ = 'raidInfo'
    # カラムの定義
    id         = Column("id",Integer, primary_key=True, autoincrement=True)
    name       = Column('name', String(255),ForeignKey(column="pokemonInfo.name", name="fk_pokemonInfo_name"),index=True, nullable=True )
    difficulty = Column("difficulty",Integer,nullable=False)


    def __init__(self, id=None, name=None, difficulty=None):
        self.id         = id
        self.name       = name
        self.difficulty = difficulty

class pokemonInfo(Base):
    # テーブル名
    __tablename__ = 'pokemonInfo'
    # カラムの定義
    id         = Column("id",         Integer,     primary_key=True, autoincrement=True)
    name       = Column("name",       String(255), primary_key=True,index=True, unique=True, nullable=False)
    type1      = Column("type1",      String(255), nullable=False)
    type2      = Column("type2",      String(255), nullable=True)
    base_stats = Column('base_stats', String(255), nullable=False)

    def __init__(self, id=None, name=None, type1=None, type2=None, base_stats=None):
        self.id         = id
        self.name       = name
        self.type1      = type1
        self.type2      = type2
        self.base_stats = base_stats

class pokemonAbilities(Base):
    # テーブル名
    __tablename__ = 'pokemonAbilities'
    # カラムの定義
    id           = Column("id",Integer, primary_key=True, autoincrement=True)
    name         = Column('name', String(255), unique=True, nullable=False )
    description  = Column('description', String(255), nullable=False)

    def __init__(self, id=None, name=None, description=None):
        self.id          = id
        self.name        = name
        self.description = description

class pokemonWeapons(Base):
    # テーブル名
    __tablename__ = 'pokemonWeapons'
    # カラムの定義
    id            = Column("id",Integer, primary_key=True, autoincrement=True)
    name          = Column('name', String(255), unique=True, nullable=False )
    description   = Column('description', String(255), nullable=False)

    def __init__(self, id=None, name=None, description=None):
        self.id          = id
        self.name        = name
        self.description = description

class raidInfo_pokemonAbilities(Base):
    # 中間テーブル名
    __tablename__ = 'raidInfo_pokemonAbilities'
    # カラムの定義
    id          = Column("id",Integer, primary_key=True, autoincrement=True)
    raid_id     = Column('raid_id', Integer, ForeignKey(column="raidInfo.id", name="fk_raidInfo_id_for_pokemonAbilities"),nullable=False )
    ability_id  = Column('ability_id', Integer, ForeignKey(column="pokemonAbilities.id", name="fk_pokemonAbilities_id_for_raidInfo"),nullable=False)

    def __init__(self, id=None, raid_id=None, ability_id=None):
        self.id          = id
        self.raid_id      = raid_id
        self.ability_id = ability_id

class pokemonInfo_pokemonAbilities(Base):
    # 中間テーブル名
    __tablename__ = 'pokemonInfo_pokemonAbilities'
    # カラムの定義
    id                  = Column("id",Integer, primary_key=True, autoincrement=True)
    pokemon_id          = Column('pokemon_id', Integer, ForeignKey(column="pokemonInfo.id", name="fk_pokemonInfo_id"),nullable=False )
    ability_id          = Column('ability_id', Integer, ForeignKey(column="pokemonAbilities.id", name="fk_pokemonAbilities_id_for_pokemonInfo"),nullable=False)
    hidden_ability_id   = Column('hidden_ability_id', Integer, ForeignKey(column="pokemonAbilities.id", name="fk_pokemon_hidden_Abilities_id"),nullable=False)

    def __init__(self, id=None, pokemon_id=None, ability_id=None, hidden_ability_id=None):
        self.id          = id
        self.pokemon_id  = pokemon_id
        self.ability_id = ability_id
        self.hidden_ability_id = hidden_ability_id

class raidInfo_pokemonWeapons(Base):
    # 中間テーブル名
    __tablename__ = 'raidInfo_pokemonWeapons'
    # カラムの定義
    id                 = Column("id",Integer, primary_key=True, autoincrement=True)
    raid_id            = Column('raid_id', Integer, ForeignKey(column="raidInfo.id", name="fk_raidInfo_id_for_pokemonWeapons"),nullable=False )
    weapon_id          = Column('weapon_id', Integer, ForeignKey(column="pokemonWeapons.id", name="fk_pokemonWeapons_id"),nullable=False)

    def __init__(self, id=None, raid_id=None, weapons_id=None):
        self.id          = id
        self.raid_id      = raid_id
        self.weapon_id = weapons_id

class raidInfo_pokemonLimitedWeapons(Base):
    # 中間テーブル名
    __tablename__ = 'raidInfo_pokemonLimitedWeapons'
    # カラムの定義
    id                 = Column("id",Integer, primary_key=True, autoincrement=True)
    raid_id            = Column('raid_id', Integer, ForeignKey(column="raidInfo.id", name="fk_raidInfo_id_for_pokemonLimitedWeapons"),nullable=False )
    limited_weapons_id = Column('limited_weapons_id', Integer, ForeignKey(column="pokemonWeapons.id", name="fk_pokemonLimitedWeapons_id"),nullable=False)

    def __init__(self, id=None, raid_id=None, limited_weapons_id=None):
        self.id          = id
        self.raid_id      = raid_id
        self.limited_weapons_id = limited_weapons_id

def read_csv_to_raidInfo_Table(filepath):
    tmp_df = pd.read_csv(filepath)
    for index, _df in tmp_df.iterrows():
        row = raidInfo(name=_df['name'],difficulty=_df['difficulty'])
        db_session.add(row)
    db_session.commit()

def read_csv_to_pokemonInfo_Table(filepath):
    tmp_df = pd.read_csv(filepath)
    for index, _df in tmp_df.iterrows():
        row = pokemonInfo(name=_df['name'],type1=_df['type1'],type2=_df['type2'],base_stats=_df['base_stats'])
        db_session.add(row)
    db_session.commit()

def read_csv_to_pokemonWeapons_Table(filepath):
    tmp_df = pd.read_csv(filepath)
    for index, _df in tmp_df.iterrows():
        row = pokemonWeapons(name=_df['name'],description=_df['description'])
        db_session.add(row)
    db_session.commit()

def read_csv_to_raidInfo_pokemonWeapons_Table(filepath):
    tmp_df = pd.read_csv(filepath)
    for index, _df in tmp_df.iterrows():
        row = raidInfo_pokemonWeapons(raid_id=int(_df['raid_id']),weapons_id=int(_df['weapon_id']))
        db_session.add(row)
    db_session.commit()

def read_csv_to_raidInfo_pokemonLimitedWeapons_Table(filepath):
    tmp_df = pd.read_csv(filepath)
    for index, _df in tmp_df.iterrows():
        row = raidInfo_pokemonLimitedWeapons(raid_id=int(_df['raid_id']),limited_weapons_id=int(_df['weapon_id']))
        db_session.add(row)
    db_session.commit()

#実行
Base.metadata.create_all(bind=engine)

read_csv_to_pokemonInfo_Table('./test_data/pokemonInfo.csv')
read_csv_to_raidInfo_Table('./test_data/raidInfo.csv')
read_csv_to_pokemonWeapons_Table('./test_data/pokemonWeapons.csv')
read_csv_to_raidInfo_pokemonWeapons_Table('./test_data/raidInfo_pokemonWeapons.csv')
read_csv_to_raidInfo_pokemonLimitedWeapons_Table('./test_data/raidInfo_pokemonLimitedWeapons.csv')