from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. Define the Database Model (acts as both DB table & Pydantic schema)
class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    price: float


# 2. Configure the Database Connection
# For SQLite (local file):
DATABASE_URL = "sqlite:///./database.db"
connect_args = {"check_same_thread": False}  # Needed only for SQLite

# For PostgreSQL, swap the URL and remove connect_args:
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"

engine = create_engine(DATABASE_URL, connect_args=connect_args)


# 3. Create Tables on Startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# 4. Dependency Injection for Database Sessions
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# 5. API Endpoints
@app.post("/items/", response_model=Item)
def create_item(item: Item, session: SessionDep):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/items/", response_model=list[Item])
def read_items(session: SessionDep):
    items = session.exec(select(Item)).all()
    return items

