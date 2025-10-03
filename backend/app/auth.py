from fastapi import Header, HTTPException
import jwt, time
SECRET = "change_this_secret"  # usa env var en real
ALGO = "HS256"

def authenticate_user(username, password):
    return username == "admin" and password == "secret"

def create_access_token(data: dict, expires: int = 3600):
    payload = data.copy()
    payload.update({"exp": time.time() + expires})
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
