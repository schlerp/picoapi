import os
from typing import List

import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


def register_uservice():
    uservice_definition = {
        "name": os.getenv("API_TITLE"),
        "tags": os.getenv("API_TAGS", "").split(":"),
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


async def healthcheck():
    return JSONResponse({"status": os.getenv("API_HEALTH_RESPONSE", "I am running!")})


class PicoAPI(FastAPI):
    def __init__(
        self,
        api_health_path=os.getenv("API_HEALTH_PATH"),
        allow_credentials=True,
        allow_origins: List[str] = [
            x for x in os.getenv("API_CORS_ALLOW_ORIGINS", "*").split()
        ],
        allow_methods: List[str] = [
            x for x in os.getenv("API_CORS_ALLOW_METHODS", "*").split()
        ],
        allow_headers: List[str] = [
            x for x in os.getenv("API_CORS_ALLOW_HEADERS", "*").split()
        ],
        *args,
        **kwargs
    ) -> None:

        # call super class __init__
        super().__init__(*args, **kwargs)

        # add the cors middleware
        self.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )

        # add the service registration event
        self.router.on_event("startup", register_uservice)

        # add the healthcheck route
        self.add_api_route(api_health_path, healthcheck)
