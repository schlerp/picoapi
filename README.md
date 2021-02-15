Picoapi
=======

A wrapper around FastAPI to simplify microservice creation. Very opinionated but also simple to fork if you would like to add your own version of service registration and configuration to FastAPI.

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
