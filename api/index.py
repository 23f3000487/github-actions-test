from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# CORS enable karna
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.post("/")
async def telemetry(data: TelemetryRequest):
    response = {}
    for region in data.regions:
        latencies = np.random.normal(loc=150, scale=20, size=100)
        uptime = np.random.uniform(99, 100, 100)

        response[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptime)),
            "breaches": int(np.sum(latencies > data.threshold_ms)),
        }
    return response
