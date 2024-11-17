from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from sqlalchemy.exc import OperationalError

# Database configuration
DATABASE_URL = "postgresql://target_db_user:target_db_password@target_db/target_db"

# Declare a base
Base = declarative_base()
# Attempt to connect to the database with retries
for _ in range(3):
    try:
        # Create an engine
        engine = create_engine(DATABASE_URL)
        break
    except OperationalError:
        print("Connection failed, retrying in 5 seconds...")
        time.sleep(5)
else:
    raise Exception("Failed to connect to the database after multiple attempts.")


# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

# Define the Signal model
class Signal(Base):
    __tablename__ = 'signal'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

# Define the Data model
class Data(Base):
    __tablename__ = 'data'
    timestamp = Column(TIMESTAMP, primary_key=True, nullable=False)
    signal_id = Column(Integer, ForeignKey('signal.id'), primary_key=True, nullable=False)
    value = Column(Float, nullable=False)

# Define the RawSourceData model
class RawSourceData(Base):
    __tablename__ = 'raw_source_data'
    timestamp = Column(TIMESTAMP, primary_key=True, nullable=False)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)

# Create all tables
Base.metadata.create_all(engine)

print("Tables created successfully.")