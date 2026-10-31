from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL="sqlite:///rangmanch.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_table():
    """create all table defined by sqlmodel class"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """dependancy which provides a database session per request"""
    with Session(engine) as session :
        yield session