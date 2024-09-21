0
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Table, MetaData, select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import pandas as pd
from pathlib import Path

# Database setup
db_path = Path(__file__).parent / "data/engineering_dashboard.db"
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
metadata = MetaData()

# Define the table structure
engineering_table = Table(
    'engineering', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('person_name', String),
    Column('task_name', String),
    Column('project_code', String),
    Column('project_name', String),
    Column('date', String),
    Column('duration', Float),
    Column('project_description', String)
)

# Create tables if they do not exist
metadata.create_all(engine)

# Context manager for handling sessions
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()

def fetch_tasks(staff):
    """Fetch tasks for a specific staff member."""
    with get_session() as session:
        query = select(engineering_table).where(engineering_table.c.person_name == staff)
        return pd.read_sql(query, con=engine)

def insert_task(task_data):
    """Insert a new task into the database."""
    with get_session() as session:
        insert_stmt = engineering_table.insert().values(**task_data)
        session.execute(insert_stmt)

def delete_tasks(staff):
    """Delete tasks for a specific staff member and reset auto-increment if table is empty."""
    with get_session() as session:
        # Delete all tasks for the specific staff
        delete_stmt = engineering_table.delete().where(engineering_table.c.person_name == staff)
        session.execute(delete_stmt)

        # Check if the table is empty
        query = select(engineering_table).limit(1)
        result = session.execute(query).fetchall()

        # Reset the auto-increment sequence if the table is empty
        if not result:
            session.execute(text("DELETE FROM sqlite_sequence WHERE name='engineering'"))
            session.commit()

def update_tasks(df, staff):
    """Update tasks in the database for a specific staff member."""
    # Delete current user's records from the database
    delete_tasks(staff)

    # Ensure 'id' column is not included in the insertion
    df = df.drop(columns=['id'], errors='ignore')

    # Insert updated dataframe records into the database
    if not df.empty:
        with get_session() as session:
            df.to_sql('engineering', con=engine, if_exists='append', index=False)
