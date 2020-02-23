# special sauce in here, or danger
# pull this thread: https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker
FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

LABEL maintainer="Austin Godber <godber@uberhip.com>"

RUN pip install starlette aiofiles

COPY ./app /app
