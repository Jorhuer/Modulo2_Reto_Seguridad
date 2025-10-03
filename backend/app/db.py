from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

class Telemetry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    device_id: str
    ts: int
    temp: float
    lat: Optional[float] = None
    lon: Optional[float] = None

engine = create_engine("sqlite:///telemetry.db", connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def save_telemetry(data: dict):
    with Session(engine) as s:
        t = Telemetry(device_id=data.get("device_id"),
                      ts=int(data.get("ts")),
                      temp=float(data.get("temp")),
                      lat=data.get("lat"),
                      lon=data.get("lon"))
        s.add(t)
        s.commit()

def get_last_for_device(device_id: str, limit: int = 100) -> List[dict]:
    with Session(engine) as s:
        q = select(Telemetry).where(Telemetry.device_id == device_id).order_by(Telemetry.ts.desc()).limit(limit)
        rows = s.exec(q).all()
        return [r.dict() for r in rows]
