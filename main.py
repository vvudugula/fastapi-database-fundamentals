from contextlib import asynccontextmanager
from typing import Annotated
from routers.llm import router as llm_router

from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

# 1. Define the Database Model (acts as both DB table & Pydantic schema)
class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    price: float

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_name: str = Field(index=True)
    product_name: str | None = None
    description: str | None = None
    price: float

item_id: int | None = Field(default=None, foreign_key="item.id")

    # 2. Use Relationship() so SQLModel knows this is a link, not a column
item: Item | None = Relationship(back_populates="orders")

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


app = FastAPI(
    title="Enterprise AI API",
    version="1.0.0"
)

app.include_router(llm_router)

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

@app.post("/orders/", response_model=Order)
def create_order(order: Order, session: SessionDep):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@app.get("/orders/", response_model=list[Order])
def read_orders(session: SessionDep):
    orders = session.exec(select(Order)).all()
    return orders

@app.get("/")
async def health():
    return {"status": "running"}