import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

psql_login = os.getenv('psql_login')
psql_pass = os.getenv('psql_pass')
psql_db = os.getenv('psql_db')

db_string = f"postgresql://{psql_login}:{psql_pass}@localhost:5432/{psql_db}"

def bdconnect():
    DB = create_engine(db_string)
    Session = sessionmaker(bind=DB)
    session = Session()
    conn = DB.connect()
    return (session, conn)

    
def bdengine():
    DB = create_engine(db_string)
    return DB
