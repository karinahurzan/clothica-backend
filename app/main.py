from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.routers import auth, users, goods, categories, orders, feedbacks, subscriptions
from app.database import engine, Base

Base.metadata.create_all(bind=engine)


def _ensure_user_profile_columns() -> None:
    """Ensure older database instances have the recent user profile columns."""
    statements = (
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS city VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS nova_post_number VARCHAR(255)",
    )
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


_ensure_user_profile_columns()

app = FastAPI(
    title="Clothica API",
    docs_url="/docs",
    openapi_url="/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )


app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(goods.router, prefix="/api/goods", tags=["Goods"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(feedbacks.router, prefix="/api/feedbacks", tags=["Feedbacks"])
app.include_router(
    subscriptions.router, prefix="/api/subscriptions", tags=["Subscriptions"]
)
