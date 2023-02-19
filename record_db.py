from flask import json
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    BigInteger, Column, DateTime, ForeignKey, Integer, Float,
    Text, Enum,
    MetaData
)
from sqlalchemy.sql import func
import pandas as pd

from datetime import datetime

Base = declarative_base()



def jsonize_data(data_dict: dict[pd.DataFrame]) -> json:

    def dict_unwrap(data):

        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = dict_unwrap(v)
            return data
        elif isinstance(data, pd.DataFrame):
            return data.to_dict()
        else:
            raise ValueError(f"{type(data)} is not supported")

    to_return = dict_unwrap(data_dict)
    return json.dumps(to_return)
class RecordsInputJson(Base):
    __tablename__ = "records_input_json"

    id = Column(BigInteger, primary_key=True)
    payload = Column(JSONB, nullable=False)
    run_id = Column(BigInteger, ForeignKey("run.id", ondelete="CASCADE"))
    run = relationship("Run", uselist=False, back_populates="records_input_json")


class RecordsOutputJson(Base):
    __tablename__ = "records_output_json"

    id = Column(BigInteger, primary_key=True)
    payload = Column(JSONB, nullable=False)
    run_id = Column(BigInteger, ForeignKey("run.id", ondelete="CASCADE"))
    run = relationship("Run", uselist=False, back_populates="records_output_json")


class Run(Base):
    __tablename__ = "run"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, nullable=False, server_default=func.now())

    records_output_json = relationship("RecordsOutputJson", back_populates="run",
                             cascade="all, delete, delete-orphan")
    records_input_json = relationship("RecordsInputJson", back_populates="run",
                             cascade="all, delete, delete-orphan")


class GenderTable(Base):
    __tablename__ = "gender_table"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    measure_gender = relationship("RecordMeasure", back_populates="gender_type",
                                  cascade="all, delete, delete-orphan")


class RecordTable(Base):
    __tablename__ = "record_table"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    measure_record = relationship("RecordMeasure", back_populates="record_type",
                                  cascade="all, delete, delete-orphan")


class SportTable(Base):
    __tablename__ = "sport_table"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    measure_sport = relationship("RecordMeasure", back_populates="sport_type",
                                  cascade="all, delete, delete-orphan")


class RecordMeasure(Base):
    __tablename__ = "record_measure"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sport_type = Column(Integer, ForeignKey("sport_table.id", ondelete="CASCADE"))
    gender_type = Column(Integer, ForeignKey("gender_table.id", ondelete="CASCADE"))
    record_type = Column(Integer, ForeignKey("record_table.id", ondelete="CASCADE"))
    measure = Column(Float(8), nullable=False)

    run_id = Column(BigInteger, ForeignKey("run.id", ondelete="CASCADE"))
    run = relationship("Run", uselist=False, back_populates="record_measure")


def save_structured_data(
        session: session.Session,
        type_dict: dict,
        dict_data: dict
) -> None:
    for g in type_dict["gender"]:
        session.query(GenderTable.name==g)


