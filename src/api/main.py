# FastAPI entrypoint
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health", response_class=JSONResponse)
def health_check() -> dict:
    """
    Health check endpoint for API status.
    Returns:
        dict: Status message.
    """
    return {"status": "ok"}


# Future: include routers for sessions, cycle logs, metrics, etc.
