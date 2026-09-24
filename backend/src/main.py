from fastapi import FastAPI

from models import User, Post
from routers import auth_route, user_route

app = FastAPI(
    title="Blog-App",
    description="This is a blog app where users can post and read blogs",
)


app.include_router(user_route.router)
app.include_router(auth_route.router)


@app.get("/health", tags=["health"])
def check_health():
    return {"status": "ok"}
