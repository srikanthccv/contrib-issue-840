import asyncio
import random

import requests
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (ConsoleSpanExporter,
                                            SimpleSpanProcessor)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

random.seed(54321)


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/ping")
async def health_check():
    return "pong"


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id % 2 == 0:
        # mock io - wait for x seconds
        seconds = random.uniform(0, 3)
        await asyncio.sleep(seconds)
    return {"item_id": item_id, "q": q}


@app.get("/invalid")
async def invalid():
    raise ValueError("Invalid ")


@app.get("/external-api")
def external_api():
    seconds = random.uniform(0, 3)
    response = requests.get(f"https://httpbin.org/delay/{seconds}")
    response.close()
    return "ok"


FastAPIInstrumentor.instrument_app(app, excluded_urls="ping")
