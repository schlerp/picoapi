import os
from typing import List

import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import picoapi.schema
import picoapi.healthcheck


class NotMasterAPIException(Exception):
    def __init__(self, msg="This API is not setup in master mode!"):
        self.msg = msg


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
        is_master=os.getenv("API_MASTER", False),
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

        self.is_master = is_master
        self.services = []
        self.healthchecks = {}
        self.add_api_route(api_health_path, healthcheck)

        if self.is_master:
            # add service registration
            self.add_api_route("/register", self.add_service)
            self.add_api_route("/services/status", self.get_services_status)
            self.add_api_route("/services/definition", self.get_services_status)

        else:
            # add the service registration event
            self.router.on_event("startup", register_uservice)

    async def get_services_status(self):
        return JSONResponse(
            [
                {
                    "name": service.name,
                    "status": self.healthchecks[service.name].get_health()
                    if self.healthchecks.get(service.name, False)
                    else "No healthcheck!",
                }
                for service in self.services
            ]
        )

    async def add_service(self, uservice_def: picoapi.schema.MicroserviceDefinition):
        self.services.append(uservice_def)
        if uservice_def.healthcheck:
            self.healthchecks[uservice_def.name] = picoapi.healthcheck.HealthCheck(
                uservice_def.healthcheck.url,
                uservice_def.healthcheck.interval,
            )
            self.healthchecks[uservice_def.name].start()

    async def get_services_openapi(self):
        def try_get_json(url):
            try:
                return requests.get(url).json()
            except:
                return {"status": "not running!"}

        return JSONResponse(
            [
                {
                    service.name: try_get_json(
                        "http://{}:{}/openapi.json".format(service.host, service.port)
                    ),
                }
                for service in self.services
            ]
        )