import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import uvicorn
import functools


dotenv.load_dotenv()


app = FastAPI(
    title=os.getenv("API_TITLE"),
    description=os.getenv("API_DESCRIPTION"),
    version=os.getenv("API_VERSION"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("API_CORS_ALLOW_ORIGINS", ["*"]),
    allow_credentials=True,
    allow_methods=os.getenv("API_CORS_ALLOW_METHODS", ["*"]),
    allow_headers=os.getenv("API_CORS_ALLOW_HEADERS", ["*"]),
)


@app.on_event("startup")
def register_uservice():
    uservice_definition = {
        "name": os.getenv("API_TITLE"),
        "tags": os.getenv("API_TAGS").split(":") if os.getenv("API_TAGS") else [],
        "host": os.getenv("API_HOST"),
        "port": os.getenv("API_PORT"),
        "healthcheck": {
            "url": "http://{}:{}{}".format(
                os.getenv("API_HOST"),
                os.getenv("API_PORT"),
                os.getenv("API_HEALTH_PATH"),
            ),
            "interval": os.getenv("API_HEALTH_INTERVAL"),
        },
    }

    requests.put(os.getenv("API_REGISTER_PATH"), json=uservice_definition)


@app.get("/health")
async def index():
    return JSONResponse({"status": os.getenv("API_HEALTH_RESPONSE", "I am running!")})


start_app = functools.partial(
    uvicorn.run, app, host=os.getenv("API_BIND"), port=int(os.getenv("API_PORT"))
)

if __name__ == "__main__":

    start_app()
