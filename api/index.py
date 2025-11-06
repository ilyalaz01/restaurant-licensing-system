from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "works"}

handler = Mangum(app, lifespan="off")