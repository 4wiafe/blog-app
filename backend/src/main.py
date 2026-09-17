from fastapi import FastAPI

app = FastAPI(
    title="Blog-App",
    description="This is blog app where users can post and read blogs",
)


@app.get("/health", tags=["health"])
def check_health():
    return {"status": "ok"}
