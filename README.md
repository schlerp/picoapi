PicoAPI Library
===============

The API Logic Library known as PicoAPI is sole API Logic library. It essentially reimplements the FastAPI interface from the Python FastAPI library with addition of some functions and logic that add some benefits for using FastAPI in a microservices architecture. The PicoAPI class itself allows for two distinct modes of operation, the supervisor (traditionally referred to as master) or worker (traditionally referred to as slave) configuration. Worker Microservices perform a task, they are told what to do and when to do it by a supervisor Microservice. The supervisor microservice knows which workers it can distribute tasks to because each worker microservice registers itself with a supervisor microservice on start.

Registration of worker microservices describes the situation where upon start, the worker microservice sends a put request to a supervisor describing the following about itself:
- Which IP microservice resides on.
- Which port the microservice is bound to.
- The worker microservices version.
- The tags associated with this microservice, these allow the supervisor to know what types of work this microservice can perform and what forms of that work this microservice supports.
- The healthcheck information.

The concept of a healthcheck is simple, it describes the supervisor asking the worker if it is still running. For the supervisor to perform these checks, the worker microservices provide information about how and when to health check them. A healthcheck definition contains two items, the address to check, and the interval for this check to repeat.

A PicoAPI supervisor adds the following functionality to the base FastAPI class:
- Endpoints for the worker microservices to register.
- Logic to perform a healthcheck.

A PicoAPI worker adds the following functionality to the base FastAPI class:
- Logic to register with a supervisor upon start.
- An endpoint to return a healthcheck when the supervisor asks.


Usage
=====

create a .env file or export the following variables:

| ENV variable           	| Required (default) 	| Default             	| Description                                                                                	| Examples                                       	| Implemented 	|
|------------------------	|--------------------	|---------------------	|--------------------------------------------------------------------------------------------	|------------------------------------------------	|-------------	|
| API_HOST               	| Yes                	|                     	| The host of the API                                                                        	| myhost\|123.123.123.123\|localhost\|127.0.0.1  	|             	|
| API_PORT               	| No                 	| 8888                	| The port of the API                                                                        	| 8080                                           	|             	|
| API_BIND               	| Yes                	|                     	| The interface descriptor to bind to                                                        	| 127.0.0.1\|0.0.0.0                             	|             	|
| API_TITLE              	| Yes                	|                     	| The FastAPI title                                                                          	| Example API Name                               	|             	|
| API_DESCRIPTION        	| No                 	| A brief Description 	| The FastAPI description                                                                    	| An Example of a short description about an API 	|             	|
| API_REGISTER_PATH      	| Yes                	|                     	| The url of the Keeper registration endpoint (similar to consul)                            	| http://keeper:8100/register                    	|             	|
| API_HEALTH_PATH        	| No                 	|                     	| The path relative to this FastAPI to call for health checks                                	| /health                                        	|             	|
| API_HEALTH_INTERVAL    	| No                 	| 300                 	| The frequency to perform health checks (in seconds)                                        	| 300                                            	|             	|
| API_VERSION            	| No                 	| 0.0.1               	| The version of this FastAPI                                                                	| 0.0.1-alpha                                    	|             	|
| API_TAGS               	| No                 	|                     	| The tags for this microservice, used as part of discovery, delimited with ":" (like $PATH) 	| servicetag1:servicetag2:servicetag3            	|             	|
| API_CORS_ALLOW_ORIGINS 	| No                 	| *                   	| The CORS allowed origins, delimited with "!"                                               	|                                                	| No          	|
| API_CORS_ALLOW_METHODS 	| No                 	| *                   	| The CORS allowed methods, delimited with "!"                                               	|                                                	| No          	|
| API_CORS_ALLOW_HEADERS 	| No                 	| *                   	| The CORS allowed headers, delimited with "!"                                               	|                                                	| No          	|

Example .env file:

```bash
# API config
# ==========
API_BIND="0.0.0.0"
API_HOST="localhost"
API_PORT="8888"
API_TITLE="test"
API_DESCRIPTION="test description"
API_VERSION="0.0.1-alpha"

# microservice registration
# =========================
API_KEEPER_URL="http://localhost:8100/register"
API_HEALTH_PATH="/health"
API_HEALTH_INTERVAL="300"
```

Authors & Contributors
======================

- [Patrick Coffey](https://github.com/schlerp) - Author
- [Asanga Abeyaratne](https://github.com/asaabey) - Contributor
