# Variables
APP_MODULE = src.api:app
HOST = 127.0.0.1
PORT = 8000

# Commands
run:
	PYTHONPATH=src uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload