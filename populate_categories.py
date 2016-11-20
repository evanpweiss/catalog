from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category

# Connect to Database and create database session
engine = create_engine('sqlite:///new_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Populate database with 10 default categories
categories = ["Speakers",
              "Receivers",
              "Cables",
              "Televisions",
              "Projectors",
              "Screens",
              "Bluray Players",
              "Game Consoles",
              "Furniture",
              "Media"]

for category in categories:
    session.add(Category(name=category))

session.commit()
