from dotenv import load_dotenv
load_dotenv()

import os

from src.main import app
import logging

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    import uvicorn
    host = os.getenv('HOST')
    port = int(os.getenv('PORT'))

    uvicorn.run(
        "main:app",
        host=host,
        port=port
    )
