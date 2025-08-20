from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# --- In-memory mock data for sessions ---
sessions: list[dict] = []


def delete_session(session_id: str):
    for idx, s in enumerate(sessions):
        if s["id"] == session_id:
            sessions.pop(idx)
            return {"detail": "Deleted"}
    raise HTTPException(status_code=404, detail="Session not found")


app = FastAPI()

# CORS setup (for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- JWT Auth Middleware (placeholder) ---
# def jwt_auth_middleware(request: Request):
#     # TODO: Implement JWT validation
#     pass

# --- RBAC Decorator (placeholder) ---
# def require_role(role: str):
#     def decorator(func):
#         # TODO: Implement role-based access control
#         return func
#     return decorator


@app.get("/health", response_class=JSONResponse)
def health_check() -> dict:
    """
    Health check endpoint for API status.
    Returns:
        dict: Status message.
    """
    return {"status": "ok"}


# Future: include routers for sessions, cycle logs, metrics, etc.
