import asyncio
import uvicorn

from src import models
from src.data_fetcher import extraction_loop
from src.database import engine
from src.rest_api import app

# Create/Ensure the database tables
models.Base.metadata.create_all(bind=engine)

def start_rest_api():
    uvicorn.run(app, host="0.0.0.0", port=8001, loop="asyncio")


async def start_data_fetcher():
    await extraction_loop()


async def main():
    # Run the REST API in a separate thread
    loop = asyncio.get_running_loop()
    rest_api_future = loop.run_in_executor(None, start_rest_api)

    # Wait for both tasks to complete
    await start_data_fetcher()
    await rest_api_future

if __name__ == "__main__":
    asyncio.run(main())