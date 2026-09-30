from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL="sqlite:///rangmanch.db"

engine = create_engine(DATABASE_URL,echo=True)
# echo is actually used to show the sql queries on the command page

def create_table():
    """ create all tables defined by SQL MODEL class """
    SQLModel.metadata.create_all(engine)

def get_session():  # every request will not create different session but these sessions are shared which is called pooling of sessions
    """Dependency that provides database session per request """
    with Session(engine) as session:
        yield session

